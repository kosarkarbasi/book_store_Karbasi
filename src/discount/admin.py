from django.contrib import admin, messages

from .models import CodeDiscount, AmountPercentDiscount

admin.site.register(AmountPercentDiscount)


@admin.register(CodeDiscount)
class CodeDiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'start_date', 'end_date', 'discount', 'limit', 'active']
    list_filter = ['active']
    search_fields = ['code']
    list_editable = ['active', 'limit']
    actions = ['make_inactive', ]

    def make_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, 'inactivate finished', messages.SUCCESS)

    make_inactive.short_description = 'make inactive'
