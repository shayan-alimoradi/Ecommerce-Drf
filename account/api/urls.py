# Core django imports
from django.urls import path, include

# 3rd-party imports
from rest_framework.routers import DefaultRouter

# Local imports
from . import views

app_name = "api_account"

router = DefaultRouter()
router.register("user", views.UserViewSet, basename="user")
router.register("profile", views.ProfileViewSet)

urlpatterns = [
    path("sign-up/", views.SignUpAPIView.as_view(), name="sign_up"),
    path("sign-out/", views.SignOutAPIView.as_view(), name="sign_out"),
    path(
        "change-password/",
        views.ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path("", include(router.urls)),
]
