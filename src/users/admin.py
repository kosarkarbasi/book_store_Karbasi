from django.contrib import admin
from django.utils.html import format_html

from .models import Customer, Personnel, Admin, Address, User


# admin.site.register(User)
@admin.register(Address)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("city", "postal_code", 'user', 'active')
    # readonly_fields = ('password',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", 'active_address', "type", 'date_joined')
    fields = ("email", 'phone_number', "avatar")
    readonly_fields = ('password',)


@admin.register(Personnel)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", "type", 'date_joined')
    fields = ("email", 'phone_number', "avatar")


@admin.register(Admin)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", "type", 'date_joined')
    fields = ("email", 'phone_number', "avatar")
