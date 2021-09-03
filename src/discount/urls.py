from django.urls import path

from .views import code_apply, AmountPercentDiscountCreateView, CodeDiscountCreateView

urlpatterns = [
    path('code/apply/', code_apply, name='code_apply'),
    path('discount/create/', AmountPercentDiscountCreateView.as_view(), name='amount_discount'),
    path('code/create/', CodeDiscountCreateView.as_view(), name='create_code'),
]
