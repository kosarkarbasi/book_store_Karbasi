from django.urls import path

from .views import code_apply

urlpatterns = [
    path('code/apply/', code_apply, name='code_apply'),
]
