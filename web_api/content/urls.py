from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from content_app import  posts, users, courses

from rest_framework.routers import DefaultRouter

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'lessons', courses.LessonsList)
router.register(r'courses', courses.CoursesList)
router.register(r'posts', posts.PostsList)
router.register(r'users', users.UserList)
router.register(r'users_profiles', users.UserProfileClass)


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   # re_path(r'^users_profile/(?P<user_id>[0-9]+)/$', users.UserProfileClass.as_view()),
   path('search_user', users.search_user),
   path('remove_user_course', users.remove_user_course),

   re_path(r'^course/(?P<course_id>[-\w]+)/$', courses.course), 

   path("check_user", users.check_user),
   path("user_courses", users.user_courses),

   path("create_new_user", users.create_new_user),
   path("add_user_course", users.add_user_course),
   path("edit_user_profile", users.edit_user_profile),


   re_path(r'^', include(router.urls)),
   re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
