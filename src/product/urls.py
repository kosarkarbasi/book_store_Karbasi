from django.urls import path
import product.views as views

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book_list'),
    path(r'books/detail/<int:pk>', views.product_detail, name='book_detail'),
    path('category/<int:pk>', views.category, name='category'),
    path('author/<int:pk>', views.author, name='author'),

    path('create/book/', views.BookCreateView.as_view(), name='book_create'),
    path('update/book/<int:pk>/', views.BookUpdateView.as_view(), name='book_update'),

    path('create/author/', views.AuthorCreateView.as_view(), name='author_create'),

    path('create/category/', views.CategoryCreateView.as_view(), name='category_create'),

    # path('sort/by/', views.most_least_price, name='sort'),
    path('sort/', views.sort, name='sort'),
]
