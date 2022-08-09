import json

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import  status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

import secrets

userModel = get_user_model()

class UserTestCase(APITestCase):
    '''
    CLass testing Users
    '''
    def setUp(self):
        '''
        Init data in users db
        '''
        self.superuser = userModel.objects.create_superuser(username='superuser', email='superuser@email.com', password='superuser')
        self.staffuser = userModel.objects.create_user(username='staffuser', email='staffuser@email.com', password='staffuser', is_staff=True)
        self.normaluser = userModel.objects.create_user(username='normaluser', email='normaluser@email.com', password='normaluser')
        self.normaluser1 = userModel.objects.create_user(username='normaluser1', email='normaluser1@email.com', password='normaluser1')
        
    def test_login(self):
        '''
        Ensure we can login.
        '''
        url = reverse('login')
        data = {
            "username" : "staffuser",
            "password" : "staffuser"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)     
        self.assertEqual(response.json()['user']['email'], 'staffuser@email.com')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + response.json()['token'])
    
    def test_user_registration(self):
        '''
        Ensure we can create a new user.
        '''
        data = {
            'username' : 'test',
            'email' : 'test@email.com',
            'first_name' : 'Test',
            'last_name' : 'User',
            'password' : secrets.token_urlsafe(10), # create ramdon pass
        }