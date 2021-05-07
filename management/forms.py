# management/forms.py

from django import forms
from django.forms.widgets import HiddenInput

from common import UserSpecific

class UserDataUpdateForm(forms.Form):
    old_username = forms.CharField(max_length=20, widget=HiddenInput)
    username = forms.CharField(max_length=20)
    date_of_joining = forms.DateField()
    position = forms.ChoiceField(choices=UserSpecific.ALLOWED_POSITIONS)
    direct_manager = forms.CharField(max_length=20)

    def __init__(self, user_data):
        super(UserDataUpdateForm, self).__init__()
        for item in self.fields.keys():
            self.fields[item].initial = user_data[item]

class DealerDataUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    pin_code = forms.CharField(max_length=6)
    address = forms.CharField(max_length=30)
    city = forms.CharField(max_length=15)
    pan_number = forms.CharField(max_length=11)
    aadhar_number = forms.CharField(max_length=20)
    unique_code = forms.CharField(max_length=15, widget=HiddenInput)

    def __init__(self, dealer_data):
        super(DealerDataUpdateForm, self).__init__()
        for item in self.fields.keys():
            self.fields[item].initial = dealer_data[item]


class DealerUniqueCodeUpdateForm(forms.Form):
    old_unique_code = forms.CharField(max_length=15, widget=HiddenInput)
    unique_code = forms.CharField(max_length=15)

    def __init__(self, old_unique_code):
        super(DealerUniqueCodeUpdateForm, self).__init__()
        self.fields['old_unique_code'].initial = old_unique_code

