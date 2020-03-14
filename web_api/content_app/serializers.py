from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from content_app.models import Course, Lesson, Post, UserProfile

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
   class Meta:
        model = User
        fields = ('email', 'username', 'password', )

