from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .forms import SignUpForm, LoginForm
from .import users
from . import endpoints
from . import sessions

import requests

def courses(request):
    user = users.session_user_info(request)
    response = requests.get(endpoints.COURSES_ENDPOINT)
    courses_data = response.json()
    return render(request, "courses_and_lessons/courses.html",{'courses':courses_data, "user":user})
    pass

def course_lesson(request, course_id, lesson_id):
    if users.session_user_info(request):
        response = requests.get(f'{endpoints.LESSONS_ENDPOINT}/{lesson_id}')
        lessons_response = response.json()
        return render(request, template_adresses.SINGLE_LESSON_PAGE, {'lesson_data':lessons_response})
    else:
        return HttpResponseRedirect("/enter") 

def single_course(request, id):
    if request.method == 'POST':
        user_id = request.session.get("user_id")
        user_courses = request.session.get("user_courses")
        if user_id :    
            if 'submit' in request.POST:
                course_id = request.POST["submit"]
                user_courses.append(course_id)
                req = requests.put(f'{endpoints.PROFILES_ENDPOINT}/{user_id}/', data={"user_courses":[course_id], "user": user_id})
                if req.status_code == 200:
                    request.session.modified = True
                    user = users.session_user_info(request)
                    course_data = requests.get(f"{endpoints.SINGLE_COURSE_ENDPOINT}/{id}").json()
                    return HttpResponseRedirect(f"/courses/{course_id}/")
                else:
                    raise Exception(f"Some troubles with request {endpoints.PROFILES_ENDPOINT}/{user_id}- {req.status_code}")

            if 'leave' in request.POST:
                course_id = request.POST["leave"]
                user_courses.remove(course_id)
                req = requests.put(f'{endpoints.PROFILES_ENDPOINT}/{user_id}/', data={"user_courses":user_courses, "user": user_id})
                if req.status_code == 200:
                    request.session.modified = True
                    user = users.session_user_info(request)
                    course_data = requests.get(f"{endpoints.SINGLE_COURSE_ENDPOINT}/{id}").json()
                    return HttpResponseRedirect(f"/courses/{course_id}/")
                else:

                    raise Exception(f"Some troubles with request to {endpoints.PROFILES_ENDPOINT}/{user_id} - {req.status_code}")
            return render(request, template_adresses.SINGLE_COURSE_PAGE)
        else:
            raise Exception("Not found in request user and user_courses")

    if request.method == 'GET':
        if users.session_user_info(request):
            user = users.session_user_info(request)
        else:
            user = None
        response = requests.get(f"{endpoints.SINGLE_COURSE_ENDPOINT}/{id}")
        course_data = response.json()
        return render(request, "courses_and_lessons/single_course.html", {'course_data':course_data, "user_info":user})
        pass
