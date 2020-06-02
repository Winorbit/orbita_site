from django.urls import include, path, re_path
from . import users, posts, courses_and_lessons
# from django.contrib.auth import views as auth_views

app_name = "OrbitProject"

urlpatterns = [
    path('', users.index, name='index'),

    path('courses/', courses_and_lessons.courses),
    re_path(r'^courses/(?P<id>[-\w]+)/$', courses_and_lessons.single_course,  name="course"), 
    re_path(r'^courses/(?P<course_id>[-\w]+)/lesson/(?P<lesson_id>[-\w]+)/$', courses_and_lessons.course_lesson,  name="course_lesson"), 

    path('blog/', posts.posts),
    re_path(r'^blog/(?P<id>[-\w]+)/$', posts.single_post, name="blog_post"), 

    path('my_cabinet/', users.user_cabinet),
    path('edit_profile', users.edit_profile),  # добавить по айдишке
    path('login/', users.login, name='login'),
    path('logout/', users.user_logout),
    path('enter/', users.enter),

    re_path(r'^signup/$', users.signup, name='register'),
    
]

#   gro_bro78+egor