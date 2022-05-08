# Stdlib imports
from uuid import uuid4

# Core django imports
from django.db import models

# Local imports
from product.models import Product


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.product.title}"

    class Meta:
        unique_together = [["cart", "product"]]
