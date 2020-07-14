import os
PORT = os.environ.get('PORT_API')
HOST = os.environ.get('API_HOST')

try:
    from . local_endpoints import *
except ImportError:
    pass

CONTENT_URL = f"{HOST}:{PORT}"
COURSES_ENDPOINT = f'{CONTENT_URL}/courses'
LESSONS_ENDPOINT = f"{CONTENT_URL}/lessons"
SINGLE_COURSE_ENDPOINT = f"{CONTENT_URL}/courses"
USERS_ENDPOINT = f"{CONTENT_URL}/users"
PROFILES_ENDPOINT = f"{CONTENT_URL}/users_profiles"

