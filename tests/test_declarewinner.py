from django.test import TestCase
from beton.BusinessLayer.core.DeclareWinner import DeclareWinner as dw
from beton.models import Userinfo, Topics, BetInfo, Bets
import requests
import jwt
from django.test import Client



class TestDeclareWinner(TestCase):
    def test_declare_winner(self):
        Userinfo.objects.create(username="testuser109", password="Welcome@2018", emailID="test109@gmail.com", balance=200)
        user = Userinfo.objects.get(username='testuser109')
        Topics.objects.create(topic_name="test_topic109", creator_name=user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic109")
        response = dw().declare_winner(tpcid.topic_id,"A")
        self.assertEqual(response,"Declared winner")

    def test_declare_winner_no_option_selected(self):
        Userinfo.objects.create(username="testuser109", password="Welcome@2018", emailID="test109@gmail.com", balance=200)
        user = Userinfo.objects.get(username='testuser109')
        Topics.objects.create(topic_name="test_topic109", creator_name=user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic109")
        response = dw().declare_winner(tpcid.topic_id,"notselected")
        self.assertEqual(response,"Please select an option")

    def test_declare_winner_when_already_declared(self):
        Userinfo.objects.create(username="testuser109", password="Welcome@2018", emailID="test109@gmail.com", balance=200)
        user = Userinfo.objects.get(username='testuser109')
        Topics.objects.create(topic_name="test_topic109", creator_name=user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21", winning_option="A")
        tpcid = Topics.objects.get(topic_name="test_topic109")
        response = dw().declare_winner(tpcid.topic_id,"B")
        self.assertEqual(response,"You already Declared A as winning option")


    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="testuser400", password="Welcome2018",
                                            emailID="testuser400@gmail.com", balance = 200)
        self.user_dict = {"username": self.user.username}
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo',
                                          algorithm="HS256")


    def test_declare_winner_api(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        Topics.objects.create(topic_name="test_topic111", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        self.tpcid = Topics.objects.get(topic_name="test_topic111")
        response = self.client.get('http://127.0.0.1:8000/api/v1/declarewinner/?topic_id='+str(self.tpcid.topic_id)+'&option=A')
        print("*****************decalre winner*******************")
        print(response)
        print("done")
        self.assertEqual(response.status_code, 200)