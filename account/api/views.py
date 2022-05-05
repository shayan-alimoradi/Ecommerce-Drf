# Core django imports
from django.contrib.auth import get_user_model

# 3rd-party import
from rest_framework.generics import (
    CreateAPIView,
)

# Local imports
from .serializers import (
    CreateNewUserSerializer,
)

User = get_user_model()


class SignUpAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateNewUserSerializer
