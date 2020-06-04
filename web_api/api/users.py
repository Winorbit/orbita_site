from django.contrib.auth.models import User

from api.models import Course, UserProfile
from api.serializers import UserSerializer, UserProfileSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

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

class UserProfileClass(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
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
