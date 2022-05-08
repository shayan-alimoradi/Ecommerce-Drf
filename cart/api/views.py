# 3rd-party imports
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet

# Local imports
from .serializers import (
    CartSerializer,
)
from cart.models import Cart


class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = Cart.objects.prefetch_related("cart_items__product").all()
    serializer_class = CartSerializer
