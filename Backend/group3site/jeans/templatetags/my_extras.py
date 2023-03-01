from django import template

register = template.Library()


@register.filter
def get_attr(value, arg):
    try:
        return getattr(value, arg)
    except:
        return