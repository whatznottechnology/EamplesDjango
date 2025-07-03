from django.contrib import admin
from django.utils.html import format_html
from .models import EcommerceType, EcommerceDemo

@admin.register(EcommerceType)
class EcommerceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'demo_count')
    search_fields = ('name', 'description')
    list_per_page = 20
    
    def demo_count(self, obj):
        return obj.demos.count()
    demo_count.short_description = 'Demos'

@admin.register(EcommerceDemo)
class EcommerceDemoAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview_image', 'category', 'link_display', 'created_at', 'tag_list')
    list_filter = ('types', 'category', 'tags', 'created_at')
    search_fields = ('name', 'description', 'tags__name')
    filter_horizontal = ('types',)
    readonly_fields = ('preview_image_large',)
    save_on_top = True
    view_on_site = True
    radio_fields = {"category": admin.HORIZONTAL}

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                ('image', 'preview_image_large'),
                'link',
                'category',
                'types',
                'tags',
            ),
            'classes': ('wide',)
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/widgets.css',)
        }
        js = ('admin/js/jquery.init.js', 'admin/js/SelectBox.js', 'admin/js/SelectFilter2.js',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    tag_list.short_description = 'Tags'

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;"/>', obj.image.url)
        return "-"
    preview_image.short_description = 'Preview'

    def preview_image_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px;"/>', obj.image.url)
        return "-"
    preview_image_large.short_description = 'Image Preview'

    def link_display(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.link, obj.link)
    link_display.short_description = 'Link'
