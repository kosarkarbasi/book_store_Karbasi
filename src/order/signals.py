from django.db.models.signals import post_save
from django.dispatch import receiver
from discount.models import CodeDiscount
from order.models import Order


@receiver(post_save, sender=Order)
def deactivate_discount(sender, instance, created, **kwargs):
    if instance.status == 'ordering':
        pass
    else:
        code = instance.code
        code_instance = CodeDiscount.objects.get(code__exact=code)
        if code_instance.limit == 0:
            code_instance.active = False
            code_instance.save()
