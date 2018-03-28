from django.test import TestCase
from beton.BusinessLayer.SignupUser import SignupUser as su
from beton.BusinessLayer.GetPublicTopics import BetInformation
from beton.models import Userinfo, Topics, BetInfo

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