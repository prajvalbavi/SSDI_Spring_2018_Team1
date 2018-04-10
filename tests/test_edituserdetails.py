from django.test import TestCase
from beton.BusinessLayer.CheckUser import CheckUser
from beton.views import post_edituserdetails
from beton.BusinessLayer.UserBetDetails import UserBetDetials
from beton.models import Userinfo, Topics, BetInfo, Bets
import requests
import jwt
from django.test import Client


class Test_Edit_User_Details(TestCase):
    def test_invalid_email(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        username = "testuser1"
        password = "Welcome@2018"
        emailID = "test@gmail.com"
        status, status_msg = CheckUser.check_user(username, password, emailID)
        self.assertEqual(status,"error")
        self.assertEqual(status_msg, "Previous email same as new")

    def test_valid_email(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        username = "testuser1"
        password = "Welcome@2018"
        emailID = "test1@gmail.com"
        status, status_msg = CheckUser.check_user(username, password, emailID)
        self.assertEqual(status, "success")
        self.assertEqual(status_msg, "Password correct")

    def test_invalid_password(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        username = "testuser1"
        password = "Welcome2018"
        emailID = "test@gmail.com"
        status, status_msg = CheckUser.check_user(username, password, emailID)
        self.assertEqual(status, "error")
        self.assertEqual(status_msg, "Password incorrect")

    def test_valid_update(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        username = "testuser1"
        password = "Welcome@2018"
        emailID = "test12@gmail.com"
        status, status_msg = CheckUser.update_user(username, password, emailID)
        self.assertEqual(status, "success")
        self.assertEqual(status_msg, "Update success")
        _updated_obj = Userinfo.objects.get(username=username)
        self.assertEqual(_updated_obj.username, username)
        self.assertEqual(_updated_obj.password, password)
        self.assertEqual(_updated_obj.emailID, emailID)

    def test_exception_username(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        username = "testuser"
        password = "Welcome@2018"
        emailID = "test@gmail.com"
        status, status_msg = CheckUser.update_user(username, password, emailID)
        self.assertEqual(status, "exception")
        self.assertEqual(status_msg, "Userinfo matching query does not exist.")

    def test_exception_email(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        username = "testuser"
        password = "Welcome@2018"
        emailID = "test12@gmail.com"
        status, status_msg = CheckUser.update_user(username, password, emailID)
        self.assertEqual(status, "exception")
        self.assertEqual(status_msg, "Userinfo matching query does not exist.")

    def test_exception_password(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        username = "testuser"
        password = "Welcome2018"
        emailID = "test@gmail.com"
        status, status_msg = CheckUser.update_user(username, password, emailID)
        self.assertEqual(status, "exception")
        self.assertEqual(status_msg, "Userinfo matching query does not exist.")


class Test_Edit_User_Details_API(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="testuser1", password="Welcome2018",
                                            emailID="testuser1@gmail.com")
        self.user_dict = {"username" : self.user.username, "password" : self.user.password, "email" : self.user.emailID}
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")

    def test_invalid_email(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.post('http://localhost:8000/api/v1/edituserdetails/', self.user_dict)
        res = response.json()
        self.assertEqual(res['status'], "error")
        self.assertEqual(res['message'], "Previous email same as new")

    def test_valid_email(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        self.user_dict['email'] = "testuser@gmail.com"
        response = self.client.post('http://localhost:8000/api/v1/edituserdetails/', self.user_dict)
        res = response.json()
        self.assertEqual(res['status'], "success")
        self.assertEqual(res['message'], "Update success")

    def test_invalid_password(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        self.user_dict['password'] = "testuser@gmail.com"
        response = self.client.post('http://localhost:8000/api/v1/edituserdetails/', self.user_dict)
        res = response.json()
        self.assertEqual(res['status'], "error")
        self.assertEqual(res['message'], "Password incorrect")


class Test_Get_User_Details_API(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="testuser1", password="Welcome2018",
                                            emailID="testuser1@gmail.com")
        self.user_dict = {"username": self.user.username}
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")


    def test_valid_call(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.post('http://localhost:8000/api/v1/user/', self.user_dict)
        res = response.json()
        self.assertEqual(res['status'], "success")
        self.assertEqual(res['username'], "testuser1")
        self.assertEqual(res['email'], 'testuser1@gmail.com')

    def test_invalid_username_call(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        self.user_dict_1 = {"username": "newuser"}
        response = self.client.post('http://localhost:8000/api/v1/user/', self.user_dict_1)
        res = response.json()
        self.assertEqual(res['status'], "exception")
        self.assertEqual(res['message'], "Userinfo matching query does not exist.")



class Test_Get_User_Details(TestCase):
    def setUp(self):
        self.user = Userinfo.objects.create(username="testuser1", password="Welcome2018",
                                            emailID="testuser1@gmail.com")
        self.user_dict = {"username": self.user.username}

    def test_valid_user(self):
        res_status, res_message_username, res_message_email =  CheckUser.get_user(self.user.username).values()
        self.assertEqual(res_status, "success")
        self.assertEqual(res_message_username, self.user.username)
        self.assertEqual(res_message_email, self.user.emailID)

    def test_invalid_user(self):
        res_status, res_message = CheckUser.get_user("nosuchuser").values()
        self.assertEqual(res_status, "exception")
        self.assertEqual(res_message, "Userinfo matching query does not exist.")








