from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from discount.forms import CodeDiscountForm
from discount.models import CodeDiscount
from product.models import Book
from users.models import Customer
from .models import ShoppingCart, Order


def cart(request):
    """
    یک آبجت از order برای کاستومر می سازد و اطلاعات آن را به صفحه cart.html پاس می دهد
    :param request:
    :return:
    """
    # print('book_id', book_id)
    if request.user.is_anonymous:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    else:
        customer = request.user

    order, created = Order.objects.get_or_create(customer=customer, status='ordering')
    add = request.GET.get('add')
    remove = request.GET.get('remove')
    # print('book_id', book_id)
    # book = Book.objects.get(id=book_id)
    # print('book', book)
    # shopping_cart_item = ShoppingCart.objects.get(order=order, item=book)
    # print('shopping_cart_item', shopping_cart_item)
    # if add == '+':
    #     shopping_cart_item.quantity += 1
    # elif remove == '_':
    #     shopping_cart_item.quantity -= 1
    #     if shopping_cart_item.quantity == 0:
    #         shopping_cart_item.remove_from_cart()
    input_code = request.GET.get('code')
    print('code: ', input_code)
    code_message = ''
    price_with_code = order.total_price_with_discount
    now = timezone.now()
    if input_code:
        try:
            code_discount = CodeDiscount.objects.get(code__exact=input_code, start_date__lte=now, end_date__gte=now,
                                                     active=True)
            # if code_discount:
            code_message = 'کد اعمال شد'
            price_with_code = order.price_with_code(code_discount)
        except ObjectDoesNotExist:
            code_message = 'کد اشتباه است'
            price_with_code = order.total_price_with_discount

    context = {'order': order, 'code_message': code_message, 'price_with_code': price_with_code}

    return render(request, 'cart.html', context)


def delete_product(request, pk):
    order_item = ShoppingCart.objects.get(id=pk)
    order_item.delete()
    # return render(request, 'cart.html')
    # redirect to same page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login.html')
def checkout(request):
    return render(request, 'checkout.html')
