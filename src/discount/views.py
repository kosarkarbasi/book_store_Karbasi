from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from discount.forms import CodeDiscountForm
from .models import CodeDiscount, AmountPercentDiscount


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


class AmountPercentDiscountCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AmountPercentDiscount
    fields = ('type', 'percent', 'amount', 'max_discount', 'active')
    template_name = 'discount_create.html'
    success_message = 'تخفیف با موفقیت اضافه شد'
    # success_url = redirect('home')

    @method_decorator(permission_required('discount.add_amountpercentdiscount', raise_exception=True))
    def dispatch(self, request, *args, **kwargs):
        """ Permission check for this class """
        if not request.user.has_perm('discount.add_amountpercentdiscount'):
            raise PermissionDenied(
                "شما اجاره ایجاد تخفیف را ندارید"
            )
        return super(AmountPercentDiscountCreateView, self).dispatch(request, *args, **kwargs)
