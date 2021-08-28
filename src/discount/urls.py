from django.urls import path

from .views import code_apply, AmountPercentDiscountCreateView

urlpatterns = [
    path('code/apply/', code_apply, name='code_apply'),
    path('code/create/', AmountPercentDiscountCreateView.as_view(), name='create_code'),
]
