from django import template

register = template.Library()

@register.filter(name='intmultiply')
def intmultiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return value