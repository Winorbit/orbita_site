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

CREATE_NEW_USER_ENDPOINT = f"{CONTENT_URL}/create_new_user"
USER_PROFILES_ENDPOINT = f"{CONTENT_URL}/user_profiles"

GET_USER_ENDPOINT = f"{CONTENT_URL}/get_user"
GET_USER_PROFILE_ENDPOINT = f"{CONTENT_URL}/get_user_profile"

CHECK_USER_ENDPOINT = f"{CONTENT_URL}/check_user"
CHECK_USER_PROFILE_ENDPOINT = f"{CONTENT_URL}/check_user_profile"

EMAIL_EXIST_ENDPOINT = f"{CONTENT_URL}/email_exist"
NAME_EXIST_ENDPOINT = f"{CONTENT_URL}/name_exist"



EDIT_USER_PROFILE_ENDPOINT = f"{CONTENT_URL}/edit_user_profile"
USER_COURSES_ENDPOINT = f'{CONTENT_URL}/user_courses'
REMOVE_USER_COURSE_ENDPOINT = f"{CONTENT_URL}/remove_user_course"
ADD_USER_COURSE_ENDPOINT = f"{CONTENT_URL}/users_profiles"
COURSES_ENDPOINT = f'{CONTENT_URL}/courses'
LESSONS_ENDPOINT = f"{CONTENT_URL}/lessons"
POSTS_ENDPOINT = f"{CONTENT_URL}/posts"
SINGLE_COURSE_ENDPOINT = f"{CONTENT_URL}/course"



