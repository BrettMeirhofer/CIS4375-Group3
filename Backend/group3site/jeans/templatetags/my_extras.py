from django import template
from inspect import ismethod
register = template.Library()


@register.filter
def get_attr(value, arg):
    try:
        out = getattr(value, arg)
        if ismethod(out):
            return out()
        else:
            return out
    except:
        return

@register.filter
def get_field_value(value, arg):
    try:
        return getattr(value, arg).get
    except:
        return value.arg()

@register.filter
def model_name(value):
    return value._meta.db_table