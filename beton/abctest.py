from django.test import TestCase
from beton.BusinessLayer.SignupUser import SignupUser as su
from beton.BusinessLayer.GetPublicTopics import BetInformation
from beton.models import Userinfo, Topics, BetInfo
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
