# Core django imports
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)
from django.db.models.signals import post_save
from django.conf import settings


def phone_validate(value):
    if len(value) != 11:
        raise ValueError("Phone number must be an 11 character")
    if not value.isnumeric():
        raise ValueError("Phone number must be a number")


class User(AbstractUser):
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    phone_number = models.CharField(
        max_length=15, blank=True, validators=[phone_validate]
    )

    def get_first_name(self):
        return self.first_name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"


def user_profile_save(sender, **kwargs):
    if kwargs["created"]:
        user_profile = Profile(user=kwargs["instance"])
        user_profile.save()


post_save.connect(user_profile_save, sender=User)
