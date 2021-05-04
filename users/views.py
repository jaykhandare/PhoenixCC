# users/views.py

from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect, render
from random import randint
from datetime import date

from users.forms import UserForm
from users.models import Personal_Info

def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            user_obj.first_name = user_obj.first_name.capitalize()
            user_obj.last_name = user_obj.last_name.capitalize()

            username = user_obj.first_name.lower()[0] + user_obj.last_name.lower() + str(randint(1, 10000))
            user_obj.username = username
            user_details_obj = Personal_Info(username=username, date_of_birth=form.cleaned_data['date_of_birth'], 
                                pin_code=form.cleaned_data['pin_code'], address=form.cleaned_data['address'], 
                                city=form.cleaned_data['city'], email_verified=False, date_of_joining=date.today())
            try:
                user_obj.save()
                user_details_obj.save()
                print("{} : {} {} added".format(username, user_obj.first_name, user_obj.last_name))
            except Exception as e:
                return HttpResponseServerError()

            return redirect('dashboard')
            # ("Thanks for the registration. We'll get back to you soon.")
        else:
            return HttpResponseBadRequest()
    elif request.method == "GET":
        return render(request, "users/register.html", {"form": UserForm})