# users/views.py

from django.http.response import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage

from random import randint
from datetime import date

from users.forms import UserForm, DealerInfoForm
from users.models import Dealer_Info, Personal_Info
import django_tables2 as tables


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
                print("{} : {} {} added".format(
                    username, user_obj.first_name, user_obj.last_name))
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
        dealer_obj = Dealer_Info(first_name=data['first_name'], last_name=data['last_name'], pin_code=data['pin_code'], address=data['address'], city=data['city'],
                                 managed_by=data['managed_by'], date_of_registration=date.today(), pan_number=data['pan_number'], aadhar_number=data['aadhar_number'], unique_code='NOT_ASSIGNED')
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

        try:
            filename = fs.save(file_name, file)
        except Exception as e:
            print(e)
            return HttpResponseServerError
        else:
            return render(request, 'users/user_headshot_upload.html', {'uploaded_file_url': fs.url(filename)})

    elif request.method == "GET":
        if str(request.user) != "AnonymousUser":
            file_name = './users/' + str(request.user) + '.png'
            if fs.exists(file_name):
                return render(request, 'users/user_headshot_upload.html', {'uploaded_file_url': fs.url(file_name)})

        # user is AnonymousUser or doesn't have profilePic
        file_name = './users/profilePic.png'
        return render(request, 'users/user_headshot_upload.html', {'uploaded_file_url': fs.url(file_name)})

def get_my_dealers(request):
    class Dealer_Info_Table(tables.Table):
        class Meta:
            model = Dealer_Info

    if request.method == "GET":
        username = str(request.user)
        dealer_objs = Dealer_Info.objects.filter(managed_by=username)
        table = Dealer_Info_Table(dealer_objs)
        return render(request, 'users/dealers_under_user.html', {'table': table})
    elif request.method == "POST":
        return HttpResponseBadRequest()
    

def upload_dealer_docs(request):
    if request.method == "POST":

        fs = FileSystemStorage()
        dealer_code = request.POST.dict()['dealer_code']
        aadhar_card = request.FILES['aadhar_card']
        pan_card = request.FILES['pan_card']

        # save both the files correctly
        file_name_aadhar_card = './dealers/' + dealer_code + '/' + aadhar_card.name
        file_name_pan_card = './dealers/' + dealer_code + '/' + pan_card.name

        if fs.exists(file_name_aadhar_card):
            fs.delete(file_name_aadhar_card)
        f1 = fs.save(file_name_aadhar_card, aadhar_card)

        if fs.exists(file_name_pan_card):
            fs.delete(file_name_pan_card)
        f2 = fs.save(file_name_pan_card, pan_card)

        return render(request, 'users/dashboard.html')

    elif request.method == "GET":
        unique_code = request.GET.dict()['unique_code']
        dealer_obj = None
        try:
            dealer_obj = Dealer_Info.objects.get(unique_code=unique_code)
        except Exception as e:
            print(e)
            return HttpResponseServerError()
        if dealer_obj is not None:
            return render(request, 'users/add_dealer_docs.html', {'dealer': dealer_obj})
        else:
            return HttpResponseServerError()
