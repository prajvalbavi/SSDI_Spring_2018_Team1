from django.test import TestCase
from beton.BusinessLayer.SignupUser import SignupUser as su
from beton.BusinessLayer.GetPublicTopics import BetInformation
from beton.models import Userinfo, Topics, BetInfo
from django.test import Client
from beton.BusinessLayer.ValidateUser import Validate
from beton.BusinessLayer.AuthenticateUser import Authenticate
import jwt

import requests

class TestSignUp(TestCase):

    def test_valid_signup(self):
        response , message = su.signup("apurva", "Welcome@2018", "apurva@gmail.com")
        self.assertEqual(response,"success")

    def test_invalid_signup1(self):
        Userinfo.objects.create(username = "apurva123", password = "Welcome@2018", emailID = "apurva123@gmail.com")
        response , message = su.signup("apurva123", "Welcome@2018", "apurva123@gmail.com")
        self.assertEqual(response,"error")
        self.assertEqual(message,"Username already exists")


    def test_invalid_signup2(self):
        Userinfo.objects.create(username = "apurva123", password = "Welcome@2018", emailID = "apurva123@gmail.com")
        response , message = su.signup("apurva999", "Welcome@2018", "apurva123@gmail.com")
        self.assertEqual(response,"error")
        self.assertEqual(message,"Email already exists")


    def test_invalid_signup3(self):
        Userinfo.objects.create(username = "apurva789", password = "Welcome@2018", emailID = "apurva789@gmail.com")
        Userinfo.objects.create(username="apurva456", password="Welcome@2018", emailID="apurva456@gmail.com")
        response , message = su.signup("apurva789", "Welcome@2018", "apurva456@gmail.com")
        self.assertEqual(response,"exception")
        self.assertEqual(message,"Both username and Email already exists")

class TestGetPublicTopics(TestCase):
    def test_get_topics_empty(self):
        bi = BetInformation()
        response = bi.get_info_by_topic()
        self.assertEqual(len(response),0)

    def test_get_topics_non_empty(self):
        bi = BetInformation()
        Topics.objects.create(topic_name = "abc", creator_name = "abc", start_date = "2017-11-21", end_date = "2017-11-21", date_of_creation = "2017-11-21")
        Topics.objects.create(topic_name = "pqr", creator_name = "pqr", start_date = "2017-11-21", end_date = "2017-11-21", date_of_creation = "2017-11-21")
        response = bi.get_info_by_topic()
        self.assertEqual(len(response),2)

class SignupAPI:
    def post_signup_new(self, username, email, password):
        url = "http://127.0.0.1:8000/api/v1/signup/"

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n"+username+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n"+email+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n"+password+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Cache-Control': "no-cache",
            'Postman-Token': "7702dcf0-16c2-4722-a542-5ce4deafee49"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.json()

    def post_signup_present(self, username, email, password):
        url = "http://127.0.0.1:8000/api/v1/signup/"

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n"+ username +"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n" + email +"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n"+password+"\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Cache-Control': "no-cache",
            'Postman-Token': "7702dcf0-16c2-4722-a542-5ce4deafee49"
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.json()


class TestApplicationMethods(TestCase):


    def test_email_in_team(self):
        signup = SignupAPI()
        server_response = signup.post_signup_present("prajval1", "pbavi1@uncc.edu", "Welcome123")
        self.assertTrue(server_response['message'] == "Username already exists")
        self.assertTrue(server_response['status'] == "error")

    def test_user_in_team(self):
        signup = SignupAPI()
        server_response = signup.post_signup_present("prajval1221", "pbavi962@uncc.edu", "Welcome123")
        self.assertTrue(server_response['message'] == "Email already exists")
        self.assertTrue(server_response['status'] == "error")

    def test_new_user(self):
        signup = SignupAPI()
        server_response = signup.post_signup_new("prajval1212", "pbavi9292@uncc.edu", "Welcome123")
        self.assertTrue(server_response['message'] == "User added successfully")
        self.assertTrue(server_response['status'] == "success")


 def get_dict_from_response(response):
        return response.json()


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


class TestValidate(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="nikhil_test", password="Welcome@2018",
                                            emailID="nikhil_test@gmail.com")
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")


    def test_is_user_valid_with_missing_token(self):
        flag, message = Validate.is_user_valid()
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



class TestAuthenticate(TestCase):
    def setUp(self):
        self.user = Userinfo.objects.create(username="nikhil_test", password="Welcome@2018",
                                            emailID="nikhil_test@gmail.com")

    def test_authenticate_user_with_valid_username(self):
        flag, message, uname = Authenticate.authenticate_user(self.user.username, self.user.password)
        self.assertTrue(flag == True)
        self.assertTrue(message = "User Authenticated")
        self.assertTrue(uname == self.user.username)

    def test_authenticate_user_with_valid_email(self):
        flag, message, uname = Authenticate.authenticate_user(self.user.emailID, self.user.password)
        self.assertTrue(flag == True)
        self.assertTrue(message = "User Authenticated")
        self.assertTrue(uname == self.user.username)

    def test_authenticate_user_with_invalid_username(self):
        flag, message, uname = Authenticate.authenticate_user("Nikhil567", self.user.password)
        self.assertTrue(flag == False)
        self.assertTrue(message = "Invalid Credentials")
        self.assertTrue(uname == '')

    def test_authenticate_user_with_invalid_email(self):
        flag, message, uname= Authenticate.authenticate_user("Nikhil910@gmail.com", self.user.password)
        self.assertTrue(flag == False)
        self.assertTrue(message = "Invalid Credentials")
        self.assertTrue(uname == '')

    def test_authenticate_user_with_invalid_password(self):
        flag, message, flag,uname = Authenticate.authenticate_user(self.user.username, "Nikhilabc")
        self.assertTrue(flag == False)
        self.assertTrue(message = "Invalid Credentials")
        self.assertTrue(uname == '')

        flag, message, uname = Authenticate.authenticate_user(self.user.emailID, "Nikhilabc")
        self.assertTrue(flag == False)
        self.assertTrue(message="Invalid Credentials")
        self.assertTrue(uname == '')

    def test_generate_token_valid_payload(self):
        pay_load = {"username": self.user.username}
        token = Authenticate.generate_token(pay_load)
        self.assertTrue(token is not None and token is not '')
        pay_load_returned = jwt.decode(token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")

        self.assertTrue(pay_load_returned['username'] == pay_load['username'])

    def test_generate_token_id_valid_username(self):
        token = Authenticate.generate_token_id(self.user.username)
        pay_load_returned = jwt.decode(token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")

        self.assertTrue(pay_load_returned['username'] == self.user.username)

    def test_generate_token_id_valid_email(self):
        token = Authenticate.generate_token_id(self.user.emailID)
        pay_load_returned = jwt.decode(token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")

        self.assertTrue(pay_load_returned['username'] == self.user.username)














