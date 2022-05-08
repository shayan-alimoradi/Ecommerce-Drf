# Core django imports
from django.urls import path, include

# 3rd-party imports
from rest_framework.routers import SimpleRouter

# Local import
from . import views

app_name = "api_cart"

router = SimpleRouter()
router.register("", views.CartViewSet)

urlpatterns = [
    path("", include(router.urls)),
]