from . import endpoints
from . import template_adresses
import requests
import json

from django.http import HttpResponseRedirect
from dataclasses import dataclass

# USER - NAMED TUPLE

# ИСПОЛЬЗОВАТЬ ТУТ PARTIAL - доп. параметр - локация
@dataclass
class User:
    username: str
    user_id: str

def get_user_from_request(request):
    username = request.session.get("username")
    user_id = request.session.get("user_id")
    if username and user_id:
        user = User(username, user_id)
    else:
        user = None 
    return user
    pass

def send_to_content(endpoint:str, data:dict):
    try: 
        req = requests.post(endpoint, data=data)
    except Exception as e:
        raise(e)
    return req
    pass

def check_user_exist(request):
    user = get_user_from_request(request)
    if user:
        user_data={"username": user.username,  "user_id": user.user_id}
        res = send_to_content(endpoints.CHECK_USER_PROFILE_ENDPOINT, user_data)
        if res.status_code == 202:
            return True
    else:
        return False
        pass

def check_user_profile_exist(request):
    user = get_user_from_request(request)
    if user:
        user_data = {"username": user.username,  "user_id": user.user_id}
        res = send_to_content(endpoints.CHECK_USER_PROFILE_ENDPOINT, user_data)
        if res.status_code == 202:
            return True
    else:
        return False
        pass

# def check_user_profie_exist(request):
#     user = get_user_from_request(request)
#     if user:
#         req = requests.post(endpoints.EDIT_USER_PROFILE_ENDPOINT, data={"username": user.username,  "user_id": user.user_id})
#         if req.status_code == 202:
#             return True
#     else:
#         return False
#         pass






def check_user_email_is_free():
    pass

def check_username_is_free():
    pass

def get_user_profile():
    pass

def get_user():
    pass

def redirect_to_main():
    return HttpResponseRedirect("/")

# def user_info(request):
#     if common_funcs.check_user_exist(request):
#         user_info = {"username": request.session.get("username"), 
#                      "user_id": request.session.get("user_id"),
#                      "user_courses": request.session.get("user_courses"),}
#         return user_info
#     else:
#         return None
#         pass



def write_into_session(request, **kwargs):
    user_name = kwargs.get('username')
    user_id = kwargs.get('user_id')
    user_courses = kwargs.get('user_courses')

    request.session["username"] = user_name
    request.session["user_id"] = user_id
    request.session["user_courses"] = user_courses
    request.session.modified = True


# get_user_profile
# get_user
# check_name_if_free
# check_email_is_free

# def check_user_exist():
#     return binary try\false



# check_user_profile_exist

# def throw(message:str):
#     raise Exception(message)