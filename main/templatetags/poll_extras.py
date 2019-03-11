from django import template

register = template.Library()


@register.filter
def need(value):
    return 3-value
