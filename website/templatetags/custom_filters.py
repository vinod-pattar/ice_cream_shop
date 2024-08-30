from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies the given value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
