from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Account

#Registration Form to capture the details
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder': 'Enter your Password'
    }))

    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder': 'Confirm your Password'
    }))

    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']


    def clean(self):
            cleaned_data = super(RegistrationForm, self).clean()
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')

            if password != confirm_password:
                raise forms.ValidationError(
                    "Password does not match!"
                )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'