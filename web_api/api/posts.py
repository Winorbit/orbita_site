from api.models import Post
from api.serializers import PostSerializer

from rest_framework import viewsets

class PostsList(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



