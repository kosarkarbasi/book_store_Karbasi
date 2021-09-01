import uuid

from django.http import HttpResponse
from django.shortcuts import render

from order.models import Order
from users.models import Customer


def user_orders(customer_id):
    orders = Order.objects.filter(customer_id=customer_id)
    return orders


def update_cookie(request, device, template):
    if Customer.objects.filter(device=device).exists():
        print('update cookie --- exist')
        new_device = uuid.uuid4().hex
        # Render the template with the manually set value
        response = render(request, template)
        # Actually set the cookie.
        response.set_cookie('device', new_device)
        return response
    return render(request, template)
