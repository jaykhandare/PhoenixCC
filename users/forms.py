# users/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    date_of_birth = forms.DateField()
    pin_code = forms.CharField(max_length=6)
    address = forms.CharField()
    city = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',
                  'date_of_birth', 'pin_code', 'address', 'city')
