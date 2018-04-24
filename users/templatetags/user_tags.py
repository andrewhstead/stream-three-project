from django import template
from django.contrib.auth.models import Group

register = template.Library()


# Allows posts and comments to be recorded differently in a user's recent activity on their profile.
@register.filter('activity_type')
def activity_type(contributions):
    return contributions.__class__.__name__


# Checks which billing plan the user chose on subscription so they can be reminded of their billing period.
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


# Checks whether a user is a blogger in order to include that information only on bloggers' profiles.
@register.filter('in_group')
def in_group(user, group_name):
    group = Group.objects.get(name=group_name)

    if group in user.groups.all():
        return True
    else:
        return False
