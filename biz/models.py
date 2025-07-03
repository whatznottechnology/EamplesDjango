from django.db import models
from taggit.managers import TaggableManager
from examples.fields import CompressedImageField

# Create your models here.

class BusinessType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Business Type"
        verbose_name_plural = "Business Types"

class BusinessExample(models.Model):
    types = models.ManyToManyField(BusinessType, related_name='examples')
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    image = CompressedImageField(upload_to='business_examples/', blank=True, null=True, quality=60)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Business Example"
        verbose_name_plural = "Business Examples"
