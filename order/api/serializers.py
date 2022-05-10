# Core django imports
from django.db import transaction
from django.core.mail import EmailMessage

# 3rd-party imports
from rest_framework import serializers

# Local imports
from order.models import Order, OrderItem
from cart.models import CartItem, Cart
from .tasks import send_order_email


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        # all the bunch of code should be executed
        # or none of them
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]

            order = Order.objects.create(user_id=self.context["user_id"])

            cart_items = CartItem.objects.filter(cart_id=cart_id)
            order_items = [
                OrderItem(order=order, product=item.product, quantity=item.quantity)
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            email = EmailMessage(
            subject="Test Subject",
            body="Thanks for your order, Hope you enjoy it.",
            # from_email=user,
            to=[email],
            )
            send_order_email.delay(email)

            return order

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("No cart with the given id was found")
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError("Cart Item is empty")
        return cart_id


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "created",
            "is_paid",
            "discount",
            "order_item",
            "status",
        )


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("status",)
