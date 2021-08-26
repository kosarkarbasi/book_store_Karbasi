from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import Customer, Personnel, Admin, Address, User, City, Province


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("city", "postal_code", 'user', 'active',)
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
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ("email", "type", 'date_joined', 'is_staff')
    fields = ("email", 'phone_number', "avatar", "type", 'device', 'is_staff')
    readonly_fields = ['date_joined']

    # def get_queryset(self, request):
    #     qs = super(PersonnelAdmin, self).get_queryset(request)
    #     return qs.filter(is_staff=True)


@admin.register(Admin)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", "type", 'date_joined', 'is_superuser')
    fields = ("email", 'phone_number', "avatar", "type", 'device', 'is_staff')
    readonly_fields = ['date_joined']


# admin.site.register(User)


# class CustomUserAdmin(UserAdmin):
#     list_display = ("email", "type", 'date_joined')
#     ordering = ('email',)


admin.site.register(User, UserAdmin)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ("email", "type", 'date_joined')
#     fields = ("email", 'phone_number', "avatar", "type", 'device', 'password')
#     readonly_fields = ['date_joined']
#
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         is_superuser = request.user.is_superuser
#         disabled_fields = set()
#
#         # Prevent non-superusers from editing their own permissions
#         if (
#                 not is_superuser
#                 and obj is not None
#                 and obj == request.user
#         ):
#             disabled_fields |= {
#                 'is_staff',
#                 'is_superuser',
#                 'groups',
#                 'user_permissions',
#             }
#
#         for f in disabled_fields:
#             if f in form.base_fields:
#                 form.base_fields[f].disabled = True
#
#         return form
