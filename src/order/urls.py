from django.urls import path
import order.views as views

urlpatterns = [
    path('add-to-cart', views.cart, name='cart'),
    path('cart/delete/<int:pk>', views.delete_product, name='delete_item'),
    path('checkout/', views.checkout, name='checkout'),
]