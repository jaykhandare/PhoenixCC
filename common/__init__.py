# common/__init__.py

from django.db import reset_queries
from django.http import response
from django.shortcuts import render

INTERNAL_ERROR_TEMPLATE = "internal_error.html"

# Singleton implementation for implementing Singleton Design Pattern
class SingletonMeta(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            instance = super().__call__(*args, **kwargs)
            cls.__instances[cls] = instance
        return cls.__instances[cls]


class UserSpecific(SingletonMeta):

    ALLOWED_POSITIONS = (
        ('director', 'director'),
        ('asst-director', 'asst-director'),
        ('hr-manager', 'hr-manager'),
        ('hr-exec', 'hr-exec'),
        ('hr-admin', 'hr-admin'),
        ('busi-dev-exec', 'busi-dev-exec'),
        ('sales-head', 'sales-head'),
        ('reg-manager', 'reg-manager'),
        ('state-manager', 'state-manager'),
        ('area-manager', 'area-manager'),
        ('tert-manager', 'tert-manager'), 
    )

    def get_user_level(self, position_string=None):
        for index in range(len(UserSpecific.ALLOWED_POSITIONS)):
            if UserSpecific.ALLOWED_POSITIONS[index][0] == position_string:
                return index
        return ValueError("{} : position not defined in the hierarchy. Please define it in common class".format(position_string))


def create_exception(request, function_name, exception, template=INTERNAL_ERROR_TEMPLATE, additional_data=None):
    response_string = "problem in {} : {} ".format(function_name, exception)
    if additional_data is not None:
        response_string += " => for value : {}".format(additional_data)
    exception_reply = {'exception' : response_string}

    return render(request, template, exception_reply)
