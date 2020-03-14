import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField

COURSES_TYPE = (("free", "free"),("premium","premium"), ("authorized", "authorized"))
COURSE_STATUSES = (( "in_queue", "in_queue"), ("started", "started"), ("finished", "finished"))
LESSON_STATUSES = COURSE_STATUSES[1:2]

class BaseTextModel(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=250, blank=False, default="hh")
	description = models.CharField(max_length=2500, default = 'f', blank=True)
	content = models.TextField(blank=False, default='f')
	pass

class Course(BaseTextModel):
	course_type = models.CharField(max_length = 20, choices=COURSES_TYPE, db_index=True, default = COURSES_TYPE[0], verbose_name='course type - free or premium')
	pass

class Lesson(BaseTextModel):
	cours = models.ForeignKey(Course, related_name='course_for_lesson', on_delete=models.CASCADE)
	pass

class Post(BaseTextModel):
 	pass

class UserProfile(models.Model):
    profile_image = models.ImageField(upload_to="user_pics", blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_courses = ArrayField(models.CharField(max_length=36,))

