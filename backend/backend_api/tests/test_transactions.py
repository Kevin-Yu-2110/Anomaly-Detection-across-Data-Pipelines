from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class UserAuthenticationTests(TestCase):

    def test_make_transaction(self):
        # register payer
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Jimmy',
                'email': 'Neutron@IMBCorporate.com',
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'alax_memento_j44',
                'password2': 'alax_memento_j44',
            }
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
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'Kdubn395ng',
                'password2': 'Kdubn395ng',
            }
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
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
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
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'SpringClean__324',
                'password2': 'SpringClean__324',
            }
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
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'CleanSpring__391',
                'password2': 'CleanSpring__391',
            }
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
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'Elly294F4our',
                'password2': 'Elly294F4our',
            }
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
            headers={
                'Authorization': f"Bearer {alice_auth}"
            }
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
            headers={
                'Authorization': f"Bearer {bob_auth}"
            }
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
            headers={
                'Authorization': f"Bearer {claire_auth}"
            },
        )
        data = response.json()
        self.assertTrue(data['success'])
        # get Alice's transaction history
        response = self.client.post(
            reverse('get_transaction_history'),
            data={'username': 'Alice', 'page_no' : 1},
            headers={
                'Authorization': f"Bearer {alice_auth}"
            },
        )
        data = response.json()
        self.assertTrue(data['total_entries'] == "3")
        # get Bob's transaction history
        response = self.client.post(
            reverse('get_transaction_history'),
            data={'username': 'Bob', 'page_no' : 1},
            headers={
                'Authorization': f"Bearer {bob_auth}"
            }
        )
        data = response.json()
        self.assertTrue(data['total_entries'] == "2")
        # get Claire's transaction history
        response = self.client.post(
            reverse('get_transaction_history'),
            data={'username': 'Claire', 'page_no' : 1},
            headers={
                'Authorization': f"Bearer {claire_auth}"
            }
        )
        data = response.json()
        self.assertTrue(data['total_entries'] == "1")

    def test_transaction_history_pagination(self):
        # register user Alice
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Alice',
                'email': 'Alice814@gmail.com',
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'SpringClean__324',
                'password2': 'SpringClean__324',
            }
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
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'CleanSpring__391',
                'password2': 'CleanSpring__391',
            }
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
                headers={
                    'Authorization': f"Bearer {alice_auth}"
                }
            )
        # get transaction history
        response = self.client.post(
            reverse('get_transaction_history'),
            data={'username': 'Alice', 'page_no' : 1},
            headers={
                'Authorization': f"Bearer {alice_auth}"
            }
        )
        # default capped at 50
        data = response.json()
        self.assertTrue(len(data['transaction_history']) == "50")
        self.assertTrue(data['total_entries'] == "100")

    def test_process_transaction_log(self):
        # register user Alice
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Alice',
                'email': 'Alice814@gmail.com',
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'SpringClean__324',
                'password2': 'SpringClean__324',
            }
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
                'city': 'Melbourne',
                'job': 'Cartographer',
                'dob': '1971-11-03',
                'password1': 'CleanSpring__391',
                'password2': 'CleanSpring__391',
            }
        )
        # Alice uploads transaction log
        csv_content = b'username,payee_name,amount,time_of_transfer\n' + \
        b'Alice_9348,Bob_2227,13.99,2024-03-18 14:30:15.302193\n' + \
        b'Bob_2227,Alice_9348,24.99,2024-03-19 17:22:34.202849\n'
        csv_file = SimpleUploadedFile("file.csv", csv_content, content_type="text/csv")
        response = self.client.post(
            reverse('process_transaction_log'),
            data={
                'username': 'Alice',
                'transaction_log': csv_file
            },
            headers={
                'Authorization': f"Bearer {alice_auth}"
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
