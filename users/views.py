# users/views.py

from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage

from random import randint
from datetime import date

from users.forms import UserForm, DealerInfoForm
from users.models import Dealer_Info, Personal_Info

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
                                city=form.cleaned_data['city'], email_verified=False)
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

def add_dealer(request):
    if request.method == "POST":
        data = request.POST.dict()
        dealer_obj = Dealer_Info(first_name=data['first_name'], last_name=data['last_name'], pin_code=data['pin_code'], address=data['address'], city=data['city'], managed_by=data['managed_by'], date_of_registration=date.today(), pan_number=data['pan_number'], aadhar_number=data['aadhar_number'], unique_code='NOT_ASSIGNED')
        try:
            dealer_obj.save()
        except Exception as e:
            print(e)
            return HttpResponseServerError()
        else:
            return redirect('dashboard')
    elif request.method == "GET":
        return render(request, "users/add_dealer.html", {"form": DealerInfoForm(username=request.user)})


def upload_user_headshot(request):
    fs = FileSystemStorage()
    if request.method == "POST" and request.FILES['profile_picture']:
        file = request.FILES['profile_picture']
        file_name = './users/' + str(request.user) + '.' + file.name.split('.')[-1]

        if fs.exists(file_name):
            fs.delete(file_name)
        filename = fs.save(file_name, file)
        uploaded_file_url = fs.url(filename)
        return render(request, 'users/user_headshot_upload.html', {'uploaded_file_url' : uploaded_file_url})
    
    elif request.method == "GET":
        if str(request.user) != "AnonymousUser":
            file_name = './users/' + str(request.user) + '.png'
            if fs.exists(file_name):
                return render(request, 'users/user_headshot_upload.html', {'uploaded_file_url' : fs.url(file_name)})
        
        # user is AnonymousUser or doesn't have profilePic
        file_name = './users/profilePic.png'
        return render(request, 'users/user_headshot_upload.html', {'uploaded_file_url' : fs.url(file_name)})

def upload_dealer_doc(request):
    pass