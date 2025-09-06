from rest_framework import permissions
from djstripe.models import Subscription

def is_user_premium(user):
    if not user.is_authenticated:
        return False
    # Check if the user has an active, paid subscription
    # This assumes a Customer object exists for the user in djstripe
    return Subscription.objects.filter(
        customer__subscriber=user,
        status__in=['active', 'trialing']
    ).exists()

class IsPremiumUser(permissions.BasePermission):
    """
    Allows access only to authenticated premium users.
    """
    def has_permission(self, request, view):
        return is_user_premium(request.user)
