from django.urls import path, include

from rest_framework_nested.routers import NestedDefaultRouter

from . import views
from product.api.urls import router

app_name = "api_comment"

comment_router = NestedDefaultRouter(router, "products", lookup="product")
comment_router.register("comments", views.CommentViewSet, basename="product-comments")

reply_router = NestedDefaultRouter(comment_router, "comments", lookup="comment")
reply_router.register("reply", views.CommentReplyViewSet, basename="reply")

urlpatterns = [
    path("", include(comment_router.urls)),
    path("", include(reply_router.urls)),
]
