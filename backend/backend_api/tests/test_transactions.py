from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import json

class UserAuthenticationTests(TestCase):

    def test_make_transaction(self):
        # register account
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
        # Jimmy makes a transaction
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Jimmy',
                'cc_num': '1947292075921022',
                'merchant': 'GraceHallaway_94',
                'category': 'personal_care',
                'amt': '59.99',
                'city': 'Melbourne',
                'job': 'Accountant',
                'dob': '1995-04-23',
            },
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
        )
        data = response.json()
        self.assertTrue(data['success'])


    def test_process_transaction_log(self):
        # register user Alice
        response = self.client.post(
            reverse('signup'), 
            data={
                'username': 'Alice_9348',
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
        # Alice uploads transaction log
        csv_content = b'time_of_transfer,cc_num,merchant,category,amt,city,job,dob\n' + \
        b'2024-03-20 15:30:00.291929,1049578773623480,Alice_9348,entertainment,13.99,Medford,Administrator,1976-11-23\n' + \
        b'2024-03-25 17:11:39.394759,3758201757923857,Bob_2227,personal_care,24.99,Melbourne,Artist,1995-04-05\n'
        csv_file = SimpleUploadedFile("file.csv", csv_content, content_type="text/csv")
        response = self.client.post(
            reverse('process_transaction_log'),
            data={
                'username': 'Alice_9348',
                'transaction_log': csv_file
            },
            headers={
                'Authorization': f"Bearer {alice_auth}"
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
        # Alice sends money
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Alice',
                'cc_num': '1947292075921022',
                'merchant': 'GraceHallaway_94',
                'category': 'personal_care',
                'amt': '59.99',
                'city': 'Melbourne',
                'job': 'Accountant',
                'dob': '1995-04-23',
            },
            headers={
                'Authorization': f"Bearer {alice_auth}"
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        # Bob sends money
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Bob',
                'cc_num': '8392019210595825',
                'merchant': 'JimmyJones938',
                'category': 'personal_care',
                'amt': '59.99',
                'city': 'Melbourne',
                'job': 'Accountant',
                'dob': '1984-05-17',
            },
            headers={
                'Authorization': f"Bearer {bob_auth}"
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        # Claire makes two transactions
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Claire',
                'cc_num': '3948595920202184',
                'merchant': 'JimmyJones938',
                'category': 'entertainment',
                'amt': '129.99',
                'city': 'Melbourne',
                'job': 'Accountant',
                'dob': '1995-04-23',
            },
            headers={
                'Authorization': f"Bearer {claire_auth}"
            },
        )
        data = response.json()
        self.assertTrue(data['success'])
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Claire',
                'cc_num': '3948595920202184',
                'merchant': 'JimmyJones938',
                'category': 'entertainment',
                'amt': '129.99',
                'city': 'Melbourne',
                'job': 'Accountant',
                'dob': '1995-04-23',
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
        self.assertTrue(data['total_entries'] == "1")
        # get Bob's transaction history
        response = self.client.post(
            reverse('get_transaction_history'),
            data={'username': 'Bob', 'page_no' : 1},
            headers={
                'Authorization': f"Bearer {bob_auth}"
            }
        )
        data = response.json()
        self.assertTrue(data['total_entries'] == "1")
        # get Claire's transaction history
        response = self.client.post(
            reverse('get_transaction_history'),
            data={'username': 'Claire', 'page_no' : 1},
            headers={
                'Authorization': f"Bearer {claire_auth}"
            }
        )
        data = response.json()
        self.assertTrue(data['total_entries'] == "2")

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
        # Alice makes 100 transactions
        for _ in range(100):
            response = self.client.post(
                reverse('make_transaction'),
                data={
                    'username': 'Alice',
                    'cc_num': '3948595920202184',
                    'merchant': 'JimmyJones938',
                    'category': 'shopping_net',
                    'amt': '4.99',
                    'city': 'Melbourne',
                    'job': 'Accountant',
                    'dob': '1995-04-23',
                },
                headers={
                    'Authorization': f"Bearer {alice_auth}"
                }
            )
            data = response.json()
            self.assertTrue(data['success'])
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
        self.assertTrue(len(data['transaction_history']) == 50)
        self.assertTrue(data['total_entries'] == "100")

    def test_search_transactions(self):
        # register account
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
        # Jimmy makes a transaction
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Jimmy',
                'cc_num': '1947292075921022',
                'merchant': 'merchant1',
                'category': 'personal_care',
                'amt': '59.99',
                'city': 'Melbourne',
                'job': 'Accountant',
                'dob': '1995-04-23',
            },
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Jimmy',
                'cc_num': '1947292075921022',
                'merchant': 'merchant2',
                'category': 'personal_care',
                'amt': '59.99',
                'city': 'Melbourne',
                'job': 'Accountant',
                'dob': '1995-04-23',
            },
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Jimmy',
                'cc_num': '1947292075921022',
                'merchant': 'merchant3',
                'category': 'personal_care',
                'amt': '59.99',
                'city': 'Melbourne',
                'job': 'Accountant',
                'dob': '1995-04-23',
            },
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        response = self.client.post(
            reverse('make_transaction'),
            data={
                'username': 'Jimmy',
                'cc_num': '1947292075921022',
                'merchant': 'merchant',
                'category': 'personal_care',
                'amt': '59.99',
                'city': 'Melbourne',
                'job': 'Accountant',
                'dob': '1995-04-23',
            },
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
        )
        data = response.json()
        self.assertTrue(data['success'])
        response = self.client.post(
            reverse('get_transaction_by_field'),
            data={
                'username': 'Jimmy',
                'page_no': 1,
                'search_fields': json.dumps({
                    'merchant': 'merchant3',
                    'category': 'personal_care'
                }),
                'sort_fields': json.dumps(['dob'])
            },
            headers={
                'Authorization': f"Bearer {auth_token}"
            }
        )
        #search by merchant = merchant 3
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['total_entries'] == "1")
