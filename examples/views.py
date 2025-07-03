from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from biz.models import BusinessType, BusinessExample
from ecom.models import EcommerceType, EcommerceDemo
from webapp.models import WebAppType, WebAppDemo
from itertools import chain
from taggit.models import Tag
from django.db.models import Count
from functools import reduce
from operator import or_

def home(request):
    # Get filter parameters
    search_query = request.GET.get('q', '').strip()
    biz_type = request.GET.get('biz_type', '')
    ecom_type = request.GET.get('ecom_type', '')
    webapp_type = request.GET.get('webapp_type', '')
    ecom_category = request.GET.get('ecom_category', '')
    tag = request.GET.get('tag', '')
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 30)) # Default to 30 items per load

    # Base querysets with annotations for relevance
    business_examples = BusinessExample.objects.all()
    ecommerce_demos = EcommerceDemo.objects.all()
    webapp_demos = WebAppDemo.objects.all()

    # Apply search filter
    if search_query:
        # Split search query into terms
        search_terms = search_query.lower().split()
        
        if search_query.startswith('#'):
            # Search by tag (case-insensitive)
            tag = search_query[1:].strip()
            business_examples = business_examples.filter(tags__name__iexact=tag)
            ecommerce_demos = ecommerce_demos.filter(tags__name__iexact=tag)
            webapp_demos = webapp_demos.filter(tags__name__iexact=tag)
        else:
            # Create Q objects for each term
            for term in search_terms:
                business_examples = business_examples.filter(
                    Q(name__icontains=term) |
                    Q(description__icontains=term) |
                    Q(tags__name__icontains=term)
                ).distinct()
                
                ecommerce_demos = ecommerce_demos.filter(
                    Q(name__icontains=term) |
                    Q(description__icontains=term) |
                    Q(tags__name__icontains=term)
                ).distinct()
                
                webapp_demos = webapp_demos.filter(
                    Q(name__icontains=term) |
                    Q(description__icontains=term) |
                    Q(tags__name__icontains=term)
                ).distinct()

    # Determine which type filter is active
    active_type = None
    if biz_type:
        active_type = 'business'
        business_examples = business_examples.filter(types__id=biz_type)
        ecommerce_demos = EcommerceDemo.objects.none()
        webapp_demos = WebAppDemo.objects.none()
    elif webapp_type:
        active_type = 'webapp'
        business_examples = BusinessExample.objects.none()
        ecommerce_demos = EcommerceDemo.objects.none()
        webapp_demos = webapp_demos.filter(types__id=webapp_type)
    elif ecom_type or ecom_category:
        active_type = 'ecommerce'
        business_examples = BusinessExample.objects.none()
        webapp_demos = WebAppDemo.objects.none()
        
        # Apply both type and category filters for ecommerce
        if ecom_type:
            ecommerce_demos = ecommerce_demos.filter(types__id=ecom_type)
        if ecom_category:
            ecommerce_demos = ecommerce_demos.filter(category=ecom_category)

    # Apply tag filter
    if tag and not search_query.startswith('#'):  # Don't apply tag filter if already searching by tag
        business_examples = business_examples.filter(tags__name__iexact=tag)
        ecommerce_demos = ecommerce_demos.filter(tags__name__iexact=tag)
        webapp_demos = webapp_demos.filter(tags__name__iexact=tag)

    # Get all types for filters
    biz_types = BusinessType.objects.all()
    ecom_types = EcommerceType.objects.all()
    webapp_types = WebAppType.objects.all()

    # Add type information to each object
    business_examples = [(item, 'business') for item in business_examples.prefetch_related('types', 'tags')]
    ecommerce_demos = [(item, 'ecommerce') for item in ecommerce_demos.prefetch_related('types', 'tags')]
    webapp_demos = [(item, 'webapp') for item in webapp_demos.prefetch_related('types', 'tags')]

    # Combine items in the desired order: business, web app, then ecommerce
    combined_items_all = business_examples + webapp_demos + ecommerce_demos
    
    # Pagination for load more functionality
    total_items = len(combined_items_all)
    paginated_items = combined_items_all[offset:offset+limit]
    has_more = (offset + limit) < total_items

    # Get unique tags
    all_tags = Tag.objects.filter(
        Q(businessexample__isnull=False) |
        Q(ecommercedemo__isnull=False) |
        Q(webappdemo__isnull=False)
    ).distinct().order_by('name')

    # Handle AJAX requests for load more
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'items': [{
                'type': item[1],
                'id': item[0].id,
                'name': item[0].name,
                'description': item[0].description,
                'image_url': item[0].image.url if item[0].image else '',
                'link': item[0].link,
                'types': [t.name for t in item[0].types.all()],
                'tags': [t.name for t in item[0].tags.all()]
            } for item in paginated_items],
            'has_more': has_more,
            'total': total_items
        }
        return JsonResponse(data)

    context = {
        'combined_items': paginated_items,  # Pass only the paginated items for initial load
        'biz_types': biz_types,
        'ecom_types': ecom_types,
        'webapp_types': webapp_types,
        'ecom_categories': dict(EcommerceDemo.CATEGORY_CHOICES),
        'tags': all_tags,
        'search_query': search_query,
        'selected_biz_type': biz_type,
        'selected_ecom_type': ecom_type,
        'selected_webapp_type': webapp_type,
        'selected_ecom_category': ecom_category,
        'selected_tag': tag,
        'active_type': active_type,
        'has_filters': any([biz_type, ecom_type, webapp_type, ecom_category, tag, search_query]),
        'total_items': total_items,
        'has_more': has_more
    }
    return render(request, 'home.html', context)

def search_suggestions(request):
    query = request.GET.get('q', '').strip().lower()
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})

    # Get suggestions from different sources
    suggestions = set()

    # If query starts with #, search only tags
    if query.startswith('#'):
        tag_query = query[1:]
        tags = Tag.objects.filter(name__icontains=tag_query).annotate(
            usage_count=Count('businessexample') + Count('ecommercedemo') + Count('webappdemo')
        ).order_by('-usage_count')[:5]
        suggestions.update(f'#{tag.name}' for tag in tags)
    else:
        # Search in names (case-insensitive)
        business_names = BusinessExample.objects.filter(name__icontains=query).values_list('name', flat=True)[:3]
        ecommerce_names = EcommerceDemo.objects.filter(name__icontains=query).values_list('name', flat=True)[:3]
        webapp_names = WebAppDemo.objects.filter(name__icontains=query).values_list('name', flat=True)[:3]
        suggestions.update(chain(business_names, ecommerce_names, webapp_names))

        # Add tag suggestions (ordered by usage)
        tags = Tag.objects.filter(name__icontains=query).annotate(
            usage_count=Count('businessexample') + Count('ecommercedemo') + Count('webappdemo')
        ).order_by('-usage_count')[:3]
        suggestions.update(f'#{tag.name}' for tag in tags)

    return JsonResponse({'suggestions': list(suggestions)[:8]})  # Limit to 8 suggestions