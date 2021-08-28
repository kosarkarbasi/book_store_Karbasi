from django.contrib import admin
from .models import Order, ShoppingCart


# Register your models here.
@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['item', 'pk', 'quantity', 'order']
    search_fields = ['order', ]


class CartInline(admin.StackedInline):
    model = ShoppingCart
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'status', 'total_price', 'order_date', 'code']
    inlines = [CartInline]
    list_filter = ['status', ]
    readonly_fields = ['order_date']
