# Core django imports
from django.urls import path, include

# 3rd-party imports
from rest_framework.routers import DefaultRouter

# Local imports
from . import views

app_name = "api_product"

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")
router.register("category", views.CategoryViewSet)


urlpatterns = [
    path("like/", views.LikeProductAPIView.as_view(), name="like"),
    path("dislike/", views.DislikeProductAPIView.as_view(), name="dislike"),
    path("", include(router.urls)),
]
