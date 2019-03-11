from django import template

register = template.Library()


@register.filter
def need(value):
    return 3-value

@register.filter
def compute_sport_rate(value):
    return value
