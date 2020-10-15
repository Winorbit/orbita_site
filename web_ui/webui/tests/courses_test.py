import os
from django.test import TestCase
from django.test import Client

from ..courses_and_lessons import courses

os.environ["PORT_API"] = "8009"
os.environ["API_HOST"] = "localhost"

c = Client()

res = c.get('/courses/')

# print(res.__dict__)
print(res)
