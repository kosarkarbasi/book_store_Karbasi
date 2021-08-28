from django.utils import timezone
from import_export import resources
from order.models import Order


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
