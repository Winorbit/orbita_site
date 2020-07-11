import requests
import math
import uuid
from settings import DEFAULT_MAIL_NAME
from datetime import datetime

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib import messages

from .forms import SignUpForm, LoginForm, EditProfile, ChangePassForm, RestoreForm
from webui.endpoints import *
from webui.sessions import *

max_diff = 86400

def index(request):
    return render(request, "info/index.html")
    pass

def session_user_info(request):
    if request.session.get("username") and request.session.get("user_id"):
        user_info = {"username": request.session.get("username"), 
                     "user_id": request.session.get("user_id"),
                     "user_courses": request.session.get("user_courses"),}
        return user_info
    else:
        return None
        pass

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            req = requests.post(f"{USERS_ENDPOINT}/", data=form.cleaned_data)
            if req.status_code == 201:
                user = form.cleaned_data.get('username')
                messages.success(request, f'{user}, для тебя был создан аккаунт, авторизуйся')
                return redirect('/login')
            elif req.status_code == 409:
                messages.error(request, 'Такой пользователь уже существует')
                context = {'form': form}
                return render(request, "users/register.html", context)
    else:
        context = {'form': form}
        return render(request,"users/register.html", context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            check_user = requests.post(f"{CONTENT_URL}/search_user", data = form.cleaned_data)
            if check_user.status_code == 200:
                write_into_session(request,**check_user.json())
                return HttpResponseRedirect('/my_cabinet')
            else:
                messages.info(request, 'Чет не то вводишь, человек.')
                context={}
                return render(request, "users/login.html", context) 
    else:
        form = LoginForm()
        return render(request, "users/login.html", {'form': form})
        pass

def user_logout(request):
    logout(request)
    return render(request, "info/index.html")

def user_cabinet(request):
    username = request.session.get("username")
    user_id = request.session.get("user_id")
    if username and user_id:
        user_courses = request.session.get("user_courses")
        courses_req = requests.get(f"{SINGLE_COURSE_ENDPOINT}")
        if courses_req.status_code == 200:
            available_courses = [x for x in courses_req.json() if x["id"] in user_courses]
            return render(request, "users/user_cabinet.html", {'available_courses':available_courses})
        else:
            raise Exception(f"Request is failed with status {courses_req.status_code}")
    else:
        return HttpResponseRedirect("/enter")
        pass

def edit_profile(request):
    if request.method == 'POST':
        session_info = session_user_info(request) 
        if session_user_info:
            form = EditProfile(data=request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                user_req = requests.get(f"{USERS_ENDPOINT}/{session_info['user_id']}")
                if user_req.status_code == 200:
                    user_info = user_req.json()
                else:
                    raise Exception(f"Request is failed with status {user_req.status_code}")
                
                if form_data:

                    if form_data["new_password"] and form_data["old_password"]:
                        new_pass = form_data["new_password"]
                        form_curent_pass = form_data["old_password"]
                    
                        if new_pass != user_info["password"]:
                            user_info["password"] = new_pass
                        else:
                            raise Exception("NEW PASSWORD IS EQUAL WITH CURRENT")
                    
                    if form_data["new_name"]:
                        new_name = form_data['new_name']
                        if new_name != user_info["username"]:
                            user_info["username"] = new_name
                        else:
                            raise Exception("NEW NAME IS EQUAL CURRENT NAME")
                    
                    if form_data["new_email"]:
                        new_email = form_data["new_email"]
                        if new_email != user_info["email"]:
                            user_info["email"] = new_email
                        else:
                            raise Exception("Email is equal!")
                else:
                    raise Exception("FORM IS EMPTY!!!!")
                
                upd_res = requests.put(f"{USERS_ENDPOINT}/{session_info['user_id']}/", data=user_info)
               
                if upd_res.status_code == 200:
                    user = requests.get(f"{USERS_ENDPOINT}/{session_info['user_id']}")
                    if request.session["username"] != user.json()["username"]:
                        request.session["username"] = user.json()["username"]
                        request.session.modified = True
                
                return HttpResponseRedirect('/my_cabinet')
            else:
                return HttpResponseRedirect('/error')
        else:
            return HttpResponseRedirect('/')
    else:
        if session_user_info(request): 
            form = EditProfile()
            return render(request, "users/edit_profile.html", {'form': form})
        else:
            return HttpResponseRedirect("/enter")
            pass

def encode_str_to_number(input_str):
    return int.from_bytes(input_str.encode(), 'little')
    pass

def decode_number_to_str(input_number):
    return input_number.to_bytes(math.ceil(input_number.bit_length() / 8), 'little').decode()
    pass

def generate_restore_link(datetime:int, user_email:str, user_id:int):
    encoded_datetime = encode_str_to_number(str(datetime))
    encoded_email = encode_str_to_number(user_email)
    uuid_token = str(uuid.uuid4())
    restore_link = f"{CONTENT_URL}/change_password/{uuid_token}/{encoded_datetime}/{encoded_email}/{user_id}"
    return restore_link
    pass

def check_expire(datetime_now:int, datetime:int):
    delta = datetime_now - datetime
    if delta > max_diff:
        result = False
    if delta == max_diff:
        result = False
    if delta < max_diff:
        result = True
    if delta <= 0:
        raise Exception("SOME WRONG WUTH DELTA",  time_from_token, datetime_now, delta)
    return result
    pass

RESTORE_ACCESS_EMAIL_TEMPLATE = "Вы можете востанвиь доступ к сайту, перейдя о следующей ссылке: {}. Ссылка будет действительна в течении 24 часов."

def email_for_restore_access(datetime:str,user_email:str, user_id:int):
    restore_link = generate_restore_link(datetime, user_email, user_id) 
    message_text = RESTORE_ACCESS_EMAIL_TEMPLATE.format(restore_link)
    return message_text
    pass

def send_restore_message(email_address, email_text):
    try:
        res = send_mail("Password restore", email_text, DEFAULT_MAIL_NAME, [email_address], fail_silently=False)
    except Exception as e:
        raise Exception(f"Problem with sending email - {e}")
    if res == 1:
        return True
    else:
        raise Exception("Some problems with sending email")

def restore_access(request):
    if request.method == 'POST':
        form = RestoreForm(data=request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            user_email = form_data["user_email"]
            res_user_by_email = requests.post("{CONTENT_URL}/search_user_by_email", data={"email": user_email})
            if res_user_by_email.status_code == 200:
                user = res_user_by_email.json()
                user_id = user["id"]
            else:
                raise Exception(f"Request to get user was gailed with status {res.user_by_email.status_code}")
            now_in_secs = int(datetime.now().strftime("%s"))
            email_text = email_for_restore_access(now_in_secs, user_email, user_id)
            send_restore_message(user_email, email_text)
            return render(request, "restore_message_sent.html")
        else:
            raise Exception("Email not sent")
    else:
        form = RestoreForm()
        context = {'access_form': form}
        return render(request,"users/restore_pass.html", context)
        pass
 
def change_pass(request, uuid, encoded_datetime, encoded_email, user_id):
    link = request.path
    link_elements =  link.split("/")
    if request.method == 'POST':
        form = ChangePassForm(data=request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            new_pass = form_data["new_pass"]
            repeated_new_pass = form_data["repeat_new_pass"]
            if new_pass != repeated_new_pass:
                raise Exception("Passes not equal, please, try again!")
        else:
            raise Exception("Some troubles with vkaid form")
        
        restore_request_datetime = decode_number_to_str(int(link_elements[3])) 
        restore_request_email = decode_number_to_str(int(link_elements[4]))
        user_id = int(link_elements[5])
        now_in_secs = int(datetime.now().strftime("%s"))
        
        if check_expire(now_in_secs, int(restore_request_datetime)):
            res_user = requests.get(f"{USERS_ENDPOINT}/{user_id}")
            if res_user.status_code == 200:
                user_info = res_user.json()
                if "email" in user_info.keys():
                    data = {"username": user_info["username"], "password": new_pass}
                    upd_res = requests.put(f"{USERS_ENDPOINT}/{user_id}/", data=data)
                    if upd_res.status_code == 200:
                        return redirect("/login") 
                    else:
                        raise Exception(f"Updating user was failed - status {upd_res.status_code}")
                else:    
                    raise Exception(f"Some troubles with user - field email not in user")
            else:
                raise Exception(f"problem with request to web_api - request status is {res_status_code}")
        else:
            return render(request, "token_expired.html")
    else:
        form = ChangePassForm()
        context = {'restore_form': form, "encoded_datetime":encoded_datetime, "encoded_email":encoded_email, "user_id":user_id,"uuid":uuid}
        return render(request,"users/change_pass.html", context)
        pass
