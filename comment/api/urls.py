from django.urls import path, include

from rest_framework_nested.routers import NestedDefaultRouter

from . import views
from product.api.urls import router


comment_router = NestedDefaultRouter(router, "product", lookup="product")
comment_router.register("comment", views.CommentViewSet, basename="comment")


reply_router = NestedDefaultRouter(comment_router, "comment", lookup="comment")
reply_router.register("reply", views.CommentReplyViewSet, basename="reply")

urlpatterns = [
    path("", include(comment_router.urls)),
    path("", include(reply_router.urls)),
]
