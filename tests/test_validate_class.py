import jwt
from django.test import Client
from django.test import TestCase
from beton.BusinessLayer.ValidateUser import Validate
from beton.models import Userinfo


class TestValidate(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="nikhil_test", password="Welcome@2018",
                                            emailID="nikhil_test@gmail.com")
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")


    def test_is_user_valid_with_missing_token(self):
        token = None
        flag, message = Validate.is_user_valid(token)
        self.assertTrue(flag == False)
        self.assertTrue(message == 'Missing Token')

    def test_is_user_valid_with_empty_token(self):
        flag, message = Validate.is_user_valid('')
        self.assertTrue(flag == False)
        self.assertTrue(message == 'Missing Token')

    def test_is_user_valid_with_invalid_token(self):
        token = "Nikhil.Invalid.User.TryingtoHack"
        flag, message = Validate.is_user_valid(token)
        self.assertTrue(flag == False)
        self.assertTrue(message == 'Invalid User')

    def test_is_user_valid_with_valid_token(self):
        token = self.valid_token
        flag, message = Validate.is_user_valid(token)
        self.assertTrue(flag == True)
        self.assertTrue(message == 'Valid User')

