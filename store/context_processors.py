from django.utils import timezone


def user_is_subscribed(request):
    user = request.user
    now = timezone.now()
    if user.is_authenticated:
        subscription_end = user.subscription_ends

        if subscription_end >= now:
            return {'user_is_subscribed': True}
        else:
            return {'user_is_subscribed': False}

    else:
        return {'user_is_subscribed': False}
