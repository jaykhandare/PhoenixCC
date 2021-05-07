# users/urls.py

from django.conf.urls import include, url
from management.views import modify_user_details, show_all_users, show_all_dealers, modify_dealer_details, assign_unique_code

urlpatterns = [
    # show all users
    url(r"^show_all_users/", show_all_users, name="show_all_users"),
    # user details modification form
    url(r"^modify_user_details/", modify_user_details, name="modify_user_details"),

    # show all dealers
    url(r"^show_all_dealers/", show_all_dealers, name="show_all_dealers"),
    # modify dealer details
    url(r"^modify_dealer_details/", modify_dealer_details, name="modify_dealer_details"),
    # assign dealer unique_code
    url(r"^assign_unique_code/", assign_unique_code, name="assign_unique_code"),

]
