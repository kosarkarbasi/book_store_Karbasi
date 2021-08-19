from django.contrib import admin
from .models import Order, ShoppingCart


# Register your models here.
@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['item','pk', 'quantity', 'order']


class CartInline(admin.StackedInline):
    model = ShoppingCart
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'status', 'order_date', 'code']
    inlines = [CartInline]
