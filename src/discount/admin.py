from django.contrib import admin

from .models import CodeDiscount, AmountPercentDiscount

admin.site.register(AmountPercentDiscount)


@admin.register(CodeDiscount)
class CodeDiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'start_date', 'end_date', 'discount', 'active']
    list_filter = ['active']
    search_fields = ['code']
