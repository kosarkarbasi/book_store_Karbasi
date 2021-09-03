from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class AmountPercentDiscount(models.Model):
    """
    amount or percent discount that apply on every book
    fields
    type: discount type - percent/amount
    max_discount: maximum value of discount
    percent: value of percent discount
    amount: value of amount discount
    """
    DISCOUNT_TYPE_CHOICES = (
        ('Percent', 'Percent'),
        ('Amount', 'Amount'),
    )
    type = models.CharField(choices=DISCOUNT_TYPE_CHOICES, max_length=7)
    percent = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    max_discount = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def cancle_activation(self):
        if self.active:
            self.active = False

    @property
    def discount_value(self):
        if self.type == 'Percent':
            return self.percent
        elif self.type == 'Amount':
            return self.amount

    def __str__(self):
        if self.amount is None:
            return f'{self.type} | {self.percent * 100}%'
        elif self.percent is None:
            return f'{self.type} | {self.amount}'

    def get_absolute_url(self):
        # return reverse('book_detail', kwargs={'slug': self.slug})
        return reverse('home')

    class Meta:
        verbose_name = 'تخفیف مقداری/درصدی'
        verbose_name_plural = 'تخفیف های مقداری/درصدی'


class CodeDiscount(models.Model):
    """
    discount code that get percent and apply on shopping cart
    code: discount code
    discount: discount percent
    start_date: start date of discount
    end_date: end date of discount
    active: active or deactivate
    """
    code = models.CharField(max_length=10, primary_key=True)
    discount = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    limit = models.IntegerField(null=True, blank=True)
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

    def calculate_discount(self, total_price):
        final_price = total_price * self.discount
        return final_price

    @property
    def discount_value(self):
        return int(self.discount * 100)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'تخفیف کدی'
        verbose_name_plural = 'تخفیف های کدی'
