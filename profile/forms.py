import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model



User = get_user_model()


class SignUpForm(forms.ModelForm):
    password = forms.CharField(label="", widget=forms.TextInput(attrs={
        'type': 'password',
        'placeholder': 'رمز عبور'
    }))

    password2 = forms.CharField(label="", widget=forms.TextInput(attrs={
        'type': 'password',
        'placeholder': 'تکرار رمز عبور'
    }))

    phone_number = forms.CharField(label="", max_length=11, min_length=11,
        widget=forms.TextInput(attrs={
            'placeholder': 'شماره موبایل'
        })
    )

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'password2']

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2



class LoginForm(forms.Form):
    phone_number = forms.CharField(label="", max_length=11, min_length=11,
        widget=forms.TextInput(attrs={
            'placeholder': 'شماره موبایل'
        })
    )

    password = forms.CharField(label="", widget=forms.TextInput(attrs={
        'type': 'password',
        'placeholder': 'رمز عبور'
    }))
