from django.urls import path
from django.views.generic import TemplateView
from .views import SearchResultsView, search_view, search_result

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    # path('search/', SearchResultsView.as_view(), name='search_results'),
    path('search/', search_result, name='search_results'),
    path(r'^ajax_calls/search/', search_view, name='search'),
]
