# Core django imports
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

# 3rd-party imports
from rest_framework import serializers

# Local imports
from comment.models import Comment
from product.models import Product


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)

    def create(self, validated_data):
        instance = get_object_or_404(Product, pk=self.context.get("product_id"))
        user_id = self.context.get("user_id")

        Comment.objects.create(
            author_id=user_id,
            content=validated_data.get("content"),
            content_type=instance.get_content_type,
            object_id=instance.id,
        )
        return validated_data
