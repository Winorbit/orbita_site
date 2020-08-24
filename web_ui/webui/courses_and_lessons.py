from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import json

from .forms import SignUpForm, LoginForm
from .import users
from . import endpoints
from . import sessions

import requests

from settings import logger


OK_CODES = (200, 201, 202, 203, 204, 205, 206)


def courses(request):
    user = users.session_user_info(request)
    res = requests.get(f"{endpoints.COURSES_ENDPOINT}")

    if res.status_code in OK_CODES:
        courses_data = res.json()['results']
        # logger.info(f'url:{endpoints.COURSES_ENDPOINT} - username:{user["username"]} - status_code:{res.status_code} - res:{res.json()}')
        return render(request, "webui/courses_and_lessons/courses.html",{'courses':courses_data, "user":user})
    else:
        logger.warning(f"url:{endpoints.COURSES_ENDPOINT} - get_data:{res.json()}")
        raise Exception(f"Some troubles with request - {res.status_code}")


def course_lesson(request, course_id, lesson_id):
    if users.session_user_info(request):
        try:
            res = requests.get(f'{endpoints.LESSONS_ENDPOINT}/{lesson_id}')
        except Exception as e:
            logging.exception(f"Exception occurred {endpoints.LESSONS_ENDPOINT}/{lesson_id}")
        lessons_response = res.json()
        return render(request, template_adresses.SINGLE_LESSON_PAGE, {'lesson_data':lessons_response})
    else:
        return HttpResponseRedirect("/enter") 


def single_course(request, id):
    if request.method == 'POST':
        user_id = request.session.get("user_id")
        user_courses = request.session.get("user_courses")
        if user_id :
            if 'subscribe' in request.POST:
                course_id = request.POST["subscribe"]
                user_courses.append(course_id)
                try:
                    req = requests.put(f'{endpoints.PROFILES_ENDPOINT}/{user_id}/', data={"user_courses":[course_id], "user": user_id})
                except Exception as e:
                    logging.exception(f"Exception occurred {endpoints.PROFILES_ENDPOINT}/{user_id}/")
                if req.status_code == 200:
                    request.session.modified = True
                    user = users.session_user_info(request)
                    try:
                        course_data = requests.get(f"{endpoints.SINGLE_COURSE_ENDPOINT}/{id}").json()
                    except Exception as e:
                        logging.exception(f"Exception occurred {endpoints.SINGLE_COURSE_ENDPOINT}/{id}/")
                    return HttpResponseRedirect(f"/courses/{course_id}/")
                else:
                    logger.warning(f"Some troubles with request {endpoints.PROFILES_ENDPOINT}/{user_id} - {req.status_code}")
                    raise Exception(f"Some troubles with request {endpoints.PROFILES_ENDPOINT}/{user_id} - {req.status_code}")

            if 'unsubscribe' in request.POST:
                course_id = request.POST["unsubscribe"]
                user_courses.remove(course_id)
                context = {"user_courses":user_courses, "user": user_id}
                try:
                    req = requests.put(f'{endpoints.PROFILES_ENDPOINT}/{user_id}/', data=context)
                except Exception as e:
                    logging.exception(f'url:{endpoints.PROFILES_ENDPOINT}/{user_id}/ - status_code:{req.status_code} - put_data:{context} - get_data:{req.json()}')
                if req.status_code == 200:
                    logger.info(f'url:{endpoints.PROFILES_ENDPOINT}/{user_id}/ - status_code:{req.status_code} - put_data:{context} - get_data:{req.json()}')
                    request.session.modified = True
                    user = users.session_user_info(request)
                    try:
                        course_data = requests.get(f"{endpoints.SINGLE_COURSE_ENDPOINT}/{id}").json()
                    except Exception as e:
                        logging.exception(f"Exception occurred {endpoints.SINGLE_COURSE_ENDPOINT}/{id}/")
                    return HttpResponseRedirect(f"/courses/{course_id}/")
                else:
                    raise Exception(f"Some troubles with request to {endpoints.PROFILES_ENDPOINT}/{user_id} - {req.status_code}")
            return render(request, template_adresses.SINGLE_COURSE_PAGE)
        else:
            logger.warning("Not found in request user and user_courses")
            raise Exception("Not found in request user and user_courses")


    if request.method == 'GET':
        if users.session_user_info(request):
            user_info = users.session_user_info(request)
        else:
            user_info = None
        try:
            res = requests.get(f"{endpoints.SINGLE_COURSE_ENDPOINT}/{id}")
        except Exception as e:
            logging.exception(f"Exception occurred {endpoints.SINGLE_COURSE_ENDPOINT}/{id}")
        course_data = res.json()
        return render(request, "webui/courses_and_lessons/single_course.html", {'course_data':course_data, "login_user":user_info})
        pass
