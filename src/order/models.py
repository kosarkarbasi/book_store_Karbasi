from django.contrib import messages
from django.db import models
from users.models import Customer, User, Address
from product.models import Book
from discount.models import AmountPercentDiscount, CodeDiscount


class Order(models.Model):
    """
    The final order that user select all items and order or submit it
    STATUS_CHOICES
    items: selected items --- ForeignKey
    customer: owner of order ---  ForeignKey
    code: discount code ---  ForeignKey
    status: status of order --- ordering / submit
    order_date: datetime for creation of order
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
        """
        :return: active address of customer
        """
        active_address = Address.objects.get(user=self.customer, active=True)
        # active_address = Customer.active_address
        return active_address

    @property
    def total_price_with_discount(self):
        """
        :return: total price of shopping cart with calculate quantity and discount
        """
        order_items = self.shoppingcart_set.all()
        total = sum([item.item.calculate_price_after_discount() * item.quantity for item in order_items])
        return int(total)

    @property
    def total_price_without_discount(self):
        """
        :return: total price of shopping cart with calculate quantity but without discount
        """
        order_items = self.shoppingcart_set.all()
        total = sum([item.item.price * item.quantity for item in order_items])
        return int(total)

    @property
    def total_discount(self):
        """
        :return: value of discount on items
        """
        return self.total_price_without_discount - self.total_price_with_discount

    @property
    def cart_items(self):
        """
        :return: number of items in shopping cart
        """
        order_items = self.shoppingcart_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    def code_value(self, code):
        """
        calculate amount of code discount that user entered
        :param code: discount code that user entered
        :return: value of discount code
        """
        if code:
            return self.code.discount_value
        else:
            return 0

    @property
    def check_code(self):
        """
        check discount code and if it's valid, return True, otherwise, return False
        """
        if self.code.active:
            return True
        else:
            return False

    def change_status(self):
        """
        change status of order form 'ordering' to 'submit' and save it
        """
        self.status = 'submit'
        self.save()

    def save_code(self, code):
        """
        save code that user entered
        :param code: discount code that user entered
        """
        self.code = code
        self.save()

    def price_with_code(self):
        """
        calculate the final price with code discount and AmountPercent discount
        :return: final price of order
        """
        # self.code = code
        if self.code:
            final_price = self.total_price_with_discount - self.code.calculate_discount(self.total_price_with_discount)
            return int(final_price)
        else:
            return int(self.total_price_with_discount)

    def __str__(self):
        return str(self.pk)

    def order_items(self):
        """
        :return: items of order
        """
        return self.shoppingcart_set.all()

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


class ShoppingCart(models.Model):
    """
    every item that user order is locate in this model
    fields:
    item: item that user choose to add to cart --- ForeignKey
    quantity: quantity of item
    order: number of order of the item --- ForeignKey
    """
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    @property
    def discount(self):
        """
        :return: discount value of the item
        """
        discount = self.item.discount.discount_value * 100
        return int(discount)

    @property
    def total_cost(self):
        """
        :return: price of the item after discount
        """
        total_cost = self.item.calculate_price_after_discount()
        return total_cost

    @property
    def quantity_price(self):
        """
        calculate price with discount * quantity
        :return: price(int)
        """
        price = self.item.calculate_price_after_discount() * self.quantity
        return price

    def update_quantity(self, quantity):
        """
        update and save the quantity of item
        :param quantity: entered quantity of item by user
        """
        self.quantity = quantity

    def __str__(self):
        return self.item.title

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'
