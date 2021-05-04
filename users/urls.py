# users/urls.py

from django.conf.urls import include, url
from users.views import dashboard, register, add_dealer, upload_user_headshot

urlpatterns = [
    # basic dashboard for everyone
    url(r"^dashboard/", dashboard, name="dashboard"),
    #  accounts page
    url(r"^accounts/", include("django.contrib.auth.urls")),
    # user registration
    url(r"^register/", register, name="register"),
    # add dealer info
    url(r"^add_dealer/", add_dealer, name="add_dealer"),
    # upload user headshot
    url(r"^upload_user_headshot/", upload_user_headshot, name="upload_user_headshot"),
]
