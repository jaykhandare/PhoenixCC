# users/models.py

from django.db import models


class Personal_Info(models.Model):
    username = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    pin_code = models.CharField(max_length=6)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=15)
    date_of_joining = models.DateField(auto_now_add=True)
    position = models.CharField(max_length=15)
    direct_manager = models.CharField(max_length=20)
    email_verified = models.BooleanField()

class Dealer_Info(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    pin_code = models.CharField(max_length=6)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=15)
    managed_by = models.CharField(max_length=20)
    date_of_registration = models.DateField(auto_now_add=True)
    pan_number = models.CharField(max_length=11)
    aadhar_number = models.CharField(max_length=20)
    unique_code = models.CharField(max_length=15, default="NOT_ASSIGNED")
