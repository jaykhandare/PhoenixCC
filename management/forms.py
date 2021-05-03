# management/forms.py

from django import forms
from django.forms.widgets import HiddenInput


class UserData_MngtForm(forms.Form):
    old_username = forms.CharField(max_length=20, widget=HiddenInput)
    username = forms.CharField(max_length=20)
    date_of_joining = forms.DateField()
    position = forms.CharField(max_length=15)
    direct_manager = forms.CharField(max_length=20)
    level = forms.IntegerField()

    def __init__(self, user_data):
        super(UserData_MngtForm, self).__init__()
        for item in self.fields.keys():
            self.fields[item].initial = user_data[item]
