from django.contrib import admin
from .models import Order, ShoppingCart

# Register your models here.
admin.site.register(Order)
admin.site.register(ShoppingCart)
