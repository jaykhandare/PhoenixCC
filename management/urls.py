# users/urls.py

from django.conf.urls import include, url
from management.views import assign_user_details, show_all_users

urlpatterns = [
    # user details modification form
    url(r"^assign_user_details/", assign_user_details, name="assign_user_details"),
    # show all users
    url(r"^show_all_users/", show_all_users, name="show_all_users"),

]
