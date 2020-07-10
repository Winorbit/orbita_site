from django.urls import include, path, re_path
from . import users, courses_and_lessons

app_name = "webui"

urlpatterns = [
    path('', users.index, name='index'),

    path('courses/', courses_and_lessons.courses),
    re_path(r'^courses/(?P<id>[-\w]+)/$', courses_and_lessons.single_course,  name="course"), 
    re_path(r'^restore_access', users.restore_access,  name="restore"), 
    re_path(r'^courses/(?P<course_id>[-\w]+)/lesson/(?P<lesson_id>[-\w]+)/$', courses_and_lessons.course_lesson,  name="course_lesson"), 

    path('my_cabinet/', users.user_cabinet),
    path('restore_access/', users.restore_access, name="restore_access"),
    path('change_password/<uuid:uuid>/<int:encoded_datetime>/<int:encoded_email>/<int:user_id>', users.change_pass,  name="change_pass"), 

    path('edit_profile', users.edit_profile),  # добавить по айдишке
    path('login/', users.login, name='login'),
    path('logout/', users.user_logout),

    re_path(r'^signup/$', users.signup, name='register'),
    
]

#   gro_bro78+egor
