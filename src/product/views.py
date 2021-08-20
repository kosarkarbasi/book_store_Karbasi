from datetime import datetime

from django.shortcuts import render, redirect
from django.views import generic

from order.models import Order, ShoppingCart
from users.models import Customer, User
from .models import Book


class BookListView(generic.ListView):
    model = Book
    template_name = 'book_list.html'


def product_detail(request, pk):
    """
    اگر در صفحه جزیات محصول، متد پست باشد، به صفحه سبد خرید هدایت خواهیم شد
    اگر متد get باشد، اطلاعات کتاب به همان صفحه فرستاده می شود
    :param request: request
    :param pk: pk of book
    :return: book_detail(get) or cart(post)
    """
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        book = Book.objects.get(id=pk)
        if request.user.is_anonymous:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        else:
            customer = request.user

        order, created = Order.objects.get_or_create(customer=customer, status='ordering')
        shopping_cart, created = ShoppingCart.objects.get_or_create(order=order, item=book)

        shopping_cart.quantity += int(request.POST['quantity'])

        if int(shopping_cart.quantity) > book.inventory:
            return render(request, 'book_detail.html', {'book': book, 'inventory_message': 'موجودی کتاب کافی نیست'})
        elif int(shopping_cart.quantity) == 0:
            return render(request, 'book_detail.html', {'book': book, 'inventory_message': 'مقدار وارد شده 0 می باشد'})
        shopping_cart.update_quantity(shopping_cart.quantity)
        shopping_cart.save()
        return redirect('cart')

    context = {'book': book}
    return render(request, 'book_detail.html', context)
