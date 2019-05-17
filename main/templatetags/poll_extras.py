from django import template

register = template.Library()


@register.filter
def need(value):
    return 3-value


@register.filter
def compute_sport_rate(value):
    return '{:.0f}'.format(value/0.3) + '%'


@register.filter
def compute_sport_gap(value):
    return 30.0 - value
