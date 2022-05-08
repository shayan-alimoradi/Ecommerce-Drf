# Core django imports
from django.urls import path, include

# 3rd-party imports
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

# Local imports
from . import views

app_name = "api_cart"

router = SimpleRouter()
router.register("", views.CartViewSet)

carts_router = routers.NestedDefaultRouter(router, "", lookup="cart")
carts_router.register("items", views.CartItemViewSet, basename="cart-items")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(carts_router.urls)),
]