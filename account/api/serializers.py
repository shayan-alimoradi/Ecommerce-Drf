# Core django imports import
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Third-party import
from rest_framework import serializers

User = get_user_model()


class CreateNewUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        qs = User.objects.filter(username__icontains=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("This username has already exists")
        return value

    def validate_email(self, value):
        qs = User.objects.filter(email__icontains=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("This email address has already exists")
        return value

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")
        user_obj = User(
            username=username,
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api_account:user-detail", lookup_field="pk"
    )
    phoneNumber = serializers.ModelField(
        model_field=User()._meta.get_field("phone_number")
    )

    class Meta:
        model = User
        fields = (
            "url",
            "username",
            "email",
            "phoneNumber",
        )


class SignOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token)
        except TokenError:
            pass


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
