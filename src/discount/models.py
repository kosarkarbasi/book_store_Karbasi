from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class AmountPercentDiscount(models.Model):
    """
    تخفیف مقداری یا درصدی که ادمین آن را تعریف کرده و روی هر کتاب میتواند اعمال شود
    fields
    type: # نوع تخفیف - درصدی یا مقداری
    book_id: آیدی کتابی که شامل تخفیف می شود
    max_discount: حداکثر مقداری که میتواند از قیمت کتاب کم شود
    percent: درصدی که روی کتاب تخفیف می خورد
    amount: مقداری که روی کتاب تخفیف می خورد
    """
    DISCOUNT_TYPE_CHOICES = (
        ('Percent', 'Percent'),
        ('Amount', 'Amount'),
    )
    type = models.CharField(choices=DISCOUNT_TYPE_CHOICES, max_length=7)
    percent = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    max_discount = models.FloatField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def cancle_activation(self):
        if self.active:
            self.active = False

    def __str__(self):
        if self.amount is None:
            return f'{self.type} | {self.percent}%'
        elif self.percent is None:
            return f'{self.type} | {self.amount}'

    class Meta:
        verbose_name = 'تخفیف مقداری/درصدی'
        verbose_name_plural = 'تخفیف های مقداری/درصدی'


class CodeDiscount(models.Model):
    """
    کد تخفیف که یک درصدی به آن داده شده و هرکاربر با وارد کردن کد، روی کل خریدش تخفیف میگیرد
    code: کد تخفیف
    value: مقدار درصد تخفیف
    start_date: شروع تاریخ تخفیف
    end_date: پایان تخفیف
    active: اکتیو بودن یا نبودن
    """
    code = models.CharField(max_length=10, primary_key=True)
    value = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=False)

    def check_activation(self):
        now = datetime.now()
        if self.start_date < now < self.end_date:
            self.active = True
            return True
        self.active = False
        return False

    def cancle_activation(self):
        if self.active:
            self.active = False

    def calculate_price(self, total_price):
        final_price = total_price * self.value
        return final_price

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'تخفیف کدی'
        verbose_name_plural = 'تخفیف های کدی'
