# users/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from users.models import Dealer_Info

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

class DealerInfoForm(forms.ModelForm):
    class Meta:
        model = Dealer_Info
        exclude =('date_of_registration', )

    def __init__(self, username):
        super(DealerInfoForm, self).__init__()
        self.fields['managed_by'].initial = username
        self.fields['unique_code'].initial = "NOT_ASSIGNED"
        self.fields['unique_code'].disabled = True
