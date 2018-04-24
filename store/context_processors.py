from django.utils import timezone


# Checks whether a user is subscribed and returns True or False.
# Used to display relevant text to the user on the  premium content page and also on their profile page.
def user_is_subscribed(request):
    user = request.user
    now = timezone.now()
    if user.is_authenticated:
        subscription_end = user.subscription_ends

        if subscription_end and subscription_end >= now:
            return {'user_is_subscribed': True}
        else:
            return {'user_is_subscribed': False}

    else:
        return {'user_is_subscribed': False}
