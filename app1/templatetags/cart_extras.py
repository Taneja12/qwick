# app1/templatetags/cart_extras.py

from django import template

register = template.Library()

@register.filter(name='get_quantity')
def get_quantity(dictionary, key):
    return dictionary.get(str(key), 0)  # Default to 0 if key doesn't exist
