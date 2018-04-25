from django.test import TestCase
from beton.BusinessLayer.core.DailyBets import DailyBets as db
from beton.models import Userinfo, Topics, BetInfo, Bets
import requests
import jwt
from django.test import Client



class TestDailyBets(TestCase):
    def test_nobets(self):
        response = db().dailybets()
        self.assertEqual(response,{})

    def test_multiplebets(self):
        Userinfo.objects.create(username="testuser186", password="Welcome@2018", emailID="test185@gmail.com", balance=200)
        user = Userinfo.objects.get(username='testuser186')
        Topics.objects.create(topic_name="test_topic186", creator_name=user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic186")
        Bets.objects.create(topic_id_id=tpcid.topic_id, username_id=user, option="A", amount=100)
        Bets.objects.create(topic_id_id=tpcid.topic_id, username_id=user, option="A", amount=200)
        Bets.objects.create(topic_id_id=tpcid.topic_id, username_id=user, option="C", amount=300)
        response = db().dailybets()
        print("*****************DAAAAAAIIILLLLLLLLLLLLYYYYYYYYYY BBBBBEEEETSSSSSSSSS********************")
        self.assertEqual(response,{'2': {'option': {u'A': {'number_of_users': 2, 'amount__sum': 300}, u'C': {'number_of_users': 1, 'amount__sum': 300}}}})
        self.assertEqual(len(response),1)

    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="testuser895", password="Welcome2018",
                                            emailID="testuser895@gmail.com", balance = 200)
        self.user_dict = {"username": self.user.username}
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo',
                                          algorithm="HS256")


    def test_declare_winner_api(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        Topics.objects.create(topic_name="test_topic18975", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        self.tpcid = Topics.objects.get(topic_name="test_topic18975")
        Bets.objects.create(topic_id_id=self.tpcid.topic_id, username_id=self.user, option="A", amount=100)
        Bets.objects.create(topic_id_id=self.tpcid.topic_id, username_id=self.user, option="B", amount=200)
        Bets.objects.create(topic_id_id=self.tpcid.topic_id, username_id=self.user, option="C", amount=300)
        response = self.client.get('http://127.0.0.1:8000/api/v1/dailybets/')
        print("*****************decalre winner*******************")
        print(response)
        print("done")
        self.assertEqual(response.status_code, 200)