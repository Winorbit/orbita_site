from content_app.models import Course, Lesson, Post, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpRequest, HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from content_app.serializers import CourseSerializer, LessonSerializer, PostSerializer, UserSerializer, UserProfileSerializer

import json


class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password1")

        serializer = UserSerializer(data={"username":username, "email":email, "password":password})
        if serializer.is_valid():
            serializer.save()
            new_user = User.objects.get(email=email, username=username)
            new_user_profile = UserProfile.objects.create(user=new_user, id = new_user.id, user_courses = [])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_409_CONFLICT)
        


@api_view(['POST'])
def search_user(request):
    user_name = request.data.get("username")
    password = request.data.get("password")
    if User.objects.filter(password=password, username=user_name).exists():
        user = User.objects.get(password=password, username=user_name)
        user_profile = UserProfile.objects.get(user=user)
        data = {**UserSerializer(user).data, **UserProfileSerializer(user_profile).data}
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


class UserProfileClass(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


def search_user_profile(**kwargs):
    # ВОТ ТУТ ЧЕКНУТЬ ПРАВИЛЬНУЮ ПРОВЕРКУ АРГУМЕНТОВ
    if kwargs.get("username") and kwargs.get("user_id"):
        test_user_data = {"username":kwargs.get("username")[0], "user_id":kwargs.get("user_id")[0]}
        if User.objects.filter(**test_user_data).exists():
            user = User.objects.get(**test_user_data)
            if user.is_active:
                if user.is_authenticated:
                    return UserProfile.objects.get(user=user)
                else:
                    print("***USer not auth")
            else:
                print("***USer not active")
        else:
            print("***USER NOT EXIST")
            return False
    else:
        print("***Incoming args not correct")


@api_view(['PUT'])
def add_user_course(request):
    course_id = request.data["course_id"]
    profile_on_update = search_user_profile(**request.data)
    if course_id not in profile_on_update.user_courses:
        profile_on_update.user_courses.append(course_id)
        profile_on_update.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        print("PROBLEM")


@api_view(['DELETE'])
def remove_user_course(request):
    course_id = request.data["course_id"]
    profile_on_update = search_user_profile(**request.data)

    if course_id in profile_on_update.user_courses:
        profile_on_update.user_courses.remove(course_id)
        profile_on_update.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response("PASKUDA")


@api_view(['POST'])
def check_user(request):
    data = request.data
    user_profile = search_user_profile(**data)
    if user_profile:
        user_info = {"user_id": user_profile.id,
                    "user_courses":user_profile.user_courses}

        return Response(user_info, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)
        pass


@api_view(['POST'])
def user_courses(request):
    user_profile = search_user_profile(**request.data)
    if user_profile:
        available_courses = []
        for course_id in user_profile.user_courses:
            course = Course.objects.get(id = course_id)
            available_courses.append({"name":course.title , "id":course_id})
    
    return Response(available_courses, status=status.HTTP_202_ACCEPTED)
    pass


@api_view(['PUT'])
def edit_user_profile(request):
    data = request.data
    user_profile = search_user_profile(**data)

    if user_profile:
        user = User.objects.get(pk = user_profile.user.id)

        new_name = data.dict()["new_name"]
        new_pass = data.dict()["new_pass"]
        new_email = data.dict()["new_email"]

        if user.username != new_name:
            user.username = new_name

        if user.password != new_pass:
            user.password = new_pass

        if user.email != new_email:
            user.email = new_email

        user.save()

        return Response(status=status.HTTP_201_CREATED)

    else:
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    # если олд пароль  = пароль
    # - сменить пассворд на нью пассворд
    # - если никнейм != олд нэйм - сменить

    # ретурн ОК


# def edit_profile(request):


# SELECT creation_datetime, stage_by_datetime, service_window_start, cutoff_datetime at time zone 'pst' at time zone 'utc' FROM public.orders WHERE order_id ='12128525';

# SELECT creation_datetime, stage_by_datetime, service_window_start, cutoff_datetime FROM public.orders WHERE order_id ='12128525';

# SELECT creation_datetime, cutoff_datetime, stage_by_datetime,service_window_start FROM public.orders WHERE order_id IN ('12171911','12127980','12128758','12119508','12128542','12128525', '12128551');
