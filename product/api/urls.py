# Core django imports
from django.urls import path, include

# 3rd-party imports
from rest_framework.routers import SimpleRouter

# Local imports
from . import views

app_name = "api_product"

router = SimpleRouter()
router.register("product", views.ProductViewSet, basename="product")


urlpatterns = [
    path("", include(router.urls)),
]
