from django.urls import path
from django.views.generic import TemplateView
from .views import SearchResultsView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
