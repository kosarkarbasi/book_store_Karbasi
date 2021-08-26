from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView

from order.models import Order
from product.models import Book
from .forms import SignUpForm, AddressForm
from .models import User, Customer, Address


def registration_view(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            device = request.COOKIES['device']
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            User.objects.create_user(email=email, password=raw_password, device=device, type='CUSTOMER')
            account = authenticate(request, email=email, password=raw_password)
            if account is not None:
                login(request, account)
            else:
                context['registration_form'] = form
                messages.error(request, 'یک چیزی اشتباه شده!')
                return render(request, 'registration/register.html', context)
            return redirect('users:profile')
            # return redirect('home')
        elif User.objects.filter(email__exact=form.cleaned_data.get('email')).exists():
            messages.error(request, 'این ایمیل قبلا ثبت نام شده است')
        elif form.cleaned_data.get('password1') is not form.cleaned_data.get('password2'):
            messages.error(request, 'رمز های وارد شده با هم مطابقت ندارند')
        else:
            messages.error(request, 'لطفا اطلاعات را درست وارد کنید')
    else:
        form = SignUpForm()
        context['registration_form'] = form
    return render(request, 'registration/register.html', context)


# -------------------------------------------------------------------
def login_view(request):
    if request.user.is_anonymous:
        context = {}
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to index page.
                    return redirect("users:profile")
                else:
                    # Return a 'disabled account' error message
                    messages.error(request, 'اکانت شما غیرفعال شده است')
                    return render(request, 'registration/login.html')
            else:
                # Return an 'invalid login' error message.
                messages.error(request, 'اطلاعات وارد شده اشتباه می باشد')
                return render(request, 'registration/login.html', {})
        else:
            # the login is a  GET request, so just show the user the login form.
            return render(request, 'registration/login.html', {})
    return redirect('users:profile')


# -------------------------------------------------------------------
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'رمز عبور شما با موفقیت تغییر یافت')
            return redirect('users:password_change_done')
        else:
            messages.error(request, 'لطفا اطلاعات را به درستی پر کنید')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {
        'form': form
    })


# -------------------------------------------------------------------
@login_required(login_url='users:login')
def add_address(request):
    """
    Read data from AddressForm and save the address to Address Model
    * it set the address to active address and change activation of other addresses to False
    :return: add_address.html
    """
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            province = form.cleaned_data.get('province')
            city = form.cleaned_data.get('city')
            postal_code = form.cleaned_data.get('postal_code')
            full_address = form.cleaned_data.get('full_address')
            active = form.cleaned_data.get('active')
            address = Address(province=province, city=city, postal_code=postal_code, full_address=full_address,
                              active=active)
            address.user = request.user
            address.save()
            previous_addresses = Address.objects.exclude(postal_code=postal_code)
            for addresses in previous_addresses.all():
                addresses.active = False
                addresses.save()
            return redirect('users:profile')
        else:
            messages.error(request, 'لطفا اطلاعات را درست وارد کنید')
    else:
        form = AddressForm()
    return render(request, 'add_address.html', {'form': form})


# -------------------------------------------------------------------
@login_required(login_url='users:login')
def user_addresses(request):
    """
    Filter user addresses and pass them to user_addresses.html
    """
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'user_addresses.html', {'addresses': addresses})


# -------------------------------------------------------------------
@login_required(login_url='users:login')
def activate_address(request, postal_code):
    """
    Activate selected address and deactivate other addresses
    :param request: request
    :param postal_code: postal code of address
    """
    addresses = Address.objects.filter(user=request.user)
    # address_postal_code = request.POST.get(postal_code)
    print(postal_code)
    other_addresses = Address.objects.exclude(postal_code__exact=postal_code)
    for add in other_addresses:
        add.active = False
        add.save()
    address = Address.objects.get(postal_code=postal_code)
    address.active = True
    address.save()
    messages.success(request, 'آدرس با موفقیت فعال شد')
    return render(request, 'user_addresses.html', {'addresses': addresses})


# -------------------------------------------------------------------
class AddressDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Address
    template_name = 'user_addresses.html'
    success_message = 'آدرس با موفقیت حذف شد'
    success_url = "/"

    # def get_success_url(self):
    #     return redirect('users:user_addresses')


def delete_address(request, pk):
    address = Address.objects.filter(pk=pk)
    address.delete()
    messages.success(request, 'آدرس با موفقیت حذف شد.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# -------------------------------------------------------------------
class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ('email', 'first_name', 'last_name', 'phone_number', 'avatar')
    template_name = 'update_profile.html'
    success_message = 'اطلاعات شما با موفقیت آپدیت شد'


# -------------------------------------------------------------------
def admin_dashboard(request):
    this_month = timezone.now().today().month
    month_orders = Order.objects.filter(order_date__month=this_month).count()
    return render(request, 'panels/admin_dashboard.html', {
        'month_orders': month_orders,
    })
