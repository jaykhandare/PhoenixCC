from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from users.models import Personal_Info
from management.forms import UserData_MngtForm


def assign_user_details(request):
    if request.method == "POST":
        data_for_update = request.POST.dict()
        old_username = data_for_update['old_username']
        
        # retrieve user and Personal_Info from old_username and update them
        user_obj = User.objects.get(username=old_username)        
        user_obj.username = data_for_update['username']
        user_obj.save()

        user_details_obj = Personal_Info.objects.get(username=old_username)
        user_details_obj.username = data_for_update['username']
        user_details_obj.date_of_joining = data_for_update['date_of_joining']
        user_details_obj.position = data_for_update['position']
        user_details_obj.direct_manager = data_for_update['direct_manager']
        user_details_obj.level = data_for_update['level']
        user_details_obj.save()
        
        return HttpResponse("Okay")

    elif request.method == "GET":
        username = request.GET.dict()['username']
        user_details_obj = Personal_Info.objects.get(username=username)
        user_details_context = {'username': user_details_obj.username, 'date_of_joining': user_details_obj.date_of_joining, 'position': user_details_obj.position,
                                'direct_manager': user_details_obj.direct_manager, 'level': user_details_obj.level, 'old_username': user_details_obj.username}
        form = UserData_MngtForm(user_data=user_details_context)

        return render(request, "user_details_modif.html", {'form': form})


def show_all_users(request):
    pass


def view_customer_info(request):
    pass