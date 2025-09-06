from rest_framework import serializers
from .models import SubscriptionProduct, SubscriptionPrice

class SubscriptionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionProduct
        fields = '__all__'

class SubscriptionPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPrice
        fields = '__all__'
