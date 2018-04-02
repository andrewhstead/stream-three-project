from django import template

register = template.Library()


@register.filter
def activity_type(contributions):
    return contributions.__class__.__name__
