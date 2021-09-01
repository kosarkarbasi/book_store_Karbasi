import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.views.generic import CreateView, UpdateView, DeleteView

from order.models import Order
from .forms import SignUpForm, AddressForm
from .models import User, Customer, Address, Personnel
from django.contrib.auth.models import Group


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

                # match anonymous shopping carts to login user
                current_device_order = Order.objects.get_or_create(device=device, status='ordering',
                                                                   customer__email__isnull=True)
                current_device_order.customer.email = email
                print('current_device_order', current_device_order)
                # device_shopping_items = current_device_order.shoppingcart_set.all()
                # for items in device_shopping_items:
                #     current_device_order.shoppingcart_set.add(items)
                # device_shopping_items.delete()

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


def validate_email(request):
    email = request.GET.get('email')
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


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

                    # match anonymous shopping carts to login user
                    device = request.COOKIES['device']
                    # try:
                    #     device = request.COOKIES['device']
                    #     response = redirect('users:profile')
                    # except:
                    #     device = uuid.uuid4().hex
                    #     response = redirect('users:profile')
                    #     response.set_cookie('device', device)
                    # response.set_cookie('cookie_name2', 'cookie_name2_value')
                    order_with_same_device = Order.objects.filter(customer__device=device, status='ordering').exists()
                    if order_with_same_device:
                        print('login --- order exist -- add orders')
                        current_device_order = Order.objects.get(customer__device=device, status='ordering')
                        print(current_device_order)
                        device_shopping_items = current_device_order.shoppingcart_set.all()
                        print(device_shopping_items)
                        user_order = Order.objects.get_or_create(customer=user, status='ordering')
                        for item in device_shopping_items:
                            print(item)
                            user_order.shoppingcart_set.add(item)
                        print(user_order)
                        current_device_order.delete()

                    login(request, user)
                    # Redirect to index page.
                    return redirect('users:profile')
                    # return response
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
            return render(request, 'registration/login.html')
    return redirect('users:profile')


# -------------------------------------------------------------------
@login_required()
def logout_view(request):
    response = redirect('home')
    response.delete_cookie('device')
    print('deleted')

    logout(request)
    device = uuid.uuid4().hex
    response.set_cookie('device', device, 30)
    # response.delete_cookie('cookie_name2')
    return response


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
    return render(request, 'registration/password_change_form.html', {'form': form})


# -------------------------------------------------------------------
@login_required(login_url='users:login')
def add_address(request):
    """
    Read data from AddressForm and save the address to Address Model
    * it set the address to active address and change activation of other addresses to False
    :return: add_address.html
    """
    if request.method == 'POST':
        form = AddressForm(request.POST, request=request)
        if form.is_valid():
            province = form.cleaned_data.get('province')
            city = form.cleaned_data.get('city')
            postal_code = form.cleaned_data.get('postal_code')
            full_address = form.cleaned_data.get('full_address')
            # active = form.cleaned_data.get('active')
            address = Address(province=province, city=city, postal_code=postal_code, full_address=full_address,
                              active=True)
            address.user = request.user
            address.save()
            previous_addresses = Address.objects.exclude(postal_code=postal_code, user=request.user)
            for addresses in previous_addresses.all():
                addresses.active = False
                addresses.save()
            return redirect('users:user_addresses')
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
    other_addresses = Address.objects.exclude(postal_code__exact=postal_code, user=request.user)
    for add in other_addresses:
        add.active = False
        add.save()
    address = Address.objects.get(postal_code=postal_code, user=request.user)
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
@login_required(login_url='users:login')
def create_personnel(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        personnel = User.objects.create_user(email=email, password=password, type='PERSONNEL')
        personnel.is_staff = True
        personnel_group = Group.objects.get(name__exact='Personnel')
        personnel.save()
        personnel_group.user_set.add(personnel)
        messages.success(request, 'کابر با موفقیت ایجاد شد')
        return render(request, 'panels/create_personnel.html')
    return render(request, 'panels/create_personnel.html')
