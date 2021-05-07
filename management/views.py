# management/views.py

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import django_tables2 as tables
from users.models import Personal_Info, Dealer_Info
from management.forms import DealerDataUpdateForm, DealerUniqueCodeUpdateForm, UserDataUpdateForm
from common import create_exception

@login_required
def show_all_users(request):
    return show_tables(request=request, table_name='users')

@login_required
def show_all_dealers(request):
    return show_tables(request=request, table_name='dealers')

def show_tables(request, table_name=None):
    class User_Info_Table(tables.Table):
        class Meta:
            model = Personal_Info
    class Dealer_Info_Table(tables.Table):
        class Meta:
            model = Dealer_Info

    if table_name is None:
        return create_exception(request, __name__, exception="data no provided")

    res = create_exception(request, __name__, exception="unknown request method")

    if request.method == "GET":
        if table_name == 'dealers':
            all_objects = Dealer_Info.objects.all()
            table = Dealer_Info_Table(all_objects)
        elif table_name == 'users':
            all_objects = Personal_Info.objects.all()
            table = User_Info_Table(all_objects)
        res = render(request, 'show_table.html', {'table_type': table_name, 'table': table})

    elif request.method == "POST":
        res = create_exception(request, __name__, exception="POST method not implemented")

    return res

@login_required
def modify_dealer_details(request):
    res = create_exception(request, __name__, exception="unknown request method")

    if request.method == "POST":
        data_for_update = request.POST.dict()
        unique_code = data_for_update.get('unique_code', None)
        try:
            dealer_info_obj = Dealer_Info.objects.get(unique_code=unique_code)
        except Exception as e:
            print(e)
            res = create_exception(
                request, __name__, exception=e, additional_data=unique_code)
        else:
            dealer_info_obj.first_name = data_for_update['first_name']
            dealer_info_obj.last_name = data_for_update['last_name']
            dealer_info_obj.pin_code = data_for_update['pin_code']
            dealer_info_obj.address = data_for_update['address']
            dealer_info_obj.city = data_for_update['city']
            dealer_info_obj.pan_number = data_for_update['pan_number']
            dealer_info_obj.aadhar_number = data_for_update['aadhar_number']
            try:
                dealer_info_obj.save()
            except Exception as e:
                res = create_exception(request, __name__, exception=e)
            else:
                # direct return of show_all_users
                request.method = "GET"
                res = show_all_dealers(request)

    elif request.method == "GET":
        data = request.GET.dict()
        unique_code = data.get('unique_code', None)
        try:
            dealer_info_obj = Dealer_Info.objects.get(unique_code=unique_code)
        except Exception as e:
            print(e)
            res = create_exception(
                request, __name__, exception=e, additional_data=unique_code)
        else:
            dealer_details_context = {'first_name': dealer_info_obj.first_name, 'last_name': dealer_info_obj.last_name, 'pin_code': dealer_info_obj.pin_code, 'address': dealer_info_obj.address, 'city': dealer_info_obj.city, 'pan_number': dealer_info_obj.pan_number, 'aadhar_number': dealer_info_obj.aadhar_number, 'unique_code': dealer_info_obj.unique_code}
            form = DealerDataUpdateForm(dealer_details_context)
            res = render(request, "obj_details_modif.html", {'form': form, 'form_type': 'dealer'})

    return res


@login_required
def modify_user_details(request):
    res = create_exception(
        request, __name__, exception="unknown request method")

    if request.method == "POST":
        data_for_update = request.POST.dict()
        old_username = data_for_update.get('old_username', None)
        # retrieve User and Personal_Info from old_username and update them
        try:
            user_obj = User.objects.get(username=old_username)
            user_details_obj = Personal_Info.objects.get(username=old_username)
        except Exception as e:
            print(e)
            res = create_exception(request, __name__, exception=e)
        else:
            user_obj.username = data_for_update['username']
            user_details_obj.username = data_for_update['username']
            user_details_obj.date_of_joining = data_for_update['date_of_joining']
            user_details_obj.position = data_for_update['position']
            user_details_obj.direct_manager = data_for_update['direct_manager']

            try:
                user_obj.save()
                user_details_obj.save()
            except Exception as e:
                res = create_exception(request, __name__, exception=e)
            else:
                # direct return of show_all_users
                request.method = "GET"
                res = show_all_users(request)

    elif request.method == "GET":
        data = request.GET.dict()
        username = data.get('username', None)
        try:
            user_details_obj = Personal_Info.objects.get(username=username)
        except Exception as e:
            print(e)
            res = create_exception(
                request, __name__, exception=e, additional_data=username)
        else:
            user_details_context = {'username': user_details_obj.username, 'date_of_joining': user_details_obj.date_of_joining, 'position': user_details_obj.position,
                                    'direct_manager': user_details_obj.direct_manager, 'old_username': user_details_obj.username}
            form = UserDataUpdateForm(user_data=user_details_context)
            res = render(request, "obj_details_modif.html", {'form': form, 'form_type': 'user'})

    return res


@login_required
def assign_unique_code(request):
    res = create_exception(
        request, __name__, exception="unknown request method")

    if request.method == "POST":
        data_for_update = request.POST.dict()
        old_unique_code = data_for_update.get('old_unique_code', None)
        try:
            dealer_obj = Dealer_Info.objects.get(unique_code=old_unique_code)
        except Exception as e:
            print(e)
            res = create_exception(request, __name__, exception=e)
        else:
            dealer_obj.unique_code = data_for_update['unique_code']
            try:
                dealer_obj.save()
            except Exception as e:
                res = create_exception(request, __name__, exception=e)
            else:
                # direct return of show_all_users
                request.method = "GET"
                res = show_all_dealers(request)

    elif request.method == "GET":
        data = request.GET.dict()
        unique_code = data.get('unique_code', None)
        try:
            dealer_obj = Dealer_Info.objects.get(unique_code=unique_code)
        except Exception as e:
            print(e)
            res = create_exception(
                request, __name__, exception=e, additional_data=unique_code)
        else:
            form = DealerUniqueCodeUpdateForm(old_unique_code=unique_code)
            res = render(request, "obj_details_modif.html", {'form': form, 'form_type': 'dealer'})

    return res