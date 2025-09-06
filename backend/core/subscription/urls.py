from django.urls import path
from .views import (
    SubscriptionProductListView,
    CreateCheckoutSessionView,
    CheckoutSuccessView,
    CheckoutCancelView,
)

urlpatterns = [
    path('products/', SubscriptionProductListView.as_view(), name='subscription-products'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('checkout-success/', CheckoutSuccessView.as_view(), name='checkout-success'),
    path('checkout-cancel/', CheckoutCancelView.as_view(), name='checkout-cancel'),
]
