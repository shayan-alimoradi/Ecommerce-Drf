# Core django imports
from django.urls import path, include

# 3rd-party imports
from rest_framework.routers import DefaultRouter

# Local imports
from . import views

app_name = "api_product"

router = DefaultRouter()
router.register("", views.ProductViewSet, basename="product")
router.register("category", views.CategoryViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
