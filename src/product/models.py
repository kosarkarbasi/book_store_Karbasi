from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.urls import reverse
from autoslug import AutoSlugField  # install django-autoslug module

from discount.models import AmountPercentDiscount


class Category(models.Model):
    """
    model for category of book
    name: name of category
    """
    name = models.CharField(max_length=20, unique=True)

    @property
    def check_category(self):
        """
        used in menubar in book_list.html
        :return: True/False
        """
        for book in Book.objects.all():
            if self.name in book.category.all().values_list('name', flat=True):
                return True
            else:
                return False

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Author(models.Model):
    """
    model of Author of books
    first_name: first name of author
    last_name: last name of author
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسندگان'

    def __str__(self):
        return self.full_name


class Book(models.Model):
    """
    fields:
    title: name of book
    author: author of book
    category: category of book - ForeignKey
    inventory: inventory of book
    price: price of book
    created: date of creation of book
    image: image of book
    score: score of book
    """
    title = models.CharField(max_length=100)
    author = models.ManyToManyField(Author, related_name='authors')
    category = models.ManyToManyField(Category, related_name='books')
    description = models.TextField(max_length=1200, null=True, blank=True)
    inventory = models.IntegerField()
    price = models.PositiveBigIntegerField()
    discount = models.ForeignKey(AmountPercentDiscount, on_delete=models.CASCADE, null=True, blank=True)
    # slug = models.SlugField(null=False, unique=True, allow_unicode=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='books/')
    score = models.PositiveSmallIntegerField(
        choices=(
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
        ),
        null=True,
        blank=True
    )

    # (1, "★☆☆☆☆"),
    # (2, "★★☆☆☆"),
    # (3, "★★★☆☆"),
    # (4, "★★★★☆"),
    # (5, "★★★★★"),

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'

        ordering = ('created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('book_detail', kwargs={'slug': self.slug})
        return reverse('book_detail', kwargs={'pk': self.pk})

    def update_count(self, quantity):
        """
        update inventory after per order
        :param quantity: quantity of book that customer ordered
        :return: update value of inventory
        """
        if quantity < self.inventory:
            self.inventory = self.inventory - quantity
        else:
            return 'موجودی کتاب کافی نیست'

    def calculate_price_after_discount(self):
        """
        calculate price after percent or amount discount
        :return: price of product after discount
        """
        if self.discount:
            if self.discount.type == 'Amount':
                new_price = self.price - self.discount.amount
                if new_price < self.discount.max_discount:
                    # self.price = new_price
                    return int(new_price)
                else:
                    return int(self.price)

            elif self.discount.type == 'Percent':
                new_price = self.price - (self.price * self.discount.percent)
                self.price = new_price
                return int(new_price)
        else:
            return int(self.price)


class Comment(models.Model):
    """
    writer: writer of comment - ForeignKey
    book: name of book - ForeignKey
    score: score of book
    title: title of comment
    content: content of comment
    timestamp: date and time of comment
    """
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    score = models.PositiveSmallIntegerField(
        choices=(
            (1, "★☆☆☆☆"),
            (2, "★★☆☆☆"),
            (3, "★★★☆☆"),
            (4, "★★★★☆"),
            (5, "★★★★★"),
        )
    )
    title = models.CharField(max_length=180)
    content = models.CharField(max_length=900)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return ", ".join((str(self.writer), str(self.book)))

    class Meta:
        ordering = ["-timestamp"]
        unique_together = ("writer", "book",)
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
