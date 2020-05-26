import requests
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm, EditProfile

from django.contrib import messages

from . import endpoints
from . import template_adresses
from . import common_funcs


def user_info(request):
    if common_funcs.check_user_profile_exist(request):
        user_info = {"username": request.session.get("username"), 
                     "user_id": request.session.get("user_id"),
                     "user_courses": request.session.get("user_courses"),}
        return user_info
    else:
        return None
        pass


def enter(request):
    if common_funcs.check_user_profile_exist(request):
        return HttpResponseRedirect("/")
    else:
        return render(request, template_adresses.ENTER_PAGE)
    pass


def index(request):
    return render(request, template_adresses.INDEX_PAGE)
    pass


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        # print('***form', data)
        if form.is_valid():
            req = requests.post("http://127.0.0.1:8000/users/", data=form.cleaned_data)
            if req.status_code == 201:
                user = form.cleaned_data.get('username')
                messages.success(request, f'{user}, для тебя был создан аккаунт, наслождайся =)')
                return redirect("/login")
            elif req.status_code == 409:
                print('***error409')
                messages.error(request, 'Такой пользователь уже существует')
                context={}
                return render(request, template_adresses.SIGNUP_PAGE, context)
        return render(request, template_adresses.SIGNUP_PAGE, {'form': form})          
    else:
        if not common_funcs.check_user_exist(request):
            form = SignUpForm()
            return render(request, template_adresses.SIGNUP_PAGE, {'form': form})
        else:
            return HttpResponseRedirect("/my_cabinet")
            pass


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            check_user = requests.post("http://127.0.0.1:8000/search_user", data = form.cleaned_data)
            if check_user.status_code == 200:
                common_funcs.write_into_session(request,**check_user.json())
                return HttpResponseRedirect('/my_cabinet')
            else:
                messages.info(request, 'Чет не то вводишь, человек.')
                # form = LoginForm(request.POST)
                # return render(request, template_adresses.LOGIN_PAGE, {'form': form, 'danger': True})
        context={}
        return render(request, template_adresses.LOGIN_PAGE, context) 
    else:
        form = LoginForm()
        return render(request, template_adresses.LOGIN_PAGE, {'form': form})
        pass


def user_logout(request):
    logout(request)
    return render(request, template_adresses.INDEX_PAGE)

 
def user_cabinet(request):
    username = request.session.get("username")
    userprofile_id = request.session.get("userprofile_id")
    if username and userprofile_id:
        user_courses = request.session.get("user_courses")
        return render(request, template_adresses.USER_CABINET_PAGE, {'available_courses':user_courses})
    else:
        return HttpResponseRedirect("/enter")
        pass


def edit_profile(request):
    if request.method == 'POST':
        if common_funcs.check_user_profile_exist(request):
            form = EditProfile(data=request.POST)
            if form.is_valid():
                form_data = form.cleaned_data
                updated_profile_info = {}
                current_profile_info = {}
                current_name = request.session.get("username")
                if form_data:
                    if form_data["new_password"] and form_data["old_password"]:
                        new_pass = form_data["new_password"]
                        form_curent_pass = form_data["old_password"]
                        if new_pass == form_curent_pass:
                            raise Exception("NEW PASSWORD IS EQUAL WITH CURRENT")
                        else:
                            updated_profile_info["password"] = new_pass
                            current_profile_info["password"] = form_curent_pass 
                    if form_data["username"]:
                        form_new_name = form.cleaned_data.get('username')
                        if form_new_name == current_name:
                            raise Exception("NEW NAME IS EQUAL CURRENT NAME")
                        else:
                            updated_profile_info["username"] = form_new_name
                            current_profile_info["username"] = current_name
                    if form_data["email"]:
                        new_email = form_data["email"]
                        updated_profile_info["email"] = new_email
                else:
                    raise Exception("FORM IS EMPTY!!!!")
                data_on_update = {"current_user_info": current_profile_info, "new_user_info": updated_profile_info}
                req = requests.put(endpoints.EDIT_USER_PROFILE_ENDPOINT, json=data_on_update)
                if req.status_code == 201:
                    if form_data["username"]:
                        request.session["username"] = form_new_name
                return HttpResponseRedirect('/my_cabinet')
            else:
                return HttpResponseRedirect('/error')
        else:
            return HttpResponseRedirect('/')
    else:
        if common_funcs.check_user_profile_exist(request):
            form = EditProfile()
            return render(request, template_adresses.LOGIN_PAGE, {'form': form})
        else:
            return HttpResponseRedirect("/enter")
            pass
            

        