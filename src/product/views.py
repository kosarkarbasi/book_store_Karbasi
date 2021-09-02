import json

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
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
    paginate_by = 6

    def dispatch(self, request, *args, **kwargs):
        # data[]
        return super(BookListView, self).dispatch(request, *args, **kwargs)


# ------------------------------------------------------------------------
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
            # try:
            device = request.COOKIES.get('device')
            customer, created = Customer.objects.get_or_create(device=device)

        else:
            customer = request.user

        order, created = Order.objects.get_or_create(customer=customer, status='ordering')
        shopping_cart, created = ShoppingCart.objects.get_or_create(order=order, item=book)
        book_quantity = request.POST.get('quantity')
        shopping_cart.quantity += int(book_quantity)

        data = {}
        if int(shopping_cart.quantity) > book.inventory:
            messages.error(request, 'موجودی کتاب کافی نیست')
            data['error_inventory'] = 'موجودی کتاب کافی نیست'
            shopping_cart.delete()
            # return JsonResponse(data, safe=False, status=1)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        shopping_cart.update_quantity(shopping_cart.quantity)
        shopping_cart.save()
        return redirect('cart')
        # data['order'] = order,
        # return JsonResponse(status=1)

    context = {'book': book}
    return render(request, 'book_detail.html', context)


# ------------------------------------------------------------------------
def category(request, pk):
    """
    Get pk of category and pass books with that category to book_list.html
    :param request: request
    :param pk: primary key of category that user choose
    :return: book_list.html
    """
    books = Book.objects.filter(category=pk)
    return render(request, 'book_list.html', {'books': books})


# ------------------------------------------------------------------------
def author(request, pk):
    """
    Get pk of category and pass books with that category to book_list.html
    :param request: request
    :param pk: primary key of category that user choose
    :return: book_list.html
    """
    books = Book.objects.filter(author=pk)
    return render(request, 'book_list.html', {'books': books})


# ------------------------------------------------------------------------
class BookCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Book
    fields = ('title', 'description', 'author', 'category', 'inventory', 'price', 'discount', 'image', 'score')
    template_name = 'management/book_create.html'
    success_message = 'کتاب با موفقیت اضافه شد'

    def form_valid(self, form):
        form.instance.created = timezone.now()
        form.save()
        return super(BookCreateView, self).form_valid(form)

    @method_decorator(permission_required('product.add_book', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        """ Permission check for this class """
        if not request.user.has_perm('product.add_book'):
            raise PermissionDenied(
                "شما اجاره ایجاد کتاب را ندارید"
            )
        return super(BookCreateView, self).dispatch(request, *args, **kwargs)


# ------------------------------------------------------------------------
class BookUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Book
    fields = ('title', 'description', 'author', 'category', 'inventory', 'price', 'discount', 'image', 'score')
    template_name = 'management/book_update.html'
    success_message = 'کتاب با موفقیت آپدیت شد'

    @method_decorator(permission_required('product.change_book', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        """ Permission check for this class """
        if not request.user.has_perm('product.change_book'):
            raise PermissionDenied(
                "شما اجاره ایجاد آپدیت کتاب را ندارید"
            )
        return super(BookUpdateView, self).dispatch(request, *args, **kwargs)


# ------------------------------------------------------------------------
class AuthorCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Author
    fields = ('first_name', 'last_name')
    template_name = 'management/author_create.html'
    success_message = 'نویسنده با موفقیت اضافه شد'

    @method_decorator(permission_required('product.add_author', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        """ Permission check for this class """
        if not request.user.has_perm('product.add_author'):
            raise PermissionDenied(
                "شما اجاره ایجاد نویسنده را ندارید"
            )
        return super(AuthorCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('book_list')


# ------------------------------------------------------------------------
class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    fields = ('name',)
    template_name = 'management/category_create.html'
    success_message = 'دسته بندی با موفقیت ایجاد گردید'

    @method_decorator(permission_required('product.add_category', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        """ Permission check for this class """
        if not request.user.has_perm('product.add_category'):
            raise PermissionDenied(
                "شما اجاره ایجاد دسته بندی را ندارید"
            )
        return super(CategoryCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('book_list')


# ------------------------------------------------------------------------
def most_least_price(request):
    sort_by = request.GET.get('sortBy')
    data = {}
    print(sort_by)
    if sort_by == '0':
        data['books'] = Book.objects.all()
    elif sort_by == '1':
        data['books'] = Book.objects.all().order_by('-created')
    elif sort_by == '2':
        data['books'] = Book.objects.all().order_by('created')
    else:
        data['error'] = 'یه چیزی اشتباه شده'
    if request.is_ajax():
        # return JsonResponse(data, safe=False)
        # return render(request, 'book_list.html', data)
        # html = render_to_string(
        #     template_name="book_list.html",
        #     context=data
        # )
        t = loader.get_template('book_list.html')
        books = {"books": data}
        # return JsonResponse(books, safe=False)
        # return HttpResponse(t.render(books))
        return render(request, 'book_list.html', books)


def sort(request):
    if request.method == 'GET':
        value = request.GET.get('sort', None)

        if value == '1':
            books = Book.objects.all().order_by('-price')
        elif value == '2':
            books = Book.objects.all().order_by('price')
        else:
            books = Book.objects.all()

        return render(request, 'book_list.html', {'books': books})
