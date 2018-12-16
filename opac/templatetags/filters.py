from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@mark_safe
def names(values, sep):
    return sep.join(escape(v.name) for v in values)
