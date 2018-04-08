from django.test import TestCase
from beton.BusinessLayer.PlaceABet import PlaceABet as pb
from beton.models import Userinfo, Topics, BetInfo, Bets
import requests

class TestPlaceBet(TestCase):
    def test_get_option_list_blank(self):
        options = pb().get_option_list(1)
        self.assertEqual(options,list())

    def test_get_option_list_multiple(self):
        Userinfo.objects.create(username="testuser3", password="Welcome@2018", emailID="test@gmail.com")
        user = Userinfo.objects.get(username='testuser3')
        Topics.objects.create(topic_name="test_topic", creator_name=user, start_date="2017-11-21", end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic")
        Bets.objects.create(topic_id=tpcid, username=user, option='A', amount=140)
        Bets.objects.create(topic_id=tpcid, username=user, option='A', amount=140)
        Bets.objects.create(topic_id=tpcid, username=user, option='B', amount=140)
        Bets.objects.create(topic_id=tpcid, username=user, option='C', amount=140)
        options = pb().get_option_list(tpcid.topic_id)
        self.assertEqual(options,['A','B','C'])


    '''def test_place_a_bet(self):
        Userinfo.objects.create(username="testuser4", password="Welcome@2018", emailID="test@gmail.com")
        user = Userinfo.objects.get(username='testuser4')
        Topics.objects.create(topic_name="test_topic", creator_name=user, start_date="2017-11-21", end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic")
        BetInfo.objects.create(topic_id_id=tpcid.topic_id, option= 'A', total_amount=100, total_users=10)
        response = pb().place_a_bet(tpcid.topic_id,'testuser4', 'A', 100)
        self.assertEqual(response, "Success")
        bet = Bets.objects.filter(topic_id_id=tpcid.topic_id, username_id='testuser4', option='A', amount=100).values()
        self.assertEqual(bet[0]['topic_id_id'],tpcid.topic_id)
        self.assertEqual(bet[0]['username_id'],'testuser4')
        self.assertEqual(bet[0]['option'],'A')
        self.assertEqual(bet[0]['amount'],100)
        betinfo = BetInfo.objects.filter(topic_id_id=tpcid.topic_id, option= 'A').values()
        self.assertEqual(betinfo[0]['total_amount'],200)
        self.assertEqual(betinfo[0]['total_users'],11)'''

    def test_place_a_bet_nobetinfo(self):
        Userinfo.objects.create(username="testuser5", password="Welcome@2018", emailID="test@gmail.com")
        user = Userinfo.objects.get(username='testuser5')
        Topics.objects.create(topic_name="test_topic1", creator_name=user, start_date="2017-11-21", end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic1")
        response = pb().place_a_bet(tpcid.topic_id,'testuser5', 'A', 100)
        self.assertEqual(response, "Success")
        bet = Bets.objects.filter(topic_id_id=tpcid.topic_id, username_id='testuser5', option='A', amount=100).values()
        self.assertEqual(bet[0]['topic_id_id'],tpcid.topic_id)
        self.assertEqual(bet[0]['username_id'],'testuser5')
        self.assertEqual(bet[0]['option'],'A')
        self.assertEqual(bet[0]['amount'],100)
        betinfo = BetInfo.objects.filter(topic_id_id=tpcid.topic_id, option= 'A').values()
        self.assertEqual(betinfo[0]['total_amount'],200)
        self.assertEqual(betinfo[0]['total_users'],11)
