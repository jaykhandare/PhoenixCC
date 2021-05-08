# users/views.py

from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from random import randint
from datetime import date
import django_tables2 as tables

from users.forms import UserForm, DealerInfoForm
from users.models import Dealer_Info, Personal_Info
from common import create_exception


def dashboard(request):
    return render(request, "users/dashboard.html")


def register(request):
    res = create_exception(
        request, __name__, exception="unknown request method")

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            user_obj.first_name = user_obj.first_name.capitalize()
            user_obj.last_name = user_obj.last_name.capitalize()

            username = user_obj.first_name.lower(
            )[0] + user_obj.last_name.lower() + str(randint(1, 10000))
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
                print(e)
                res = create_exception(request, __name__, exception=e)
            else:
                res = redirect('dashboard')
        else:
            res = create_exception(request, __name__, str(
                ValueError("form data in request not valid")))
    elif request.method == "GET":
        empty_form = UserForm()
        res = render(request, "users/register.html", {"form": empty_form, "helper": empty_form.get_helper()})

    return res

@login_required
def add_dealer(request):
    res = create_exception(
        request, __name__, exception="unknown request method")
    if request.method == "POST":
        data = request.POST.dict()
        dealer_obj = Dealer_Info(first_name=data['first_name'], last_name=data['last_name'], pin_code=data['pin_code'], address=data['address'], city=data['city'],
                                 managed_by=data['managed_by'], date_of_registration=date.today(), pan_number=data['pan_number'], aadhar_number=data['aadhar_number'], unique_code='NOT_ASSIGNED')
        try:
            dealer_obj.save()
        except Exception as e:
            print(e)
            res = create_exception(request, __name__, exception=e)
        else:
            res = redirect('dashboard')
    elif request.method == "GET":
        empty_form = DealerInfoForm(username=request.user)
        res = render(request, "users/add_dealer.html",
                     {"form": empty_form, "helper": empty_form.get_helper()})

    return res


@login_required
def upload_user_headshot(request):
    res = create_exception(
        request, __name__, exception="unknown request method")
    fs = FileSystemStorage()
    if request.method == "POST": 
        if request.FILES['profile_picture']:
            file = request.FILES['profile_picture']
            file_name = './users/' + \
                str(request.user) + '.' + file.name.split('.')[-1]

            if fs.exists(file_name):
                fs.delete(file_name)

            try:
                filename = fs.save(file_name, file)
            except Exception as e:
                print(e)
                res = create_exception(request, __name__, exception=e)
            else:
                res = render(request, 'users/user_headshot_upload.html',
                            {'uploaded_file_url': fs.url(filename)})
        else:
            res = create_exception(request, __name__, exception="no file uploaded")

    elif request.method == "GET":
        if str(request.user) != "AnonymousUser":
            file_name = './users/' + str(request.user) + '.png'
            if fs.exists(file_name):
                res = render(request, 'users/user_headshot_upload.html',
                             {'uploaded_file_url': fs.url(file_name)})
        # user is AnonymousUser or doesn't have profilePic
        file_name = './users/profilePic.png'
        res = render(request, 'users/user_headshot_upload.html',
                     {'uploaded_file_url': fs.url(file_name)})

    return res


@login_required
def get_my_dealers(request):
    res = create_exception(
        request, __name__, exception="unknown request method")

    class Dealer_Info_Table(tables.Table):
        class Meta:
            model = Dealer_Info

    if request.method == "GET":
        username = str(request.user)
        dealer_objs = Dealer_Info.objects.filter(managed_by=username)
        table = Dealer_Info_Table(dealer_objs)
        res = render(request, 'users/dealers_under_user.html',
                     {'table': table})
    elif request.method == "POST":
        res = create_exception(
            request, __name__, exception="POST method not implemented")

    return res


@login_required
def upload_dealer_docs(request):
    res = create_exception(
        request, __name__, exception="unknown request method")
    if request.method == "POST":
        fs = FileSystemStorage()
        unique_code = request.POST.dict()['unique_code']
        aadhar_card = request.FILES['aadhar_card']
        pan_card = request.FILES['pan_card']

        # save both the files correctly
        file_name_aadhar_card = './dealers/' + unique_code + '/' + aadhar_card.name
        file_name_pan_card = './dealers/' + unique_code + '/' + pan_card.name

        if fs.exists(file_name_aadhar_card):
            fs.delete(file_name_aadhar_card)
        fs.save(file_name_aadhar_card, aadhar_card)

        if fs.exists(file_name_pan_card):
            fs.delete(file_name_pan_card)
        fs.save(file_name_pan_card, pan_card)

        res = render(request, 'users/dashboard.html')

    elif request.method == "GET":
        unique_code = request.GET.dict()['unique_code']
        dealer_obj = None
        try:
            dealer_obj = Dealer_Info.objects.get(unique_code=unique_code)
        except Exception as e:
            print(e)
            res = create_exception(request, __name__, exception=e)
        if dealer_obj is not None:
            res = render(request, 'users/add_dealer_docs.html',
                         {'dealer': dealer_obj})
        else:
            res = create_exception(
                request, __name__, exception="dealer with unique_code({}) not found".format(unique_code))

    return res
