"""
Custom template filters for locations app
"""
from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """
    Multiply the value by the argument.

    Usage: {{ value|multiply:5 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
