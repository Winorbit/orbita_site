import requests
import math
import uuid

from settings import logger, DEFAULT_MAIL_NAME
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

from .forms import SignUpForm, LoginForm, EditProfile, ChangePassForm, RestoreForm
from .endpoints import *
from .sessions import *

def index(request):
    return render(request, "webui/info/index.html")
# перенести в urls 


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
                logger.info(f"User id-{req.json()['id']} registration success")
                user = form.cleaned_data.get('username')
                messages.success(request, f'{user}, для тебя был создан аккаунт, авторизуйся')
                return redirect('/login')
            elif req.status_code == 409:
                messages.error(request, 'Такой пользователь уже существует')
                context = {'form': form}
                return render(request, "webui/users/signup.html", context)
    else:
        context = {'form': form}
        return render(request,"webui/users/signup.html", context)


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            check_user = requests.post(f"{CONTENT_URL}/search_userprofile", data = form.cleaned_data)
            logger.info(f'url:{CONTENT_URL}/search_user - status_code:{check_user.status_code} - put_data:{form.cleaned_data} - get_data:{check_user.json()}')
            if check_user.status_code == 200:
                logger.info(f"User id-{check_user.json()['id']} login success")
                write_into_session(request,**check_user.json())
                # то ли пишеться в сессию?
                return redirect('/my_cabinet')
            else:
                messages.info(request, 'Чет не то вводишь, человек.')
                context={}
                return render(request, "webui/users/login.html", context) 
    else:
        form = LoginForm()
        return render(request, "webui/users/login.html", {'form': form})
        pass


def user_logout(request):
    logout(request)
    return render(request, "webui/info/index.html")


def user_cabinet(request):
    username = request.session.get("username")
    user_id = request.session.get("user_id")
    if username and user_id:
        user_courses = request.session.get("user_courses")
        courses_req = requests.get(f"{SINGLE_COURSE_ENDPOINT}")
        if courses_req.status_code == 200:
            results = courses_req.json()["results"]
            available_courses = [x for x in results if x["id"] in user_courses]
            return render(request, "webui/users/user_cabinet.html", {'available_courses':available_courses})
        else:
            logger.warning(f"Request is failed with status {courses_req.status_code}")
            raise Exception(f"Request is failed with status {courses_req.status_code}")
    else:
        return redirect("/enter")
        pass
