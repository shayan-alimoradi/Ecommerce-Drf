# Core django imports
from django.contrib.auth import get_user_model

# 3rd-party import
from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.viewsets import ModelViewSet

# Local imports
from .serializers import (
    CreateNewUserSerializer,
    UserSerializer
)

User = get_user_model()


class SignUpAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateNewUserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "patch", "delete","head"]
