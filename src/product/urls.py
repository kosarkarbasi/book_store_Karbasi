from django.urls import path
import product.views as views

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book_list'),
    path(r'books/detail/(?P<slug>[-\w]+)/', views.BookDetailView.as_view(), name='book_detail')
]
