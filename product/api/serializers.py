# Stdlib imports
from decimal import Decimal

# 3rd-party imports
from rest_framework import serializers

# Local imports
from product.models import (
    Product,
    Category,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "title",
        )

    def validate_title(self, value):
        qs = Category.objects.filter(title__icontains=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Title exists")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    unitPrice = serializers.ModelField(
        model_field=Product()._meta.get_field("unit_price")
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "unitPrice",
            "price_with_tax",
            "amount",
            "created",
            "category",
        )

    def get_price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class ProductDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    favourite = serializers.CharField(source="favourite_to_str", read_only=True)
    like = serializers.CharField(source="like_to_str", read_only=True)
    dislike = serializers.CharField(source="dislike_to_str", read_only=True)
    unitPrice = serializers.ModelField(
        model_field=Product()._meta.get_field("unit_price")
    )
    totalPrice = serializers.ModelField(
        model_field=Product()._meta.get_field("total_price")
    )

    class Meta:
        model = Product
        fields = (
            "title",
            "slug",
            "description",
            "available",
            "unitPrice",
            "amount",
            "discount",
            "totalPrice",
            "image",
            "sell",
            # 'comments',
            "category",
            "favourite",
            "like",
            "dislike",
            "created",
            "updated",
        )

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    # def get_category(self, obj):
    #     return CategorySerializer(instance=obj.category).data

    def get_category(self, obj):
        return Category.objects.all().values("id", "title")


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "available",
            "unit_price",
            "amount",
            "discount",
            "total_price",
            "image",
            "sell",
            "category",
            # "tags",
        )
        extra_kwargs = {"description": {"required": False}}

    def validate_title(self, value):
        qs = Product.objects.filter(title__icontains=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title has already exists")
        return value
