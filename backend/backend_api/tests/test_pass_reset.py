from django.test import TestCase
from django.urls import reverse
import imaplib
import email

class UserAuthenticationTests(TestCase):
    def test_reset_pass_success(self):
        #register new user
        response = self.client.post(
            reverse('signup'),
            data = {
                'username': 'newuser',
                'email': 'pearproject3900@gmail.com',
                'password1': 'admin123123',
                'password2': 'admin123123',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        auth_token = data['token']
        # reset request to get One-Time-Password
        response = self.client.post(
            reverse('reset_request'), 
            data={
                'username': 'newuser',
                'email': 'pearproject3900@gmail.com'
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        self.assertTrue(response.json()['success'])
        receiver_email = "pearproject3900@gmail.com"
        receiver_pass = "obed iylr awsd trqg"
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(receiver_email, receiver_pass)
        imap.select('INBOX')
        result, data = imap.search(None, '(FROM "pearproject3900@gmail.com" SUBJECT "OTP for password reset")')
        ids = data[0]
        id_list = ids.split()
        latest_email_id = id_list[-1]
        result, data = imap.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        msg = email.message_from_string(raw_email_string)
        otp = msg.get_payload()
        otp = otp.strip()
        # request password reset with One-Time-Password
        response = self.client.post(
            reverse('reset_password'), 
            data={
                'email': receiver_email,
                'otp': otp,
                'password1': 'admin123123123',
                'password2': 'admin123123123'
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        # login with new password
        data = response.json()
        self.assertTrue(data['success'])
        new_auth_token = data['token']
        response = self.client.post(
            reverse('login'),
            data={
                'username': 'newuser',
                'password': 'admin123123123'
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=new_auth_token
        )
        data = response.json()
        self.assertTrue(data['success'])

    def test_reset_pass_wrong_otp(self):
        #register new user
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'newuser',
                'email': 'pearproject3900@gmail.com',
                'password1': 'admin123123',
                'password2': 'admin123123',
                'accountType': 'client'
            }, 
            content_type='application/json')
        data = response.json()
        self.assertTrue(data['success'])
        auth_token = data['token']
        # request one-time-password for password reset
        response = self.client.post(
            reverse('reset_request'), 
            data={'email': 'pearproject3900@gmail.com'},
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        self.assertTrue(response.json()['success'])
        receiver_email = "pearproject3900@gmail.com"
        receiver_pass = "obed iylr awsd trqg"
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(receiver_email, receiver_pass)
        imap.select('INBOX')
        result, data = imap.search(None, '(FROM "pearproject3900@gmail.com" SUBJECT "OTP for password reset")')
        ids = data[0]
        id_list = ids.split()
        latest_email_id = id_list[-1]
        result, data = imap.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        msg = email.message_from_string(raw_email_string)
        otp = msg.get_payload()
        otp = int(otp.strip())
        # request password reset with wrong one-time-pass
        response = self.client.post(
            reverse('reset_password'), 
            data={
                'email': receiver_email,
                'otp': str(otp + 1),
                'password1': 'admin123123123',
                'password2': 'admin123123123'
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        data = response.json()
        self.assertFalse(data['success'])
