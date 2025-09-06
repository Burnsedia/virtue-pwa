from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.urls import reverse
import stripe

from .models import SubscriptionProduct, SubscriptionPrice
from .serializers import SubscriptionProductSerializer, SubscriptionPriceSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class SubscriptionProductListView(generics.ListAPIView):
    queryset = SubscriptionProduct.objects.all()
    serializer_class = SubscriptionProductSerializer
    permission_classes = [] # Allow unauthenticated access to list products

class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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
                success_url=request.build_absolute_uri(reverse('checkout-success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('checkout-cancel')),
                client_reference_id=request.user.id, # Link to your user
                customer_email=request.user.email, # Pre-fill customer email
            )
            return Response({'sessionId': checkout_session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckoutSuccessView(APIView):
    # This view will be hit by Stripe after a successful checkout.
    # You'll typically handle the actual subscription creation/update via webhooks.
    # This is more for redirecting the user to a success page.
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if not session_id:
            return Response({'error': 'Session ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # In a real application, you'd verify the session with Stripe
        # and then update your local database based on the webhook event.
        # For now, we'll just return a success message.
        return Response({'message': 'Checkout successful! Your subscription will be activated shortly.'})

class CheckoutCancelView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Checkout cancelled.'})

# You would also need views for webhook handling (dj-stripe handles this largely)
# and potentially a view for users to manage their subscriptions (e.g., cancel, view status)
# which would interact with dj-stripe's Customer and Subscription models.
