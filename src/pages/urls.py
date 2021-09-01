from django.urls import path
from django.views.generic import TemplateView
from .views import search_view, search_result, home

urlpatterns = [
    path('', home, name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('search/', search_result, name='search_results'),
    path(r'^ajax_calls/search/', search_view, name='search'),

]
