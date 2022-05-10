from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("account.api.urls", namespace="api_account")),
    path("api/v1/product/", include("product.api.urls", namespace="api_product")),
    path("api/v1/cart/", include("cart.api.urls", namespace="api_cart")),
    path("api/v1/order/", include("order.api.urls", namespace="api_order")),
    # path("api/v1/comment/", include("comment.api.urls", namespace="api_comment")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
