# Core django imports
from django.contrib import admin

# Local imports
from .models import Cart, CartItem


@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "id")
    search_fields = ("cart", "product")


admin.site.register(Cart)
