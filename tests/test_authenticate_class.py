import jwt
from django.test import TestCase
from beton.BusinessLayer.core.UserAuthorization import UserAuthorization
from beton.models import Userinfo


class TestAuthenticate(TestCase):
    def setUp(self):
        self.user = Userinfo.objects.create(username="nikhil_test", password="Welcome@2018",
                                            emailID="nikhil_test@gmail.com")
        self.auth = UserAuthorization()
        

    def test_authenticate_user_with_valid_username(self):
        flag, message, uname = self.auth.authenticate(self.user.username, self.user.password)
        self.assertTrue(flag == True)
        self.assertTrue(message == "User Authenticated")
        self.assertTrue(uname == self.user.username)

    def test_authenticate_user_with_valid_email(self):
        flag, message, uname = self.auth.authenticate(self.user.emailID, self.user.password)
        self.assertTrue(flag == True)
        self.assertTrue(message == "User Authenticated")
        self.assertTrue(uname == self.user.username)

    def test_authenticate_user_with_invalid_username(self):
        flag, message, uname = self.auth.authenticate("Nikhil567", self.user.password)
        self.assertTrue(flag == False)
        self.assertTrue(message == "Invalid Credentials")
        self.assertTrue(uname == '')

    def test_authenticate_user_with_invalid_email(self):
        flag, message, uname= self.auth.authenticate("Nikhil910@gmail.com", self.user.password)
        self.assertTrue(flag == False)
        self.assertTrue(message == "Invalid Credentials")
        self.assertTrue(uname == '')

    def test_authenticate_user_with_invalid_password(self):
        flag, message,uname = self.auth.authenticate(self.user.username, "Nikhilabc")
        self.assertTrue(flag == False)
        self.assertTrue(message == "Invalid Credentials")
        self.assertTrue(uname == '')

        flag, message, uname = self.auth.authenticate(self.user.emailID, "Nikhilabc")
        self.assertTrue(flag == False)
        self.assertTrue(message=="Invalid Credentials")
        self.assertTrue(uname == '')

    def test_generate_token_valid_payload(self):
        token = self.auth.generate_token(self.user.username)
        self.assertTrue(token is not None and token is not '')

        pay_load_returned = jwt.decode(token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
        self.assertTrue(pay_load_returned['username'] == self.user.username)

    def test_generate_token_id_valid_username(self):
        flag, token = self.auth.generate_token(self.user.username)
        pay_load_returned = jwt.decode(token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
        self.assertTrue(pay_load_returned['username'] == self.user.username)

    def test_generate_token_id_valid_email(self):
        flag, token = self.auth.generate_token(self.user.emailID)
        pay_load_returned = jwt.decode(token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
        self.assertTrue(pay_load_returned['username'] == self.user.username)
