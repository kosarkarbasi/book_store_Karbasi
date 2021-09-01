import random
import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect

from users.models import Customer
from .models import ShoppingCart, Order


@login_required()
def cart(request):
    if request.user.is_anonymous:
        try:
            device = request.COOKIES['device']
        # device = request.COOKIES['device']
        # print('context processor -- device exist')
        except:
            device = uuid.uuid4().hex
            response = HttpResponse()
            response.set_cookie('device', device, secure=False)
            print('context processor -- device doesn"t exist')
            return response
        customer, created = Customer.objects.get_or_create(device=device, email=None)

    else:
        # except:
        customer = request.user

    cart_items = ShoppingCart.objects.filter(order__customer=customer, order__status='ordering')
    return {'cart_items': cart_items}

# ----------------------------------------------------------
