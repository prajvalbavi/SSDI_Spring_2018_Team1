import jwt
from django.test import Client
from django.test import TestCase
from beton.models import BetOnAdmins as admins
from tests.utils import *

class TestAdminLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_identity = "test_admin"
        self.password = "test_password"
        self.secret_key = "test_secret_key"
        self.admin = admins.objects.create(admin_identity=self.admin_identity, password=self.password,
                                           secret_key=self.secret_key)

    def test_admin_login_valid(self):
        response = self.client.post('http://localhost:8000/api/v1/auth/',
                                    data={'identifier': self.admin_identity,
                                          'password': self.password, 'is_admin': "true", 'secret_key': self.secret_key})


        pay_load = get_dict_from_response(response)
        self.assertTrue('token' in pay_load.keys())
        auth_token = pay_load['token']

        # Validate the authorization token signature.
        pay_load = jwt.decode(auth_token, 'ThisU$erI$LoggedInBetoInfo'+ self.secret_key, algorithm="HS256")
        self.assertTrue(pay_load["username"] == self.admin_identity)


    def test_admin_login_invalid_identity(self):
        response = self.client.post('http://localhost:8000/api/v1/auth/',
                                    data={'identifier': 'Nikhil10001',
                                          'password': self.password, 'is_admin': "true", 'secret_key': self.secret_key})


        pay_load = get_dict_from_response(response)

        self.assertTrue('errors' in pay_load.keys())
        errors_dict = pay_load['errors']
        self.assertTrue(type(errors_dict) == dict)
        self.assertTrue('form' in errors_dict.keys())
        error_message = errors_dict['form']
        self.assertTrue(error_message == 'Invalid Credentials')

        # validate status code
        self.assertTrue(response.status_code == 401)

    def test_admin_login_invalid_password(self):
        response = self.client.post('http://localhost:8000/api/v1/auth/',
                                    data={'identifier': self.admin_identity,
                                          'password': "Nikhil10001", 'is_admin': "true", 'secret_key': self.secret_key})


        pay_load = get_dict_from_response(response)

        self.assertTrue('errors' in pay_load.keys())
        errors_dict = pay_load['errors']
        self.assertTrue(type(errors_dict) == dict)
        self.assertTrue('form' in errors_dict.keys())
        error_message = errors_dict['form']
        self.assertTrue(error_message == 'Invalid Credentials')

        # validate status code
        self.assertTrue(response.status_code == 401)

    def test_admin_login_invalid_secret_key(self):
        response = self.client.post('http://localhost:8000/api/v1/auth/',
                                        data={'identifier': self.admin_identity,
                                              'password':  self.password , 'is_admin': "true",
                                              'secret_key': "NikhilKeySecret"})

        pay_load = get_dict_from_response(response)

        self.assertTrue('errors' in pay_load.keys())
        errors_dict = pay_load['errors']
        self.assertTrue(type(errors_dict) == dict)
        self.assertTrue('form' in errors_dict.keys())
        error_message = errors_dict['form']
        self.assertTrue(error_message == 'Invalid Credentials')

        # validate status code
        self.assertTrue(response.status_code == 401)


    def test_admin_login_invalid_admin_flag(self):
        response = self.client.post('http://localhost:8000/api/v1/auth/',
                                        data={'identifier': self.admin_identity,
                                              'password':  self.password , 'is_admin': "false",
                                              'secret_key': self.secret_key})

        pay_load = get_dict_from_response(response)

        self.assertTrue('errors' in pay_load.keys())
        errors_dict = pay_load['errors']
        self.assertTrue(type(errors_dict) == dict)
        self.assertTrue('form' in errors_dict.keys())
        error_message = errors_dict['form']
        self.assertTrue(error_message == 'Invalid Credentials')

        # validate status code
        self.assertTrue(response.status_code == 401)
