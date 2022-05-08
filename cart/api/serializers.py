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


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ("id", "product_id", "quantity")

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data.get("product_id")
        quantity = self.validated_data.get("quantity")

        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id,
                product_id=product_id,
            )
            # Update an existing item
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # Create a new item
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data  # fields in serializer
            )

        return self.instance

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with the given id was found")
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("quantity",)
