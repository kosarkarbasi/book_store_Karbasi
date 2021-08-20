from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from discount.forms import CodeDiscountForm
from .models import CodeDiscount


@require_POST
def code_apply(request):
    now = timezone.now()
    form = CodeDiscountForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = CodeDiscount.objects.get(code__exact=code, start_date__lte=now, end_date__gte=now, active=True)
            request.session['code'] = coupon
        except:
            request.session['code'] = None

    return redirect('cart')
