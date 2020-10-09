from django.test import TestCase
from rest_framework.test import APIClient
from .. import users 
from django.contrib.auth.models import User

class UsersTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        user_1 = User.objects.create(username= "User", password = 'TOPSECRET', email="user_num@gmail.com")
        user_profile_1 = users.UserProfile.objects.create(user=user_1, id=user_1.id, user_courses=[])

    def test_search_user(self):
        userprofile_resp = {'email': 'user_num@gmail.com',
                            'first_name': '',
                            'groups': [],
                            'id': 1,
                            'is_active': True,
                            'is_staff': False,
                            'is_superuser': False,
                            'last_login': None,
                            'last_name': '',
                            'password': 'TOPSECRET',
                            'profile_image': None,
                            'user': 1,
                            'user_courses': [],
                            'user_permissions': [],
                            'username': 'User'}
       
        response = self.client.post("/search_userprofile", {"username": "User", "password": "TOPSECRET"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue( all(item in response.data.items() for item in userprofile_resp.items()))


        response = self.client.post("/search_userprofile", {"username": "user_num@gmail.com", "password": "TOPSECRET"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue( all(item in response.data.items() for item in userprofile_resp.items()))

        response = self.client.post("/search_userprofile", {"username": "User", "password": ""})
        self.assertEqual(response.status_code, 401)
        
        response = self.client.post("/search_userprofile", {"username": "User"})
        self.assertEqual(response.status_code, 401)
        
        response = self.client.post("/search_userprofile")
        self.assertEqual(response.status_code, 400)
