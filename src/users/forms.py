from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Address, City, Customer, Province
from django import forms


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
    active = forms.BooleanField(widget=forms.HiddenInput(), initial=True)

    class Meta:
        model = Address
        fields = ['province', 'city', 'postal_code', 'full_address', 'active']
        labels = {
            'city': 'شهر',
            'province': 'استان',
            'postal_code': 'کد پستی',
            'full_address': 'آدرس کامل',
            # 'active': 'این آدرس دیفالت باشد؟'
        }

    def __init__(self, *args, **kwargs):
        """ use init method to access request for using messages """
        self.request = kwargs.pop('request', None)
        super(AddressForm, self).__init__(*args, **kwargs)

    def clean_postal_code(self):
        """ check length of postal code to be 10 digits """
        super(AddressForm, self).clean()
        postal_code = self.cleaned_data.get('postal_code')
        if len(str(postal_code)) != 10:
            messages.error(request=self.request, message='لطفا کد پستی 10 زقمی خود را وارد کنید')
            self._errors['postal_code'] = self.error_class(['کد پستی اشتباه است'])
        return postal_code
