import django_filters
from product.models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {"unit_price": ["lt", "gt"], "category_id": ["exact"]}
