from django.db import models
from users.models import Customer, User
from product.models import Book
from discount.models import AmountPercentDiscount, CodeDiscount


class ShoppingCart(models.Model):
    """
    سفارشات کاربر در سبد خریدش، در این مدل قرار می گیرد
    کاربر می تواند آیتمی را حذف یا اضافه کند
    fields:
    item: آن کتابی که کاربر برای افزودن به سبد خرید انتخاب کرده است
    quantity: تعداد انتخابی از آن کتاب
    customer: کاربری که آن کتاب را انتخاب کرده است که در حالت پیشفرض مهمان است
    discount: مقدار تخفیف روی آن کتاب
    price: قیمت کتاب بدون در نظر گرفتن تخفیف
    cost: هزینه نهایی کتاب
    """
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def price(self):
        price = self.item.price * self.quantity
        return price

    @property
    def discount(self):
        discount = self.item.discount
        return discount

    @property
    def cost(self):
        total_cost = self.item.calculate_price_after_discount()
        return total_cost

    def remove_from_cart(self):
        self.delete()
        return 'done'

    def __str__(self):
        return f'{self.customer} | {self.item}'

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'


class Order(models.Model):
    """
    اوردر نهایی که کاربر تمامی آیتم هارا انتخاب کرده و ثبت یا سفارش میکند
    STATUS_CHOICES
    items: آیتم های انتخابی
    customer_id: آیدی مشتری
    code: کد تخفیف
    status: وصعیت ثبت یا سفارش
    start_date: تاریخ تشکیل اوردر
    order_date: تاریخ دادن اوردر
    """
    STATUS_CHOICES = [('ordering', 'سفارش'), ('submit', 'ثبت')]
    items = models.ManyToManyField(ShoppingCart)
    customer_id = models.OneToOneField(Customer, on_delete=models.CASCADE)
    code = models.ForeignKey(CodeDiscount, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=8)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()

    @property
    def address(self):
        active_address = Customer.objects.filter(pk=self.customer_id).filter(addresses__active=True)
        # active_address = Customer.active_address
        return active_address

    @property
    def total_price(self):
        queryset = self.items.all().aggregate(
            total_price=models.Sum('cost'))
        return queryset["total_price"]

    def price_with_code(self):
        final_price = self.code.calculate_price(self.total_price)
        return final_price

    def __str__(self):
        return f'{self.customer_id} | {self.status}'

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'



