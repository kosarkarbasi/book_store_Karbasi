from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F, Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from discount.models import CodeDiscount
from users.models import Customer
from .models import ShoppingCart, Order


def cart(request):
    """
    this method create an object from customer's order with 'ordering' status
    then check the validation of code that user interred and if the code valid, save it to order's code
    then if everything is ok, pass order and final price with code to cart.html
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
    price_with_code = order.total_price_with_discount
    now = timezone.now()
    if input_code:
        try:
            code_discount = CodeDiscount.objects.get(code__exact=input_code, start_date__lte=now, end_date__gte=now,
                                                     active=True)
            order.save_code(code_discount)
            messages.success(request, 'کد اعمال شد')
            price_with_code = order.price_with_code(code_discount)
        except ObjectDoesNotExist:
            messages.error(request, 'کد اشتباه است')
            price_with_code = order.total_price_with_discount

    context = {'order': order, 'price_with_code': price_with_code}

    return render(request, 'cart.html', context)


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


@login_required(login_url='users:login')
def checkout(request):
    """
    this method get the ordering order of customer and check the quantities
    if everything be ok, it pass the values to template for checkout
    """
    order, created = Order.objects.get_or_create(customer=request.user, status='ordering')

    # check item inventory with item quantity in cart
    shopping_cart = order.shoppingcart_set.all()
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
    price_with_code = order.price_with_code()
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


@login_required(login_url='users:login')
def user_orders(request):
    """
    this method get current customer orders and pass in to user_orders.html template
    """
    user = request.user
    order = Order.objects.filter(customer=user)
    return render(request, 'user_orders.html', {'order': order})


@login_required()
def submit_order(request):
    """
    this method call when customer wants to checkout and pay for items
    it changes status of order form 'ordering' to 'submit'
    so the items will no longer in shopping cart
    """
    order = Order.objects.get(customer=request.user, status='ordering')
    order.change_status()
    return render(request, 'end_order.html')


def best_seller(request):
    best_sellers_books = ShoppingCart.objects.select_related('order').filter(order__status='submit').values(
        'item_id').annotate(total=Count('item_id')).order_by('-total').values_list('item_id', 'total','item__title')
    print(best_sellers_books)
    return render(request, 'home.html', {'best_sellers_books': best_sellers_books})

# select item_id, count(item_id) from public.order_shoppingcart as cart
# inner join public.order_order as orders
# on (cart.order_id=orders.id)
# where orders.status = 'submit'
# group by item_id
# order by count(item_id)
