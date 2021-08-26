from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField, AuthenticationForm
from django.core.validators import MaxValueValidator

from .models import User, Address, City, Customer, Province
from django import forms
from django.shortcuts import get_list_or_404, get_object_or_404


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='required')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    email = forms.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'password',)


class AddressForm(forms.ModelForm):
    # province = forms.ChoiceField(label='')
    # city = forms.ChoiceField(label='')
    # active = forms.BooleanField(widget=forms.BooleanField, label='')

    class Meta:
        model = Address
        fields = ['province', 'city', 'postal_code', 'full_address']
        labels = {
            'city': '',
            'province': '',
            'postal_code': '',
            'full_address': '',
            # 'active': 'این آدرس دیفالت باشد؟'
        }

