from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render, redirect

from users.models import Customer
from .models import ShoppingCart, Order
from django.contrib.auth.decorators import login_required


def cart(request):
    if request.user.is_anonymous:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    else:
        customer = request.user

    cart_items = ShoppingCart.objects.filter(order__customer=customer)
    for item in cart_items:
        item.item.calculate_price_after_discount()
    return {'cart_items': cart_items}

# def order(request):
#     if request.user.is_anonymous:
#         device = request.COOKIES['device']
#         customer, created = Customer.objects.get_or_create(device=device)
#     else:
#         customer = request.user
#     order_items = Order.objects.get(customer=customer, status='ordering')
#
#     return {'order_items': order_items}
# return redirect('users:login')
