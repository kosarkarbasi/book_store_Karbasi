import json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
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


def search_result(request):
    search_term = request.GET.get('search')
    book = Book.objects.get(title__exact=search_term)
    return render(request, 'search_results.html', {'book': book})

