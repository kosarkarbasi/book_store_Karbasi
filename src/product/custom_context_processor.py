from .models import Book, Category


def book_renderer(request):
    return {'all_books': Book.objects.all(),
            'all_categories': Category.objects.all()}
