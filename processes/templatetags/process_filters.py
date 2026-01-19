"""
Template filters for processes app
"""
from django import template
from django.utils.safestring import mark_safe
from datetime import datetime
import json

register = template.Library()


@register.filter
def format_audit_value(value):
    """
    Format audit log old_value/new_value for display.

    Converts raw dictionaries into human-readable format.
    """
    if not value:
        return mark_safe('<span class="text-muted">None</span>')

    # If it's already a string (shouldn't happen but handle it)
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return value

    # If it's not a dict at this point, just return it
    if not isinstance(value, dict):
        return str(value)

    # Format the dictionary nicely
    output = []
    for key, val in value.items():
        # Format the key
        formatted_key = key.replace('_', ' ').title()

        # Format the value
        if isinstance(val, bool):
            formatted_val = '✓ Yes' if val else '✗ No'
        elif val is None:
            formatted_val = '<span class="text-muted">None</span>'
        elif isinstance(val, str):
            # Check if it's a datetime string
            if 'T' in val or '+' in val or val.count('-') == 2 and val.count(':') == 2:
                try:
                    # Try to parse and format datetime
                    dt = datetime.fromisoformat(val.replace('Z', '+00:00'))
                    formatted_val = dt.strftime('%Y-%m-%d %H:%M:%S')
                except (ValueError, AttributeError):
                    formatted_val = val
            else:
                formatted_val = val
        else:
            formatted_val = str(val)

        output.append(f'<strong>{formatted_key}:</strong> {formatted_val}')

    return mark_safe('<br>'.join(output))
