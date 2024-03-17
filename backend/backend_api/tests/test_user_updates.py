from django.test import TestCase
from django.urls import reverse

class UserUpdateTests(TestCase):

    def test_update_username_email(self):
        # register a user
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'newpassword123',
                'password2': 'newpassword123',
                'accountType': 'client'
            },
            content_type='application/json',
        )
        data = response.json()
        self.assertTrue(data['success'])
        auth_token = data['token']
        # request username update
        response = self.client.post(
            reverse('update_username'), 
            data={
                'username': 'newuser',
                'new_username': 'updated_user'
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        data = response.json()
        self.assertTrue(data['success'])
        new_auth_token = data['token']
        # check that new auth token works for email update request
        response = self.client.post(
            reverse('update_email'),
            data={
                'username': 'updated_user',
                'new_email': 'updated_user@example.com'
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=new_auth_token
        )
        data = response.json()
        self.assertTrue(data['success'])
        # check that old auth token doesn't for email update request
        response = self.client.post(
            reverse('update_email'),
            data={
                'username': 'updated_user',
                'new_email': 'newuser@example.com'
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        data = response.json()
        self.assertFalse(data['success'])