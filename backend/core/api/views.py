from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from djstripe.models import Product, Price
import stripe

from .models import Organization, Project, Issue, TimeLog
from .serializers import *
from .permissions import IsPremiumUser, is_user_premium

stripe.api_key = settings.STRIPE_SECRET_KEY

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated, IsPremiumUser]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not is_user_premium(request.user) and Project.objects.filter(user_owner=request.user).count() >= 1:
            return Response(
                {'detail': 'Free users are limited to one project. Please upgrade to create more.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

class TimeLogViewSet(viewsets.ModelViewSet):
    queryset = TimeLog.objects.all()
    serializer_class = TimeLogSerializer

class SubscriptionProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer

class SubscriptionPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Price.objects.filter(active=True)
    serializer_class = PriceSerializer

class CheckoutViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def create_checkout_session(self, request):
        price_id = request.data.get('price_id')
        if not price_id:
            return Response({'error': 'Price ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url='http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://localhost:3000/cancel',
                # customer_email=request.user.email, # Uncomment if user is authenticated
            )
            return Response({'sessionId': checkout_session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def create_customer_portal_session(self, request):
        # For this to work, the customer must already exist in Stripe
        # and be associated with your Django User model (e.g., via djstripe.Customer)
        customer_id = request.data.get('customer_id') # You'll need to pass the customer ID from frontend

        if not customer_id:
            return Response({'error': 'Customer ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            portalSession = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url='http://localhost:4321/settings', # Frontend URL to return to
            )
            return Response({'url': portalSession.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserSubscriptionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        is_premium = is_user_premium(request.user)
        return Response({'is_premium': is_premium})

