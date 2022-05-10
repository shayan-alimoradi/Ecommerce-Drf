from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "content_type",
        "object_id",
        "content_object",
        "id",
    )
