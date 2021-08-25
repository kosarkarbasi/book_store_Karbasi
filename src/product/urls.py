from django.urls import path
import product.views as views

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book_list'),
    # path(r'books/detail/(?P<slug>[-\w]+)/', views.product_detail, name='book_detail'),
    path(r'books/detail/<int:pk>', views.product_detail, name='book_detail'),
    path('books/search/', views.book_after_search, name='book_search'),
    # path(r'books/delete/<int:pk>', views.delete_product, name='book_delete'),
]
