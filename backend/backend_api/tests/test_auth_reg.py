from django.test import TestCase
from django.urls import reverse

class UserAuthenticationTests(TestCase):

    def test_user_registration(self):
        # user registration
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Joseph_493',
                'email': 'Joseph_493@gmail.com',
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'newpassword123',
                'password2': 'newpassword123',
            },
        )
        data = response.json()
        self.assertTrue(data['success'])
        auth_token = data['token']
        # duplicate registration
        response = self.client.post(
            reverse('signup'),
            data={
                'username': 'Joseph_493',
                'email': 'Joseph_493@gmail.com',
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'newpassword123',
                'password2': 'newpassword123',
            }
        )
        self.assertFalse(response.json()['success'])
        # account deletion
        response = self.client.post(
            reverse('delete_account'),
            data={'username': 'Joseph_493'},
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
        )
        self.assertTrue(response.json()['success'])

    def test_user_authentication(self):
        # register new user
        response = self.client.post(
            reverse('signup'),
            data={
                'username': 'newuser2',
                'email': 'newuser2@example.com',
                'city': 'North Wilkesboro',
                'job': 'Applications Developer',
                'dob': '1983-04-21',
                'password1': 'newpassword1234',
                'password2': 'newpassword1234',
            }
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
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        # delete user account
        response = self.client.post(
            reverse('delete_account'), 
            data={'username': 'newuser2'},
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
        )
        self.assertTrue(response.json()['success'])

    def test_invalid_login(self):
        # register new user and get session token
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'newuser3',
                'email': 'newuser2@example.com',
                'city': 'North Wilkesboro',
                'job': 'Applications Developer',
                'dob': '1983-04-21',
                'password1': 'newpassword12345',
                'password2': 'newpassword12345',
            },
        )
        # user login (wrong password)
        response = self.client.post(
            reverse('login'), 
            data={
            'username': 'newuser3',
            'password': 'newpasswrd12345'
            }
        )
        data = response.json()
        self.assertFalse(data['success'])
        # user login (username does not exist)
        response = self.client.post(
            reverse('login'), 
            data={
            'username': 'newuser1',
            'password': 'newpassword12345'
            }
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
                'city': 'West Green',
                'job': 'Building surveyor',
                'dob': '1995-07-26',
                'password1': 'newpassword12345',
                'password2': 'newpassword12345',
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        auth_token = data['token']
        # user logout
        response = self.client.post(
            reverse('logout'), 
            data={'username': 'newuser3'},
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        # user login + get new session token
        response = self.client.post(
            reverse('login'), 
            data={
                'username': 'newuser3',
                'password': 'newpassword12345'
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        auth_token = data['token']
        # user logout
        response = self.client.post(
            reverse('logout'), 
            data={'username': 'newuser3'},
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
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
                'city': 'Mulberry Grove',
                'job': 'Broadcast journalist',
                'dob': '1983-04-21',
                'password1': 'persephone_ajx4',
                'password2': 'persephone_ajx4',
            }
        )
        data = response.json()
        auth_token = data['token']
        self.assertTrue(data['success'])
        # make api call without session token
        response = self.client.post(
            reverse('delete_account'),
            data={'username': 'SarahH184'},
        )
        data = response.json()
        self.assertFalse(data['success'])
        # make api call with session token
        response = self.client.post(
            reverse('delete_account'),
            data={'username': 'SarahH184'},
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
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
                'city': 'Mulberry Grove',
                'job': 'Broadcast journalist',
                'dob': '1983-04-21',
                'password1': 'SpringClean__324',
                'password2': 'SpringClean__324',
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Bob',
                'email': 'Bob2394@gmail.com',
                'city': 'Oaks',
                'job': 'Chemist, analytical',
                'dob': '1975-06-17',
                'password1': 'CleanSpring__391',
                'password2': 'CleanSpring__391',
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        # Bob attempts JWT impersonation attack
        bob_auth_token = data['token']
        response = self.client.post(
            reverse('delete_account'), 
            data={'username': 'Alice'},
            headers={
                'Authorization': f"Bearer {bob_auth_token}"
            }
        )
        data = response.json()
        self.assertFalse(data['success'])

    def test_get_email(self):
        # register new user
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'randomuser',
                'email': 'randomuser@gmail.com',
                'city': 'Oaks',
                'job': 'Chemist, analytical',
                'dob': '1983-04-21',
                'password1': 'randompassword',
                'password2': 'randompassword',
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        # get email of new user
        response = self.client.get(
            reverse('get_email'),
            data={
                'username': 'randomuser'
            }
        )
        data = response.json()
        self.assertTrue(data['email'] == 'randomuser@gmail.com')



