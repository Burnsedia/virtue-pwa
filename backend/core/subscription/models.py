from django.db import models
from djstripe.models import Product, Price

class SubscriptionProduct(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # Link to the dj-stripe Product model
    djstripe_product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name

class SubscriptionPrice(models.Model):
    subscription_product = models.ForeignKey(
        SubscriptionProduct, on_delete=models.CASCADE, related_name="prices"
    )
    # Link to the dj-stripe Price model
    djstripe_price = models.ForeignKey(
        Price, on_delete=models.SET_NULL, null=True, blank=True
    )
    # You might want to add fields like 'currency', 'amount' here for convenience
    # or rely directly on djstripe_price for that information.

    def __str__(self):
        return f"{self.subscription_product.name} - {self.djstripe_price.unit_amount / 100 if self.djstripe_price else 'N/A'}"
