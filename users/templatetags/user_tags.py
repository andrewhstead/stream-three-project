from django import template

register = template.Library()


@register.filter('activity_type')
def activity_type(contributions):
    return contributions.__class__.__name__


@register.simple_tag(takes_context=True)
def renewal_period(context):

    request = context['request']
    user = request.user

    if user.subscription_plan == 'BIBL_MONTHLY':
        return '1 month'
    elif user.subscription_plan == 'BIBL_THREE':
        return '3 months'
    elif user.subscription_plan == 'BIBL_SIX':
        return '6 months'
    elif user.subscription_plan == 'BIBL_YEARLY':
        return '12 months'
    else:
        return None
