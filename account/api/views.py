# Core django imports
from django.contrib.auth import get_user_model

# 3rd-party import
from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions

# Local imports
from .serializers import (
    CreateNewUserSerializer,
    UserSerializer,
    SignOutSerializer,
)

User = get_user_model()


class SignUpAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateNewUserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "patch", "delete","head"]


class SignOutAPIView(GenericAPIView):
    """
    Sign-Out & destory the refresh token
    """

    serializer_class = SignOutSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Signed-Out Successfully.")
