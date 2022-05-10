# Core django imports
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone

# 3rd-party imports
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework import status

# Local imports
from .serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    OrderUpdateSerializer,
)
from order.models import Order, Coupon
from .permissions import IsAdminUser

User = get_user_model()


class OrderAPIView(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "option"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            permission_classes = (IsAdminUser,)
        else:
            permission_classes = (IsAuthenticated,)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related("user").all()
        return Order.objects.filter(user_id=self.request.user.id)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        elif self.request.method == "PATCH":
            return OrderUpdateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(
            data=request.data, context={"user_id": self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


@api_view(("POST",))
def coupon_order(request, order_id):
    code = request.data.get("code")
    time = timezone.now()
    try:
        coupon = Coupon.objects.get(
            code=code, start__lte=time, end__gte=time, active=True
        )
    except Coupon.DoesNotExist:
        return Response(
            {"Error": "Code does not exists or it is expired"},
            status=status.HTTP_404_NOT_FOUND,
        )
    coupon.users.add(request.user.id)
    order = get_object_or_404(Order, ok=order_id)
    order.discount = coupon.discount
    order.save()
    return Response({"Msg": "Success"}, status=status.HTTP_200_OK)
