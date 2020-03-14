import requests
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm, EditProfile

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
    # response = requests.get('http://0.0.0.0:8000/')
    # response = requests.get('http://0.0.0.0:8000')
    # response = requests.get('http://webapi:8000/lessons',verify=False)


    return render(request, template_adresses.INDEX_PAGE)
    pass

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():


            user_name = form.cleaned_data.get('username')
            user_pass = form.cleaned_data.get('password1')
            user_mail = form.cleaned_data.get('email')

            data = {'username': user_name, "password":user_pass, "email":user_mail}
            print(endpoints.CREATE_NEW_USER_ENDPOINT)


            req = requests.post(endpoints.CREATE_NEW_USER_ENDPOINT, data=data)


            if req.status_code == 202:
                return HttpResponseRedirect("/my_cabinet")
            else:
                print(req.status_code)
                return HttpResponseRedirect("/error_page")          
    else:
        if not common_funcs.check_user_exist(request):
            form = SignUpForm()
            return render(request, template_adresses.SIGNUP_PAGE, {'form': form})
        else:
            return HttpResponseRedirect("/my_cabinet")
            pass

def login(request):
    #  12gor-mor
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            user_pass = form.cleaned_data.get('password')

            form_data = {'username': user_name, "password":user_pass}

            check_user = requests.post(endpoints.CHECK_USER_PROFILE_ENDPOINT, data = form_data)
            if check_user.status_code == 202:
                user_data  = requests.post(endpoints.GET_USER_PROFILE_ENDPOINT, data = form_data)


                form_data.update(user_data.json())

                common_funcs.write_into_session(request,**form_data)
                return HttpResponseRedirect("/my_cabinet")
            else:
                return HttpResponseRedirect("/enter")
        return HttpResponseRedirect('/')
          
    else:
        form = LoginForm()
        return render(request, template_adresses.LOGIN_PAGE, {'form': form})
        pass

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def user_cabinet(request):
    if common_funcs.check_user_profile_exist(request):
        username = request.session.get("username")
        user_id = request.session.get("user_id")
        data={"username": username,  "user_id": user_id}

        # response = requests.post(endpoints.USER_COURSES_ENDPOINT, data={"username": username,  "user_id": user_id})
        res = common_funcs.send_to_content(endpoints.USER_COURSES_ENDPOINT, data )
        available_courses = res.json()

        return render(request, template_adresses.USER_CABINET_PAGE,{'available_courses':available_courses})
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
            print(form.errors)
            return HttpResponseRedirect('/')
          
    else:
        if common_funcs.check_user_profile_exist(request):
            form = EditProfile()
            return render(request, template_adresses.LOGIN_PAGE, {'form': form})
        else:
            return HttpResponseRedirect("/enter")
            pass
            

        