from django.test import TestCase
from django.urls import reverse

class UserAuthenticationTests(TestCase):

    def test_make_transaction(self):
        # register payer
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Jimmy',
                'email': 'Neutron@IMBCorporate.com',
                'password1': 'alax_memento_j44',
                'password2': 'alax_memento_j44',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        auth_token = data['token']
        # register payee
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'GraceHallaway_39',
                'email': 'GraceHallaway@ghibli.com',
                'password1': 'Kdubn395ng',
                'password2': 'Kdubn395ng',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        # Jimmy pays Grace 13.99
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Jimmy',
                'payeeName': 'GraceHallaway_39',
                'amountPayed': 13.99
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=auth_token
        )
        data = response.json()
        self.assertTrue(data['success'])

    def test_get_transaction_history(self):
        # register user Alice
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Alice',
                'email': 'Alice814@gmail.com',
                'password1': 'SpringClean__324',
                'password2': 'SpringClean__324',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        alice_auth = data['token']
        # register user Bob
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Bob',
                'email': 'Bob2394@gmail.com',
                'password1': 'CleanSpring__391',
                'password2': 'CleanSpring__391',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        bob_auth = data['token']
        # register user Claire
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Claire',
                'email': 'Claire@protonmail.com',
                'password1': 'Elly294F4our',
                'password2': 'Elly294F4our',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        claire_auth = data['token']
        # Alice sends Bob money
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Alice',
                'payeeName': 'Bob',
                'amountPayed': 13.99
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=alice_auth
        )
        data = response.json()
        self.assertTrue(data['success'])
        # Bob sends Alice money
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Bob',
                'payeeName': 'Alice',
                'amountPayed': 19.99
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=bob_auth
        )
        data = response.json()
        self.assertTrue(data['success'])
        # Claire sends Alice money
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Claire',
                'payeeName': 'Alice',
                'amountPayed': 24.99
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=claire_auth
        )
        data = response.json()
        self.assertTrue(data['success'])
        # get Alice's transaction history
        response = self.client.post(
            reverse('get_transaction_history'),
            data={'username': 'Alice', 'page_no' : 1},
            content_type='application/json',
            HTTP_AUTHORIZATION=alice_auth
        )
        data = response.json()
        self.assertTrue(len(data['transaction_history']) == 3)
        # get Bob's transaction history
        response = self.client.post(
            reverse('get_transaction_history'),
            data={'username': 'Bob', 'page_no' : 1},
            content_type='application/json',
            HTTP_AUTHORIZATION=bob_auth
        )
        data = response.json()
        self.assertTrue(len(data['transaction_history']) == 2)
        # get Claire's transaction history
        response = self.client.post(
            reverse('get_transaction_history'),
            data={'username': 'Claire', 'page_no' : 1},
            content_type='application/json',
            HTTP_AUTHORIZATION=claire_auth
        )
        data = response.json()
        self.assertTrue(len(data['transaction_history']) == 1)

    def test_transaction_history_pagination(self):
        # register user Alice
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Alice',
                'email': 'Alice814@gmail.com',
                'password1': 'SpringClean__324',
                'password2': 'SpringClean__324',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        alice_auth = data['token']
        # register user Bob
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Bob',
                'email': 'Bob2394@gmail.com',
                'password1': 'CleanSpring__391',
                'password2': 'CleanSpring__391',
                'accountType': 'client'
            },
            content_type='application/json'
        )
        data = response.json()
        self.assertTrue(data['success'])
        # Alice makes 100 transactions to Bob
        for _ in range(100):
            response = self.client.post(
                reverse('make_transaction'),
                data={
                    'username': 'Alice',
                    'payeeName': 'Bob',
                    'amountPayed': 1.00
                },
            content_type='application/json',
            HTTP_AUTHORIZATION=alice_auth
        )
        # get transaction history
        response = self.client.post(
            reverse('get_transaction_history'),
            data={'username': 'Alice', 'page_no' : 1},
            content_type='application/json',
            HTTP_AUTHORIZATION=alice_auth
        )
        # default capped at 50
        data = response.json()
        self.assertTrue(len(data['transaction_history']) == 50)



