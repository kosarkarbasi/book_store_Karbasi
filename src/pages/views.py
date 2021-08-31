import json
from datetime import timedelta

from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import ListView

from config import settings
from order.models import ShoppingCart
from product.models import Book


# --------------------------------------------------------------------
class SearchResultsView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        search_result = Book.objects.filter(
            Q(title__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query)
        )
        return search_result


# --------------------------------------------------------------------
def search_view(request):
    if request.is_ajax():
        query = request.GET.get('term')
        queryset = list(Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)))
        result = []
        for obj in queryset:
            data = {'label': obj.title, 'value': obj.title}
            result.append(data)
            print(data)
        dump = json.dumps(result)

    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(dump, mimetype)


# --------------------------------------------------------------------
def search_result(request):
    search_term = request.GET.get('search')
    book = Book.objects.get(title__exact=search_term)
    return render(request, 'search_results.html', {'book': book})


# --------------------------------------------------------------------
def home(request):
    best_sellers_ids = ShoppingCart.objects.select_related('order').filter(order__status='submit').values(
        'item_id').annotate(total=Count('item_id')).order_by('-total').values_list('item_id')
    best_sellers_books = []
    for best_id in best_sellers_ids:
        book = Book.objects.get(pk=best_id[0])
        best_sellers_books.append(book)

    now = timezone.now().today()
    after_one_week = now + timedelta(days=-7)
    newest_books = Book.objects.filter(created__lte=now, created__gte=after_one_week)
    return render(request, 'home.html', {'best_sellers_books': best_sellers_books, 'newest_books': newest_books})

# --- SQL query
# select item_id, count(item_id) from public.order_shoppingcart as cart
# inner join public.order_order as orders
# on (cart.order_id=orders.id)
# where orders.status = 'submit'
# group by item_id
# order by count(item_id)
