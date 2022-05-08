# Stdlib imports
from decimal import Decimal

# 3-party imports
from rest_framework import serializers

# Local imports
from cart.models import Cart, CartItem
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "title",
            "unit_price",
            "amount",
            "discount",
            "total_price",
        )


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "total_price")

    def get_total_price(self, obj) -> Decimal:
        return obj.product.total_price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "cart_items", "total_price")

        extra_kwargs = {"id": {"read_only": True}}

    def get_total_price(self, obj):
        return sum(
            [item.quantity * item.product.total_price for item in obj.cart_items.all()]
        )
