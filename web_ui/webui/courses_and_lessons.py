from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import logging

from .forms import SignUpForm, LoginForm
from .import users
from . import endpoints
from . import sessions

import requests


logging.basicConfig(level='DEBUG', filename='weblog.log', format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger()

OK_CODES = (200, 201, 202, 203, 204, 205, 206)


def courses(request):
    user = users.session_user_info(request)
    res = requests.get(f"{endpoints.COURSES_ENDPOINT}")

    if res.status_code in OK_CODES:
        courses_data = res.json()['results']
        return render(request, "webui/courses_and_lessons/courses.html",{'courses':courses_data, "user":user})
    else:
        raise Exception(f"Some troubles with request - {res.status_code}")
        logger.warning(f"Some troubles with request - {res.status_code}")

def course_lesson(request, course_id, lesson_id):
    if users.session_user_info(request):
        try:
            res = requests.get(f'{endpoints.LESSONS_ENDPOINT}/{lesson_id}')
        except Exception as e:
            logger.warning(f"Some troubles with request '{endpoints.LESSONS_ENDPOINT}/{lesson_id}' - {e}")
        lessons_response = res.json()
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
                try:
                    req = requests.put(f'{endpoints.PROFILES_ENDPOINT}/{user_id}/', data={"user_courses":[course_id], "user": user_id})
                except Exception as e:
                    logger.warning(f"Some troubles with request '{endpoints.PROFILES_ENDPOINT}/{user_id}/' - {e}")
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
                try:
                    req = requests.put(f'{endpoints.PROFILES_ENDPOINT}/{user_id}/', data={"user_courses":user_courses, "user": user_id})
                except Exception as e:
                    logger.warning(f"Some troubles with request '{endpoints.PROFILES_ENDPOINT}/{user_id}/' - {e}")
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
            logger.info("Not found in request user and user_courses")

    if request.method == 'GET':
        if users.session_user_info(request):
            user = users.session_user_info(request)
        else:
            user = None
        try:
            res = requests.get(f"{endpoints.SINGLE_COURSE_ENDPOINT}/{id}")
        except Exception as e:
            logger.warning(f"Some troubles with request '{endpoints.SINGLE_COURSE_ENDPOINT}/{id}' - {e}")
        course_data = res.json()
        return render(request, "webui/courses_and_lessons/single_course.html", {'course_data':course_data, "user_info":user})
        pass
