from django.test import TestCase
from django.urls import reverse

class UserAuthenticationTests(TestCase):

    def test_user_registration(self):
        # user registration
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'accountType': 'client'
        }, content_type='application/json')
        self.assertTrue(response.json()['success'])
        # duplicate registration
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'accountType': 'client'
        }, content_type='application/json')
        self.assertFalse(response.json()['success'])
        # account deletion
        response = self.client.post(reverse('delete_account'), {
            'username': 'newuser',
        }, content_type='application/json')
        self.assertTrue(response.json()['success'])

    def test_user_authentication(self):
        # register new user
        response = self.client.post(reverse('signup'), {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password1': 'newpassword1234',
            'password2': 'newpassword1234',
            'accountType': 'client'
        }, content_type='application/json')
        self.assertTrue(response.json()['success'])
        # login new user
        response = self.client.post(reverse('login'), {
            'username': 'newuser2',
            'password': 'newpassword1234'
        }, content_type='application/json')
        # delete new user account
        response = self.client.post(reverse('delete_account'), {
            'username': 'newuser2',
        }, content_type='application/json')
        self.assertTrue(response.json()['success'])
        # login non-existent user
        response = self.client.post(reverse('login'), {
            'username': 'newuser',
            'password': 'newpassword123'
        }, content_type='application/json')
        self.assertFalse(response.json()['success'])

    def test_user_logout(self):
        # register new user
        response = self.client.post(reverse('signup'), {
            'username': 'newuser3',
            'email': 'newuser2@example.com',
            'password1': 'newpassword12345',
            'password2': 'newpassword12345',
            'accountType': 'client'
        }, content_type='application/json')
        self.assertTrue(response.json()['success'])
        # login new user
        response = self.client.post(reverse('login'), {
            'username': 'newuser3',
            'password': 'newpassword12345'
        }, content_type='application/json')
        # logout new user
        response = self.client.post(reverse('logout'), {
            'username': 'newuser3'
        }, content_type='application/json')

