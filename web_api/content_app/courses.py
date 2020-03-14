from content_app.models import Course, Lesson, UserProfile
from django.contrib.auth.models import User
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.decorators import action


from content_app.serializers import CourseSerializer, LessonSerializer

class LessonsList(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class CoursesList(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

@api_view(['GET'])
def course(request, course_id):
    course = Course.objects.get(id=course_id)
    course_lessons = Lesson.objects.filter(cours=course_id)
    serializer_lessons = LessonSerializer(course_lessons, many=True)
    course_serializer = CourseSerializer(course, many=False)

    dicta = {"lessons":serializer_lessons.data,
            "course": course_serializer.data}


    return Response(dicta, status=status.HTTP_202_ACCEPTED)
    pass

