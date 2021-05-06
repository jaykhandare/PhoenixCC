# management/forms.py

from django import forms
from django.forms.widgets import HiddenInput

position_allowed = (('director', 'director'), ('asst-director', 'asst-director'), ('hr-manager', 'hr-manager'), ('hr-exec', 'hr-exec'), ('hr-admin', 'hr-admin'), ('busi-dev-exec', 'busi-dev-exec'), ('sales-head', 'sales-head'), ('reg-manager', 'reg-manager'), ('state-manager', 'state-manager'), ('area-manager', 'area-manager'), ('tert-manager', 'tert-manager'), )

class UserDataUpdateForm(forms.Form):
    old_username = forms.CharField(max_length=20, widget=HiddenInput)
    username = forms.CharField(max_length=20)
    date_of_joining = forms.DateField()
    position = forms.ChoiceField(choices=position_allowed)
    direct_manager = forms.CharField(max_length=20)
    level = forms.IntegerField()

    def __init__(self, user_data):
        super(UserDataUpdateForm, self).__init__()
        for item in self.fields.keys():
            self.fields[item].initial = user_data[item]
