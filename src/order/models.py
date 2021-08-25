from django.db import models
from users.models import Customer, User, Address
from product.models import Book
from discount.models import AmountPercentDiscount, CodeDiscount


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
    # items = models.ManyToManyField(ShoppingCart)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.ForeignKey(CodeDiscount, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=8)
    order_date = models.DateTimeField(auto_now_add=True)

    # order_date = models.DateTimeField()

    @property
    def address(self):
        active_address = Address.objects.get(user=self.customer, active=True)
        # active_address = Customer.active_address
        return active_address

    @property
    def total_price_with_discount(self):
        order_items = self.shoppingcart_set.all()
        total = sum([item.item.calculate_price_after_discount() * item.quantity for item in order_items])
        return int(total)

    @property
    def total_price_wihout_discount(self):
        order_items = self.shoppingcart_set.all()
        total = sum([item.item.price * item.quantity for item in order_items])
        return int(total)

    @property
    def total_discount(self):
        return self.total_price_wihout_discount - self.total_price_with_discount

    @property
    def cart_items(self):
        order_items = self.shoppingcart_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    def code_value(self, code):
        if code:
            return self.code.discount_value
        else:
            return 0

    @property
    def check_code(self):
        if self.code.active:
            return True
        else:
            return False

    def change_status(self):
        self.status = 'submit'
        self.save()

    def save_code(self, code):
        self.code = code
        self.save()

    def price_with_code(self, code=None):
        # self.code = code
        if self.code:
            final_price = self.total_price_with_discount - self.code.calculate_discount(self.total_price_with_discount)
            return int(final_price)
        else:
            return int(self.total_price_with_discount)

    def __str__(self):
        return str(self.pk)

    def order_items(self):
        return self.shoppingcart_set.all()

    def clear_cart(self):
        self.shoppingcart_set.all().delete()
        self.save()

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


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
    quantity = models.IntegerField(default=0, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    @property
    def discount(self):
        discount = self.item.discount.discount_value * 100
        return int(discount)

    @property
    def total_cost(self):
        total_cost = self.item.calculate_price_after_discount()
        return total_cost

    def update_quantity(self, quantity):
        self.quantity = quantity

    @property
    def quantity_price(self):
        """
        calculate price with discount * quantity
        :return: price(int)
        """
        price = self.item.calculate_price_after_discount() * self.quantity
        return int(price)

    def remove_from_cart(self):
        self.delete()
        return 'done'

    def __str__(self):
        return self.item.title

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'
