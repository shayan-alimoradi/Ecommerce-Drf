# Core django imports
from django.urls import path, include

# Local import
from . import views

app_name = "api_account"

urlpatterns = [
    path("sign-up/", views.SignUpAPIView.as_view(), name="sign_up"),
]
