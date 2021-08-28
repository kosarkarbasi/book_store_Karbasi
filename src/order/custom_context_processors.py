from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from users.models import Customer
from .models import ShoppingCart


# @login_required(login_url='users:login')
def cart(request):
    if request.user.is_anonymous:
        # try:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device, email=None)
    else:
        # except:
        customer = request.user

    cart_items = ShoppingCart.objects.filter(order__customer=customer, order__status='ordering')
    return {'cart_items': cart_items}
