# Core django imports
from django.contrib.auth import get_user_model

# 3rd-party import
from rest_framework.generics import (
    CreateAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import status

# Local imports
from .serializers import (
    CreateNewUserSerializer,
    UserSerializer,
    SignOutSerializer,
    ChangePasswordSerializer,
    UserRetrieveSerializer,
)

User = get_user_model()


class SignUpAPIView(CreateAPIView):
    """
    Create user

    input_data => {
        "username": <string>,
        "email": <email>,
        "password": <string>
    }
    """

    queryset = User.objects.all()
    serializer_class = CreateNewUserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "patch", "delete", "head"]


class SignOutAPIView(GenericAPIView):
    """
    Sign-Out & destory the refresh token
    """

    serializer_class = SignOutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response("Signed-Out Successfully.")


class ChangePasswordAPIView(APIView):
    """
    An endpoint for changing password.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def put(self, request):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserRetrieveSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "patch", "head"]

    @action(detail=False, methods=["GET", "PATCH"])
    def me(self, request):
        user = User.objects.filter(email=request.user.email).first()
        if request.method == "GET":
            serializer = self.serializer_class(user)
            return Response(serializer.data)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
