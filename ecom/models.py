from django.db import models
from taggit.managers import TaggableManager
from examples.fields import CompressedImageField

# Create your models here.

class EcommerceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "E-commerce Type"
        verbose_name_plural = "E-commerce Types"

class EcommerceDemo(models.Model):
    CATEGORY_CHOICES = [
        ('single', 'Single Vendor'),
        ('multi', 'Multi Vendor'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    image = CompressedImageField(upload_to='ecommerce_demos/', blank=True, null=True, quality=60)
    types = models.ManyToManyField(EcommerceType, related_name='demos')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='single')
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_vendor_type(self):
        if not self.category:
            return None
        return "Multivendor" if self.category == 'multi' else "Single Vendor"

    def get_category_name(self):
        if not self.category:
            return None
        category_dict = dict(self.CATEGORY_CHOICES)
        return category_dict.get(self.category)

    class Meta:
        verbose_name = "E-commerce Demo"
        verbose_name_plural = "E-commerce Demos"
