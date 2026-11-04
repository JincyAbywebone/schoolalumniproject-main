from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Safely retrieve a dictionary key, avoiding attribute errors."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, 0)  # Return default 0 if key is missing
    return 0  # If not a dictionary, return 0

@register.filter
def grade_from_mark(mark):
    try:
        mark = float(mark)
    except (ValueError, TypeError):
        return 'N/A'

    if mark >= 91:
        return 'A1'
    elif mark >= 81:
        return 'A2'
    elif mark >= 71:
        return 'B1'
    elif mark >= 61:
        return 'B2'
    elif mark >= 51:
        return 'C1'
    elif mark >= 41:
        return 'C2'
    elif mark >= 33:
        return 'D'
    else:
        return 'E (Fail)'

@register.filter
def dict_get(d, key):
    try:
        return d.get(key)
    except Exception:
        return None    


register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)    
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0
    
@register.filter
def dict_get(d, key):
    return d.get(key)    