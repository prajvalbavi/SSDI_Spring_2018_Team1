from django.test import TestCase
from beton.BusinessLayer.GetBetDetails import BetDetails as bd
from beton.BusinessLayer.PlaceABet import PlaceABet as pb
from beton.BusinessLayer.UserBetDetails import UserBetDetials
from beton.models import Userinfo, Topics, BetInfo, Bets
import requests

class TestPerUserBetDetails(TestCase):
    def test_per_user_bets_blank(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        res_status, bet_list = UserBetDetials.get_peruser_bets("testuser1")
        self.assertTrue(res_status, "success")
        self.assertEqual(len(bet_list), 0)

    def test_per_user_bets_single(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        user = Userinfo.objects.get(username='testuser1')
        Topics.objects.create(topic_name="xyz", creator_name=user, start_date="2017-11-21", end_date="2017-11-21",
                              date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="xyz")
        pb().place_a_bet(tpcid.topic_id, 'testuser1', 'A', 100)
        res_status, bet_list = UserBetDetials.get_peruser_bets("testuser1")
        self.assertTrue(res_status, "success")
        self.assertEqual(len(bet_list), 1)
        _betlist = bet_list[0]
        self.assertEqual(_betlist.amount, 100)
        self.assertEqual(_betlist.option, "A")
        self.assertNotEquals(_betlist.bet_id, 0)
        self.assertNotEquals(_betlist.topic_id_id, 0)
        self.assertEqual(_betlist.username_id, "testuser1")



