from django.core.mail import send_mail
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.urls import reverse

from .managers import UserManager
from django.contrib.auth.models import PermissionsMixin

from phonenumber_field.modelfields import PhoneNumberField
from smart_selects.db_fields import ChainedForeignKey


class User(AbstractBaseUser, PermissionsMixin):
    """
    مدل کاربر
    type: نوع کاربر : مشتری/کارمند/ادمین
    email: ایمیل که باید یکتا باشد
    first_name: نام
    last_name: نام خانوادگی
    date_joined: تاریخ جوین شدن
    is_active: اکتیو است یا نه
    is_staff: استف هست یا نه
    is_superuser: یوپریوزر هست یا نه
    avatar: آواتار کاربر
    address: آدرس کاربر
    phone_number: شماره تلفن کاربر
    """

    class Type(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        PERSONNEL = 'PERSONNEL', 'Personnel'
        ADMIN = 'ADMIN', 'Admin'

    type = models.CharField(max_length=50, choices=Type.choices)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    device = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField('نام', max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatar.png')
    phone_number = PhoneNumberField(max_length=11, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # A list of the field names that will be prompted for
    # when creating a user via the createsuperuser management command.
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    @property
    def active_address(self):
        active_address = Address.objects.filter(user=self.pk).filter(active=True).values_list(
            'full_address', flat=True)
        return active_address

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        # return reverse('users:profile', kwargs={'pk': self.pk})
        return reverse('users:profile')

    def __str__(self):
        if self.email:
            name = self.email
        else:
            name = self.device
        return str(name)


# -------------- managers

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.CUSTOMER)


class PersonnelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.PERSONNEL)


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.ADMIN)


# -------------- end managers


class Customer(User):
    base_type = User.Type.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتری ها'

    def save(self, *args, **kwargs):
        """
        متد سیو اورراید شده است که هر دفعه نیازی نباشد type را برای یوزرها تعریف کنیم
        """
        if not self.pk:
            self.type = User.Type.CUSTOMER
        return super().save(*args, **kwargs)


class Personnel(User):
    # is_staff = models.BooleanField(default=True)
    base_type = User.Type.PERSONNEL
    objects = PersonnelManager()

    class Meta:
        proxy = True
        # permissions = ('product.add_book',)
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندها'

    def save(self, *args, **kwargs):
        """
        متد سیو اورراید شده است که هر دفعه نیازی نباشد type را برای یوزرها تعریف کنیم
        """
        if not self.pk:
            self.type = User.Type.PERSONNEL
        return super().save(*args, **kwargs)


class Admin(User):
    base_type = User.Type.ADMIN
    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = 'ادمین'
        verbose_name_plural = 'ادمین ها'

    def save(self, *args, **kwargs):
        """
        متد سیو اورراید شده است که هر دفعه نیازی نباشد type را برای یوزرها تعریف کنیم
        """
        if not self.pk:
            self.type = User.Type.ADMIN
        return super().save(*args, **kwargs)


# -------------- Address Models

class Province(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'استان'
        verbose_name_plural = 'استان ها'


class City(models.Model):
    name = models.CharField(max_length=20)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهر ها'


class Address(models.Model):
    """
    مدل آدرس کاربر
    city: شهر
    province: استان
    postal code: کد پستی
    full_address: آدرس کامل
    active: اکتیوبودن یا نبودن : True/false
    """

    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    city = ChainedForeignKey(City,
                             chained_field="province",
                             chained_model_field="province",
                             show_all=False,
                             auto_choose=True,
                             sort=True,
                             on_delete=models.SET_NULL,
                             null=True)
    postal_code = models.IntegerField(validators=[MaxValueValidator(9999999999)])
    full_address = models.TextField(max_length=200)
    active = models.BooleanField(default=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.full_address

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'
