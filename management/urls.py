# users/urls.py

from django.conf.urls import include, url
from management.views import assign_user_details

urlpatterns = [
    # user details modification form
    url(r"^assign_user_details/", assign_user_details, name="assign_user_details"),
]
