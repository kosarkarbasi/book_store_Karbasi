from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from django.views.generic import CreateView, UpdateView

from order.models import Order, ShoppingCart
from users.models import Customer, User
from .models import Book, Category, Author


class BookListView(generic.ListView):
    """
    Class-based view for list of books
    """
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'


def book_after_search(request):
    """
    Method for search ====== fail :/
    """
    if request.method == 'GET':
        books = request.GET.get()
        print(books)
        return render(request, 'search_results.html')


def product_detail(request, pk=None):
    """
    Function-based view for book_detail
    In book_detail.html,
    if method == 'POST', and the inventory of book is enough, then user redirect to cart
    if method == 'GET', the book_detail.html with book details will show
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
            messages.error(request, 'موجودی کتاب کافی نیست')
            shopping_cart.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif int(shopping_cart.quantity) == 0:
            messages.error(request, 'تعداد وارد شده 0 عدد می باشد')
            shopping_cart.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        shopping_cart.update_quantity(shopping_cart.quantity)
        shopping_cart.save()
        return redirect('cart')

    context = {'book': book}
    return render(request, 'book_detail.html', context)


def category(request, pk):
    """
    Get pk of category and pass books with that category to book_list.html
    :param request: request
    :param pk: primary key of category that user choose
    :return: book_list.html
    """
    books = Book.objects.filter(category=pk)
    return render(request, 'book_list.html', {'books': books})


def author(request, pk):
    """
    Get pk of category and pass books with that category to book_list.html
    :param request: request
    :param pk: primary key of category that user choose
    :return: book_list.html
    """
    books = Book.objects.filter(author=pk)
    return render(request, 'book_list.html', {'books': books})


class BookCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Book
    fields = ('title', 'description', 'author', 'category', 'inventory', 'price', 'discount', 'image', 'score')
    template_name = 'management/book_create.html'
    success_message = 'کتاب با موفقیت اضافه شد'

    def form_valid(self, form):
        form.instance.created = timezone.now()
        form.save()
        return super(BookCreateView, self).form_valid(form)

    # def get_success_url(self):
    #     return reverse('users:profile')


class BookUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Book
    fields = ('title', 'description', 'author', 'category', 'inventory', 'price', 'discount', 'image', 'score')
    template_name = 'management/book_update.html'
    success_message = 'کتاب با موفقیت آپدیت شد'


class AuthorCreateView(SuccessMessageMixin,LoginRequiredMixin, CreateView):
    model = Author
    fields = ('first_name', 'last_name')
    template_name = 'management/author_create.html'
    success_message = 'نویسنده با موفقیت اضافه شد'

    def get_success_url(self):
        return reverse('book_list')
