from django.db.models import Q
from django.views.generic import ListView
from product.models import Book


class SearchResultsView(ListView):
    model = Book
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        search_result = Book.objects.filter(
            Q(title__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query)
        )
        return search_result
