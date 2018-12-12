from django import template

register = template.Library()


@register.filter
def join_names(objs, separator):
    return separator.join(obj.name for obj in objs)
