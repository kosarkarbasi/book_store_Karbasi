import random
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from discount.models import CodeDiscount
from users.models import Customer
from .models import ShoppingCart, Order


# @login_required(login_url='users:login')
def cart(request):
    """
    this method create an object from customer's order with 'ordering' status
    then check the validation of code that user interred and if the code valid, save it to order's code
    then if everything is ok, pass order and final price with code to cart.html
    """
    if request.user.is_anonymous:
        device = request.COOKIES.get('device')
        # if Customer.objects.filter(device=device).exists():
        #     print('cart --- new device create')
        #     new_device = uuid.uuid4().hex
        #     print(new_device)
        #     response = render(request, 'cart.html')
        #     response.set_cookie('device', new_device)
        #     return response
        # #     customer = Customer.objects.create(device=new_device)
        # # else:
        # #     print('cart --- device exist')
        customer, created = Customer.objects.get_or_create(device=device)
        print('cart --- customer with device created')
        # customer, created = Customer.objects.get_or_create(device=device)
    else:
        customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, status='ordering')
    now = timezone.now()

    if request.method == "POST":
        data = {}

        item_id = request.POST.get('item_id')
        operation = request.POST.get('buttonText')
        code = request.POST.get('code')

        # check inventory
        if item_id and operation:
            cart = ShoppingCart.objects.get(id=int(item_id))
            if operation == '+' and cart.quantity < cart.item.inventory:
                cart.quantity += 1
                new_quantity_price = cart.quantity_price
                cart.save()
                data['new_quantity_price'] = new_quantity_price
            elif operation == '-' and 1 < cart.quantity <= cart.item.inventory:
                cart.quantity -= 1
                new_quantity_price = cart.quantity_price
                cart.save()
                data['new_quantity_price'] = new_quantity_price
            elif operation == '-' and cart.quantity == 1:
                # cart.delete()
                data['error_message'] = 'میخواهید از کارت خود حذف کنید؟'
            elif operation == '+' and cart.quantity == cart.item.inventory:
                data['error_message'] = 'موجودی کافی نیست'
            cart.save()
            data['new_quantity'] = str(cart.quantity)
            data['order_price_with_discount'] = order.total_price_with_discount
            data['total_discount'] = order.total_discount
            data['price_with_code'] = order.price_with_code

        # check code
        # if request.user.is_authenticated:
        if code:
            try:
                code_discount = CodeDiscount.objects.get(code__exact=code, start_date__lte=now, end_date__gte=now,
                                                         active=True)
                user_orders = Order.objects.filter(customer=customer)
                print(user_orders)
                for user_order in user_orders:
                    if user_order.code == code_discount and user_order.status == 'ordering':
                        data['warning_code'] = "این کد قبلا اعمال شده است"
                    elif user_order.code == code_discount and user_order.status == 'submit':
                        data['error_code'] = "این کد قبلا استفاده شده است"
                    elif user_order.status == 'ordering' and user_order.code is not None:
                        # order.save_code() # if we want to replace code
                        data['warning_code'] = "شما مجاز به استفاده از یک کد هستید"
                else:
                    order.save_code(code_discount)
                    messages.success(request, 'کد اعمال شد')
                    data['code_message'] = "کد اعمال شد"
                    data['order_price_with_discount'] = order.total_price_with_discount
                    data['total_discount'] = order.total_discount
                    data['price_with_code'] = order.price_with_code
                    data['discount_value'] = order.code.discount_value
                    print(data['discount_value'])

            except ObjectDoesNotExist:
                # print('no')
                messages.error(request, 'کد اشتباه است')
                data['error_code'] = "کد اشتباه است"
                data['price_with_code'] = order.price_with_code

        return JsonResponse(data, safe=False)

    if order.shoppingcart_set.all().count() == 0:
        messages.error(request, 'سبد خرید شما خالی است')
        return render(request, 'cart.html')

    price_with_code = order.price_with_code
    context = {'order': order, 'price_with_code': price_with_code}

    return render(request, 'cart.html', context)


# ------------------------------------------------------------------------
def delete_product(request, pk):
    """
    this method calls when customer wants to delete cart items in cart
    :param request: request
    :param pk: primary key of the item that user wants to delete form cart
    :return: cart.html page
    """
    order_item = ShoppingCart.objects.get(id=pk)
    order_item.delete()
    # redirect to same page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# ------------------------------------------------------------------------
@login_required(login_url='users:login')
def checkout(request):
    """
    this method get the ordering order of customer and check the quantities
    if everything be ok, it pass the values to template for checkout
    """
    order, created = Order.objects.get_or_create(customer=request.user, status='ordering')

    # # delete device customer
    # device = request.COOKIES.get('device')
    # device_customer = Customer.objects.get(device=device)
    # device_customer.delete()

    # check item inventory with item quantity in cart
    shopping_cart = order.shoppingcart_set.all()
    if shopping_cart.count() == 0:
        messages.error(request, 'سبد خرید شما خالی است')
        return render(request, 'cart.html')
    for cart_item in shopping_cart:
        if 0 < cart_item.item.inventory < cart_item.quantity:
            messages.error(request, f'موجودی {cart_item.item.title}، {cart_item.item.inventory} عدد است')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif cart_item.item.inventory == 0:
            messages.error(request, f'موجودی {cart_item.item.title} تمام شده است ')
            cart_item.remove_from_cart()
            return render(request, 'cart.html')
    # end check

    code = order.code
    price_with_code = order.price_with_code
    discount = order.code_value(code)
    address = order.address
    if address is None:
        messages.error(request, 'لطفا یک آدرس وارد کنید')
        return redirect('users:user_addresses')
    return render(request, 'checkout.html', {
        'order': order,
        'price_with_code': price_with_code,
        'discount': discount,
        'address': address
    })


# ------------------------------------------------------------------------
@login_required(login_url='users:login')
def user_orders(request):
    """
    this method get current customer orders and pass in to user_orders.html template
    """
    user = request.user
    order = Order.objects.filter(customer=user)
    return render(request, 'user_orders.html', {'order': order})


# ------------------------------------------------------------------------
@login_required()
def submit_order(request):
    """
    this method call when customer wants to checkout and pay for items
    it changes status of order form 'ordering' to 'submit'
    so the items will no longer in shopping cart
    """
    order = Order.objects.get(customer=request.user, status='ordering')
    order.change_status()
    order.reduce_inventory()
    return render(request, 'end_order.html')

# ------------------------------------------------------------------------
