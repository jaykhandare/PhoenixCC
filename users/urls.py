# users/urls.py

from django.conf.urls import include, url
from users.views import dashboard

urlpatterns = [
    # basic dashboard for everyone
    url(r"^dashboard/", dashboard, name="dashboard"),
    #  accounts page
    url(r"^accounts/", include("django.contrib.auth.urls")),
]