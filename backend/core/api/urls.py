from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('organizations', OrganizationViewSet)
router.register('projects', ProjectViewSet)
router.register('issues', IssueViewSet)
router.register('timelogs', TimeLogViewSet)
router.register('products', SubscriptionProductViewSet)
router.register('prices', SubscriptionPriceViewSet)
router.register('checkout', CheckoutViewSet, basename='checkout')
router.register('reports', ProjectReportViewSet, basename='reports')
router.register('clients', ClientViewSet)
router.register('invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/me/subscription_status/', UserSubscriptionStatusView.as_view(), name='user-subscription-status'),
]

