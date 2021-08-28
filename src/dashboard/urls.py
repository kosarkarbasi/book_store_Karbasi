from django.urls import path

from .views import admin_dashboard, orders_chart, export

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('order-chart/', orders_chart, name='order-chart'),
    path('export/', export, name='export')
]
