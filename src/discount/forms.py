from django import forms


class CodeDiscountForm(forms.Form):
    code = forms.CharField()
