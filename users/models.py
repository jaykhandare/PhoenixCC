from django.db import models


class UserDetails(models.Model):
    username = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    pin_code = models.CharField(max_length=6)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=15)
    date_of_joining = models.DateField()
    position = models.CharField(max_length=15)
    direct_manager = models.CharField(max_length=20)
    level = models.IntegerField(default=-1)
    email_verified = models.BooleanField()
