import requests

def write_into_session(request, **kwargs):
    user_name = kwargs.get('username')
    user_id = kwargs.get('id')
    user_courses = kwargs.get('user_courses')

    request.session["username"] = user_name
    request.session["user_id"] = user_id
    request.session["user_courses"] = user_courses
    request.session.modified = True
