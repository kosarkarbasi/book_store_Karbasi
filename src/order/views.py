from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from discount.models import CodeDiscount
from users.models import Customer
from .models import ShoppingCart, Order


def cart(request):
    """
    یک آبجت از order برای کاستومر می سازد و اطلاعات آن را به صفحه cart.html پاس می دهد
    :param request:
    :return:
    """
    if request.user.is_anonymous:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    else:
        customer = request.user

    order, created = Order.objects.get_or_create(customer=customer, status='ordering')

    context = {'order': order}

    return render(request, 'cart.html', context)


def delete_product(request, pk):
    order_item = ShoppingCart.objects.get(id=pk)
    order_item.delete()
    # return render(request, 'cart.html')
    # redirect to same page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def check_discount_code(request):
    input_code = request.GET.get('code')
    total_price = request.GET.get('total')
    print('total_price:', total_price)
    code = CodeDiscount.objects.filter(code__exact=input_code)
    if code.exists():
        code_exist = CodeDiscount.objects.get(code__exact=input_code)
        if code_exist.active and code_exist.start_date < timezone.now() < code_exist.end_date:
            messages.success(request, 'کد تخفیف اعمال شد')
            code_value = int(code_exist.value * 100)

            # code_total = code_exist.calculate_price(total_price=total_price)
            return render(request, 'cart.html',
                          {'code_result': 'کد تخفیف اعمال شد', 'code_value': code_value})
        else:
            return render(request, 'cart.html', {'code_result': 'کد اشتباه است'})
    else:
        messages.error(request, 'کد اشتباه است')
        return render(request, 'cart.html', {'code_result': 'کد اشتباه است'})
