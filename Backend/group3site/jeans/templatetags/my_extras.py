from django import template

register = template.Library()


@register.filter
def get_attr(value, arg):
    try:
        return getattr(value, arg)
    except:
        return

@register.filter
def model_name(value):
    return value._meta.db_table