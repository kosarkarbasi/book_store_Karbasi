from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, LoginForm
from .models import User, Customer


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
            return redirect('profile')
            # return redirect('home')
        else:
            messages.error(request, 'لطفا اطلاعات را درست وارد کنید')
    else:
        form = SignUpForm()
        context['registration_form'] = form
    return render(request, 'registration/register.html', context)


# class LoginView(auth_views.LoginView):
#     form_class = LoginForm
#     template_name = 'registration/login.html'
#     success_url = reverse_lazy('home')

def login_view(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'خوش آمدید')
                # Redirect to index page.
                return redirect("profile")
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

# -------------------------------------------------------------------

# class ProfileView(UpdateView):
#     model = User
#     fields = ['first_name', 'last_name', 'email', 'phone_number', 'avatar']
#     template_name = 'registration/profile.html'
#
#     # def get_success_url(self):
#     #     return reverse('index')
#
#     # def get_object(self):
#     #     return self.request.user
