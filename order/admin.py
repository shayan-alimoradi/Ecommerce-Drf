from django.contrib import admin

from .models import Order, OrderItem, Coupon


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("product", "order", "quantity")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "is_paid", "id")
    list_filter = ("is_paid",)

    inlines = (OrderItemAdmin,)


admin.site.register(OrderItem)
admin.site.register(Coupon)
