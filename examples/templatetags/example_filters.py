from django import template
from biz.models import BusinessExample
from ecom.models import EcommerceDemo
from webapp.models import WebAppDemo

register = template.Library()

@register.filter
def model_name(obj):
    """Returns the model name of the given object."""
    return obj._meta.model_name if obj else ''

@register.filter
def isinstance(obj, class_name):
    """Check if an object is an instance of a given class."""
    if class_name == "BusinessExample":
        return isinstance(obj, BusinessExample)
    elif class_name == "EcommerceDemo":
        return isinstance(obj, EcommerceDemo)
    elif class_name == "WebAppDemo":
        return isinstance(obj, WebAppDemo)
    return False 