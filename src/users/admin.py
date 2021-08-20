from django.contrib import admin
from django.utils.html import format_html

from .models import Customer, Personnel, Admin, Address, User, City, Province

admin.site.register(User)


# admin.site.register(City)
# admin.site.register(Province)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("city", "postal_code", 'user', 'active')
    # readonly_fields = ('password',)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', "slug")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", 'province_id')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", 'device', 'active_address', "type", 'date_joined')
    fields = ("email", 'phone_number', "avatar", 'device')
    readonly_fields = ('password',)


@admin.register(Personnel)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", "type", 'date_joined')
    fields = ("email", 'phone_number', "avatar", 'device')


@admin.register(Admin)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", "type", 'date_joined')
    fields = ("email", 'phone_number', "avatar", 'device')
