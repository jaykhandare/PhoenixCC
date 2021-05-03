# users/views.py

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from random import randint
from datetime import date

from users.forms import UserForm
from users.models import UserDetails


def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            user_obj.first_name = user_obj.first_name.capitalize()
            user_obj.last_name = user_obj.last_name.capitalize()

            for _ in range(10):
                username = str(randint(1, 10000))
                try:
                    user_obj.username = username
                    user_obj.save()
                except:
                    pass
                else:
                    user_details_obj = UserDetails(username=username, date_of_birth=form.cleaned_data['date_of_birth'], 
                                                   pin_code=form.cleaned_data['pin_code'], address=form.cleaned_data['address'], 
                                                   city=form.cleaned_data['city'], email_verified=False, date_of_joining=date.today(), all_clear_status=False)
                    user_details_obj.save()
                    return HttpResponse("Thanks for the registration. We'll get back to you soon.")

            return HttpResponse("You are extremely unlucky. Try again.")
        else:
            return HttpResponseBadRequest()
    elif request.method == "GET":
        return render(request, "users/register.html", {"form": UserForm})

def verify_email(request):
    pass