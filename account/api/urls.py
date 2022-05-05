# Core django imports
from django.urls import path, include

# 3rd-party imports
from rest_framework.routers import DefaultRouter

# Local import
from . import views

app_name = "api_account"

router = DefaultRouter()
router.register("user", views.UserViewSet, basename="user")

urlpatterns = [
    path("sign-up/", views.SignUpAPIView.as_view(), name="sign_up"),
    path("", include(router.urls)),
]
