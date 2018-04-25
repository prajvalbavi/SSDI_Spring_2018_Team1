import jwt
from django.test import Client
from django.test import TestCase
from beton.models import BetOnAdmins as admins
from tests.utils import *

class TestAdminValidation(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = admins.objects.create(admin_identity="test_admin", password="test_password",
                                           secret_key="test_secret_key")

        self.valid_token = jwt.encode({'username': self.admin.admin_identity},
                                      'ThisU$erI$LoggedInBetoInfo' + self.admin.secret_key, algorithm="HS256")

    def test_validate_admin_missing_token(self):
        response = self.client.post('http://localhost:8000/api/v1/validuser/', data={"is_admin": "true"})
        pay_load = get_dict_from_response(response)
        self.assertTrue('isValid' in pay_load.keys())
        flag = pay_load['isValid']
        self.assertTrue(flag == False)

    #has a Invalid token
    def test_validate_admin_invalid_token(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = "Nikhil.Invalid.User.TryingtoHack"
        response = self.client.post('http://localhost:8000/api/v1/validuser/', data={"is_admin": "true"})
        pay_load = get_dict_from_response(response)
        self.assertTrue('isValid' in pay_load.keys())
        flag = pay_load['isValid']
        self.assertTrue(flag == False)
        self.client.defaults = {}


    #has a Valid token
    def test_valid_auth_request(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.post('http://localhost:8000/api/v1/validuser/', data={"is_admin": "true"})
        pay_load = get_dict_from_response(response)
        self.assertTrue('isValid' in pay_load.keys())
        flag = pay_load['isValid']
        self.assertTrue(flag == True)
        self.client.defaults = {}
