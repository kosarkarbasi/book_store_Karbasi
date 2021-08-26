from .models import Book, Category, Author


def book_renderer(request):
    return {'all_books': Book.objects.all(),
            'all_categories': Category.objects.all(),
            'all_authors': Author.objects.all()}
