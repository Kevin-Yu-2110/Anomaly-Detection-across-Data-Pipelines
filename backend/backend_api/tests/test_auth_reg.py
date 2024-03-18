from django.test import TestCase
from django.urls import reverse

class UserAuthenticationTests(TestCase):

    def test_user_registration(self):
        # user registration
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
        # duplicate registration
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
            HTTP_AUTHORIZATION=auth_token
        )
        self.assertFalse(response.json()['success'])
        # account deletion
        response = self.client.post(
            reverse('delete_account'),
            data={'username': 'newuser'},
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        self.assertTrue(response.json()['success'])

    def test_user_authentication(self):
        # register new user
        response = self.client.post(
            reverse('signup'),
            data={
                'username': 'newuser2',
                'email': 'newuser2@example.com',
                'password1': 'newpassword1234',
                'password2': 'newpassword1234',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        auth_token = data['token']
        # login already logged in user (no-effect)
        response = self.client.post(
            reverse('login'),
            data={
                'username': 'newuser2',
                'password': 'newpassword1234'
            },
            content_type='application/json',  
            HTTP_AUTHORIZATION=auth_token
        )
        data = response.json()
        self.assertTrue(data['success'])
        # delete user account
        response = self.client.post(
            reverse('delete_account'), 
            data={'username': 'newuser2'},
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        self.assertTrue(response.json()['success'])

    def test_invalid_login(self):
        # register new user and get session token
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'newuser3',
                'email': 'newuser2@example.com',
                'password1': 'newpassword12345',
                'password2': 'newpassword12345',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        # user login (wrong password)
        response = self.client.post(
            reverse('login'), 
            data={
            'username': 'newuser3',
            'password': 'newpasswrd12345'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertFalse(data['success'])
        # user login (username does not exist)
        response = self.client.post(
            reverse('login'), 
            data={
            'username': 'newuser1',
            'password': 'newpassword12345'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertFalse(data['success'])

    def test_user_logout(self):
        # register new user and get session token
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'newuser3',
                'email': 'newuser2@example.com',
                'password1': 'newpassword12345',
                'password2': 'newpassword12345',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        auth_token = data['token']
        # user logout
        response = self.client.post(
            reverse('logout'), 
            data={'username': 'newuser3'},
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        data = response.json()
        self.assertTrue(data['success'])
        # user login + get new session token
        response = self.client.post(
            reverse('login'), 
            data={
            'username': 'newuser3',
            'password': 'newpassword12345'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        auth_token = data['token']
        # user logout
        response = self.client.post(
            reverse('logout'), 
            data={'username': 'newuser3'},
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        data = response.json()
        self.assertTrue(data['success'])

    def test_unauthenticated_call(self):
        # register new user
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'SarahH184',
                'email': 'SarahHMonty@outlook.com',
                'password1': 'persephone_ajx4',
                'password2': 'persephone_ajx4',
                'accountType': 'business'
            },
            content_type='application/json'
        )
        data = response.json()
        auth_token = data['token']
        self.assertTrue(data['success'])
        # make api call without session token
        response = self.client.post(
            reverse('delete_account'),
            data={'username': 'SarahH184'},
            content_type='application/json',
        )
        data = response.json()
        self.assertFalse(data['success'])
        # make api call with session token
        response = self.client.post(
            reverse('delete_account'),
            data={'username': 'SarahH184'},
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        data = response.json()
        self.assertTrue(data['success'])

    def test_jwt_impersonation(self):
        # register new user
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Alice',
                'email': 'Alice814@gmail.com',
                'password1': 'SpringClean__324',
                'password2': 'SpringClean__324',
                'accountType': 'business'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Bob',
                'email': 'Bob2394@gmail.com',
                'password1': 'CleanSpring__391',
                'password2': 'CleanSpring__391',
                'accountType': 'business'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        # Bob attempts JWT impersonation attack
        bob_auth_token = data['token']
        response = self.client.post(
            reverse('delete_account'), 
            data={'username': 'Alice'},
            content_type='application/json',
            HTTP_AUTHORIZATION=bob_auth_token
        )
        data = response.json()
        self.assertFalse(data['success'])



