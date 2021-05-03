# users/urls.py

from django.conf.urls import include, url
from users.views import dashboard, register

urlpatterns = [
    # basic dashboard for everyone
    url(r"^dashboard/", dashboard, name="dashboard"),
    #  accounts page
    url(r"^accounts/", include("django.contrib.auth.urls")),
    # user registration
    url(r"^register/", register, name="register"),
]
