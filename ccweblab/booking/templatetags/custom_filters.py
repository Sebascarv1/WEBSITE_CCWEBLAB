from django import template

register = template.Library()


@register.filter
def get_dict_key(dictionary, key):
    """Get a value from a dictionary using a key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def get_item(obj, key):
    """Get item from dict or list."""
    if isinstance(obj, dict):
        return obj.get(key)
    elif isinstance(obj, (list, tuple)):
        try:
            return obj[int(key)]
        except (ValueError, IndexError):
            return None
    return None


@register.filter
def get_attr(obj, attr):
    """Get an attribute from an object."""
    try:
        return getattr(obj, attr, None)
    except:
        return None
