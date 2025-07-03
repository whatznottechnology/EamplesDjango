from django.db import models
from taggit.managers import TaggableManager
from examples.fields import CompressedImageField

# Create your models here.

class WebAppType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Web App Type"
        verbose_name_plural = "Web App Types"

class WebAppDemo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    image = CompressedImageField(upload_to='webapp_demos/', blank=True, null=True, quality=60)
    types = models.ManyToManyField(WebAppType, related_name='demos')
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Web App Demo"
        verbose_name_plural = "Web App Demos"
