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
        })
        self.assertTrue(response.json()['success'])
        # duplicate registration
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'accountType': 'client'
        })
        self.assertFalse(response.json()['success'])
        # account deletion
        response = self.client.post(reverse('delete_account'), {
            'username': 'newuser',
        })
        print("THIS IS THE RESPONSE: ", response.json(), end="")
        self.assertTrue(response.json()['success'])

    def test_user_authentication(self):
        # register new user
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'accountType': 'client'
        })
        self.assertTrue(response.json()['success'])
        # login new user
        response = self.client.post(reverse('login'), {
            'username': 'newuser',
            'password': 'newpassword123'
        })
        # delete new user account
        response = self.client.post(reverse('delete_account'), {
            'username': 'newuser',
        })
        self.assertTrue(response.json()['success'])
        # login non-existent user
        response = self.client.post(reverse('login'), {
            'username': 'newuser',
            'password': 'newpassword123'
        })
        self.assertFalse(response.json()['success'])
