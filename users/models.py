from django.db import models


class UserDetails(models.Model):
    username = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    pin_code = models.CharField(max_length=6)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    date_of_joining = models.DateField()
