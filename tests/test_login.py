import jwt
from django.test import Client
from django.test import TestCase
from beton.models import Userinfo
from tests.utils import *


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user =   Userinfo.objects.create(username = "nikhil_test", password = "Welcome@2018", emailID = "nikhil_test@gmail.com")
        self.valid_token_user = jwt.decode({'identifier': self.user.username, 'password': self.user.password})
        self.valid_token_email = jwt.decode({'identifier': self.user.username, 'password': self.user.password})

    def test_login_valid_username(self):
        username = self.user.username
        password = self.user.password
        response = self.client.post('api/v1/validuser/', data={'identifier': username, 'password': password})
        pay_load = get_dict_from_response(response)
        self.assertTrue('token' in pay_load.keys())
        auth_token = pay_load['token']

        #Validate the authorization token signature.
        pay_load = jwt.decode(auth_token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
        self.assertTrue(pay_load["identifier"] == username)
        self.assertTrue(pay_load["password"] == password)

    def test_login_valid_email(self):
        emaiId = self.user.emailID
        password = self.user.password
        response = self.client.post('api/v1/validuser/', data={'identifier': emaiId, 'password': password})
        pay_load = get_dict_from_response(response)
        self.assertTrue('token' in pay_load.keys())
        auth_token = pay_load['token']

        #Validate the authorization token signature.
        pay_load = jwt.decode(auth_token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
        self.assertTrue(pay_load["identifier"] == emaiId)
        self.assertTrue(pay_load["password"] == password)

        #validate status code
        self.assertTrue(response.status_code == 200)

    def test_login_invalid_username(self):
        username = "nikhil112233"
        password = self.user.password
        response = self.client.post('api/v1/validuser/', data={'identifier': username, 'password': password})
        pay_load = get_dict_from_response(response)
        self.assertTrue('errors' in pay_load.keys())
        errors_dict = pay_load['token']
        self.assertTrue(type(errors_dict) == dict)
        self.assertTrue('form' in errors_dict.keys())
        error_message = errors_dict['form']
        self.assertTrue(error_message == 'Invalid Credentials')

        # validate status code
        self.assertTrue(response.status_code == 401)

        # validate status code
        self.assertTrue(response.status_code == 401)

    def test_login_invalid_email(self):
        emaiId = "nikhil112233@gmail.com"
        password = self.user.password
        response = self.client.post('api/v1/validuser/', data={'identifier': emaiId, 'password': password})
        pay_load = get_dict_from_response(response)
        self.assertTrue('errors' in pay_load.keys())
        errors_dict = pay_load['token']
        self.assertTrue(type(errors_dict) == dict)
        self.assertTrue('form' in errors_dict.keys())
        error_message = errors_dict['form']
        self.assertTrue(error_message == 'Invalid Credentials')

        # validate status code
        self.assertTrue(response.status_code == 401)


    def test_login_invalid_password(self):
        username = self.user.username
        password = 'nikhilaabbcc'
        response = self.client.post('api/v1/validuser/', data={'identifier': username, 'password': password})
        pay_load = get_dict_from_response(response)
        self.assertTrue('errors' in pay_load.keys())
        errors_dict = pay_load['token']
        self.assertTrue(type(errors_dict) == dict)
        self.assertTrue('form' in errors_dict.keys())
        error_message = errors_dict['form']
        self.assertTrue(error_message == 'Invalid Credentials')

        # validate status code
        self.assertTrue(response.status_code == 401)
