from django.urls import path, include

from rest_framework_nested.routers import NestedDefaultRouter

from . import views
from product.api.urls import router


comment_router = NestedDefaultRouter(router, "product", lookup="product")
comment_router.register("comment", views.CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(comment_router.urls)),
]
