# Core django imports
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

# Local imports
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "id",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    def add_to_admin(self, request, queryset):
        updated = queryset.update(is_admin=True)
        self.message_user(
            request,
            ngettext(
                "%d user was successfully add to admin.",
                "%d users were successfully add to admin.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    def remove_from_admin(self, request, queryset):
        updated = queryset.update(is_admin=False)
        self.message_user(
            request,
            ngettext(
                "%d user was successfully removed from admin.",
                "%d users were successfully removed from admin.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


admin.site.register(Profile)
admin.site.unregister(Group)
