from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .forms import SignUpForm, LoginForm
from .import users
from . import endpoints
from . import sessions

import requests

def courses(request):
    user = users.user_info(request)
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
                user_id = request.session.get("user_id")
                user_courses = request.session.get("user_courses")
                
                course_id = request.POST["submit"]
                user_courses.append(course_id)
                req = requests.put(f'{endpoints.ADD_USER_COURSE_ENDPOINT}/{user_id}/', data={"user_courses":user_courses, "user": user_id})
                if req.status_code == 200:
                    request.session.modified = True

                    user = users.user_info(request)
                    course_data = requests.get(f"{endpoints.SINGLE_COURSE_ENDPOINT}/{id}").json()
                    return render(request, template_adresses.SINGLE_COURSE_PAGE, {'course_data':course_data, "user_info":user})

        if 'leave' in request.POST:
            if common_funcs.check_user_exist(request):
                user_id = request.session.get("user_id")
                user_courses = request.session.get("user_courses")

                course_id = request.POST["leave"]
                user_courses.remove(course_id)
                req = requests.put(f'{endpoints.ADD_USER_COURSE_ENDPOINT}/{user_id}/', data={"user_courses":user_courses, "user": user_id})
                if req.status_code == 200:
                    request.session.modified = True

                    user = users.user_info(request)
                    course_data = requests.get(f"{endpoints.SINGLE_COURSE_ENDPOINT}/{id}").json()
                    return render(request, template_adresses.SINGLE_COURSE_PAGE, {'course_data':course_data, "user_info":user})
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