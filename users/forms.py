# users/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.layout import Submit
from common import get_helper

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = get_helper()
        self.helper.form_id = 'id-registerForm'
        self.helper.add_input(Submit('submit', 'Submit'))

    def get_helper(self):
        return self.helper


class DealerInfoForm(forms.ModelForm):
    class Meta:
        model = Dealer_Info
        exclude =('date_of_registration', )

    def __init__(self, username):
        super(DealerInfoForm, self).__init__()
        self.fields['managed_by'].initial = username
        self.fields['unique_code'].initial = "NOT_ASSIGNED"
        self.fields['unique_code'].disabled = True

        self.helper = get_helper()
        self.helper.form_id = 'id-registerForm'
        self.helper.add_input(Submit('submit', 'Submit'))

    def get_helper(self):
        return self.helper
