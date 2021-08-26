from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# from .views import RegistrationView, ProfileView
from django.views.generic import TemplateView

from .views import (registration_view,
                    login_view,
                    change_password,
                    add_address,
                    user_addresses,
                    activate_address,
                    ProfileUpdateView,
                    AddressDeleteView,
                    delete_address,
                    admin_dashboard, )

app_name = 'users'

urlpatterns = [
    path('address/', add_address, name='add_address'),
    path('profile/', login_required(TemplateView.as_view(template_name='profile.html')), name='profile'),
    path('user/addresses/', user_addresses, name='user_addresses'),
    path('user/addresses/active<int:postal_code>', activate_address, name='activate_address'),

    path('<int:pk>/delete/', delete_address, name='delete_address'),
    path('profile/update/<int:pk>', ProfileUpdateView.as_view(), name='update_profile'),

    path('admin/panel/', admin_dashboard, name='admin_dashboard'),

    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login'), name='logout'),
    path('register/', registration_view, name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', change_password, name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
