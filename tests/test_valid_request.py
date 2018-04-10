import jwt
from django.test import Client
from django.test import TestCase
from beton.models import Userinfo
from tests.utils import *


class TestIsRequestValid(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="nikhil_test", password="Welcome@2018",
                                            emailID="nikhil_test@gmail.com")
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")

    #Missing Authentication token
    def test_missing_auth_request(self):
        response = self.client.post('http://localhost:8000/api/v1/validuser/')
        pay_load = get_dict_from_response(response)
        self.assertTrue('isValid' in pay_load.keys())
        flag = pay_load['isValid']
        self.assertTrue(flag == False)

    #has a Invalid token
    def test_invalid_auth_request(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = "Nikhil.Invalid.User.TryingtoHack"
        response = self.client.post('http://localhost:8000/api/v1/validuser/')
        pay_load = get_dict_from_response(response)
        self.assertTrue('isValid' in pay_load.keys())
        flag = pay_load['isValid']
        self.assertTrue(flag == False)
        self.client.defaults = {}


    #has a Valid token
    def test_valid_auth_request(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.post('http://localhost:8000/api/v1/validuser/')
        pay_load = get_dict_from_response(response)
        self.assertTrue('isValid' in pay_load.keys())
        flag = pay_load['isValid']
        self.assertTrue(flag == True)
        self.client.defaults = {}

