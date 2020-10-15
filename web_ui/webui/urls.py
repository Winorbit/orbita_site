from django.urls import include, path, re_path
from . import users, courses_and_lessons

app_name = "webui"

urlpatterns = [
    path('', users.index, name='index'),

    path('courses/', courses_and_lessons.courses),
    re_path(r'^courses/(?P<id>[-\w]+)/$', courses_and_lessons.single_course,  name="course"), 
    re_path(r'^courses/(?P<course_id>[-\w]+)/lesson/(?P<lesson_id>[-\w]+)/$', courses_and_lessons.course_lesson,  name="course_lesson"), 

    path('my_cabinet/', users.user_cabinet),

    path('login/', users.login, name='login'),
    path('logout/', users.user_logout),

    re_path(r'^signup/$', users.signup, name='register'),
]
