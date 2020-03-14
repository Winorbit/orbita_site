from content_app.models import Post
from django.http import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets

from content_app.serializers import PostSerializer

class PostsList(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



