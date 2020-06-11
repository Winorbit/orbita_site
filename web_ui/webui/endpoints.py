import os
PORT_API = os.environ.get('PORT_API')
HOST = "http://web-api"
PORT = PORT_API

try:
    from .local_endpoints import *
except ImportError:
    pass

# ENDPOINTS CONTENT ADRESSES

CONTENT_URL = f"{HOST}:{PORT}"
COURSES_ENDPOINT = f'{CONTENT_URL}/courses'
LESSONS_ENDPOINT = f"{CONTENT_URL}/lessons"
SINGLE_COURSE_ENDPOINT = f"{CONTENT_URL}/courses"

print('***SINGLE_COURSE_ENDPOINT', SINGLE_COURSE_ENDPOINT)


