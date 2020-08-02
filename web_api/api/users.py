from django.contrib.auth.models import User

from api.models import Course, UserProfile
from api.serializers import UserSerializer, UserProfileSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

from settings import logging
logger = logging.getLogger(__name__)

class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer

    def create(self, request):
        if all(value != None for value in request.data.values()):
            email = request.data.get("email")
            username = request.data.get("username")
            password = request.data.get("password") or request.data.get("password1")
            logging.info(f"TRYING SERIALIZE NEW USER: {request.data}")

            serializer = UserSerializer(data={"username":username, "email":email, "password":password}) 
            if serializer.is_valid():
                serializer.save()
                logging.info(f"NEW USER CREATED: {serializer.data} ")
                new_user = User.objects.get(email=email, username=username)
                if UserProfile.objects.create(user=new_user, id = new_user.id, user_courses = []):
                    logger.info(f"USER PROFILE WAS CREATED - {new_user.id}")
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"NEW USER WAS NOT CREATED {serializer.data} BECAUSE OF {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            logger.error(f"NEW USER WAS NOT CREATED - SOME EMPTY INPUT FIELDS: {request.data}")
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        
class UserProfileClass(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('-id')
    serializer_class = UserProfileSerializer

@api_view(['POST'])
def search_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    if User.objects.filter(password=password, username=username).exists():
        user = User.objects.get(password=password, username=username)
        user_profile = UserProfile.objects.get(user=user)
        data = {**UserSerializer(user).data, **UserProfileSerializer(user_profile).data}

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def search_user_by_email(request):
    email = request.data.get("email")

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        data = {**UserSerializer(user).data}

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
