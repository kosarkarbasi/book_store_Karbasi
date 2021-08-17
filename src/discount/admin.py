from django.contrib import admin

from .models import CodeDiscount, AmountPercentDiscount

admin.site.register(CodeDiscount)
admin.site.register(AmountPercentDiscount)
