# Core django imports
from django.urls import path, include

# 3rd-party imports
from rest_framework.routers import SimpleRouter

# Local imports
from . import views

app_name = "api_order"

router = SimpleRouter()
router.register("", views.OrderAPIView, basename="order")


urlpatterns = [
    path("", include(router.urls)),
]
