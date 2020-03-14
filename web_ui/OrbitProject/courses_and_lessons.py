import requests
import json
import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm
from .import users
from . import endpoints
from . import template_adresses
from . import common_funcs

def courses(request):
    user = users.user_info(request)

    # if user:
    #     pass
        # ВАШИ КУРСЫ
    response = requests.get(endpoints.COURSES_ENDPOINT)
    courses_data = response.json()
    return render(request, template_adresses.COURSES_PAGE,{'courses':courses_data, "user":user})
    pass

def course_lesson(request, course_id, lesson_id):
    if users.user_info(request):
        response = requests.get(f'{endpoints.LESSONS_ENDPOINT}/{lesson_id}')
        lessons_response = response.json()
        return render(request, template_adresses.SINGLE_LESSON_PAGE, {'lesson_data':lessons_response})
    else:
        return HttpResponseRedirect("/enter") 

def single_course(request, id):
    if request.method == 'POST':
        if 'submit' in request.POST:
            if common_funcs.check_user_exist(request):
                username = request.session.get("username")
                user_id = request.session.get("user_id")
                course_id = request.POST["submit"]
                req = requests.put(endpoints.ADD_USER_COURSE_ENDPOINT, data={"course_id":course_id,"username": username,  "user_id": user_id})
                if req.status_code == 201:
                    request.session["user_courses"].append(course_id)
                    request.session.modified = True

        if 'leave' in request.POST:
            if common_funcs.check_user_exist(request):
                username = request.session.get("username")
                user_id = request.session.get("user_id")
                course_id = request.POST["leave"]
                req = requests.delete(endpoints.REMOVE_USER_COURSE_ENDPOINT, data={"course_id":course_id,"username": username,  "user_id": user_id})
                if req.status_code == 204:
                    request.session["user_courses"].remove(course_id)
                    request.session.modified = True
        return render(request, template_adresses.SINGLE_COURSE_PAGE)

    if request.method == 'GET':
        if users.user_info(request):
            user = users.user_info(request)
        else:
            user = None
        response = requests.get(f"{endpoints.SINGLE_COURSE_ENDPOINT}/{id}")
        course_data = response.json()
        return render(request, template_adresses.SINGLE_COURSE_PAGE, {'course_data':course_data, "user_info":user})
        pass