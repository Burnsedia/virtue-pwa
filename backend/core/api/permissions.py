from rest_framework import permissions
from djstripe.models import Subscription, Customer

def is_user_premium(user):
    if not user.is_authenticated:
        return False
    # Ensure the user has a profile
    if not hasattr(user, 'profile'):
        return False
    try:
        customer = Customer.objects.get(subscriber=user)
    except Customer.DoesNotExist:
        return False
    # Check if the user has an active, paid subscription
    return Subscription.objects.filter(
        customer=customer,
        status__in=['active', 'trialing']
    ).exists()

class IsPremiumUser(permissions.BasePermission):
    """
    Allows access only to authenticated premium users.
    """
    def has_permission(self, request, view):
        return is_user_premium(request.user)
