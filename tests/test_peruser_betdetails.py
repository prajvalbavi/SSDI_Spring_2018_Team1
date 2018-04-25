from django.test import TestCase
from beton.BusinessLayer.core.GetBetDetails import BetDetails as bd
from beton.BusinessLayer.core.PlaceABet import PlaceABet as pb
from beton.BusinessLayer.core.UserBetDetails import UserBetDetials
from beton.models import Userinfo, Topics, BetInfo, Bets
import requests
import jwt
from django.test import Client

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
        self.assertEqual(_betlist['amount'], 100)
        self.assertEqual(_betlist['option'], "A")
        self.assertNotEquals(_betlist['bet_id'], 0)
        self.assertNotEquals(_betlist['topic_id_id'], 0)
        self.assertEqual(_betlist['username_id'], "testuser1")

    def test_per_user_bets_multiple(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        user = Userinfo.objects.get(username='testuser1')
        Topics.objects.create(topic_name="xyz", creator_name=user, start_date="2017-11-21", end_date="2017-11-21",
                              date_of_creation="2017-11-21")
        Topics.objects.create(topic_name="xyz1", creator_name=user, start_date="2017-11-21", end_date="2017-11-21",
                              date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="xyz")
        pb().place_a_bet(tpcid.topic_id, 'testuser1', 'A', 100)
        tpcid1 = Topics.objects.get(topic_name="xyz1")
        pb().place_a_bet(tpcid1.topic_id, 'testuser1', 'B', 200)
        res_status, bet_list = UserBetDetials.get_peruser_bets("testuser1")
        self.assertTrue(res_status, "success")
        self.assertEqual(len(bet_list), 2)
        _betlist = bet_list[0]
        self.assertEqual(_betlist['amount'], 100)
        self.assertEqual(_betlist['option'], "A")
        self.assertNotEquals(_betlist['bet_id'], 0)
        self.assertNotEquals(_betlist['topic_id_id'], 0)
        self.assertEqual(_betlist['username_id'], "testuser1")

        _betlist = bet_list[1]
        self.assertEqual(_betlist['amount'], 200)
        self.assertEqual(_betlist['option'], "B")
        self.assertNotEquals(_betlist['bet_id'], 0)
        self.assertNotEquals(_betlist['topic_id_id'], 0)
        self.assertEqual(_betlist['username_id'], "testuser1")

class TestPerUserBetDetailsAPI(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="testuser1", password="Welcome2018",
                                            emailID="testuser1@gmail.com")
        self.user_dict = {"username": self.user.username}
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
        self.invalid_token = jwt.encode({'username': self.user.username}, 'meinvalidtoken', algorithm="HS256")

    def test_client_no_bets_api(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.post('http://localhost:8000/api/v1/userbetdetails/', self.user_dict)
        res = response.json()
        self.assertEqual(res['status'], "success")
        self.assertEqual(len(res['user_bets_info']), 0)

    def test_client_no_bets_invalid_api(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.invalid_token
        response = self.client.post('http://localhost:8000/api/v1/userbetdetails/', self.user_dict)
        res = response.json()
        self.assertEqual(res['status'], "error")
        self.assertEqual(res['message'], "Invalid User")

    def test_client_no_bets_no_header_api(self):
        response = self.client.post('http://localhost:8000/api/v1/userbetdetails/', self.user_dict)
        res = response.json()
        self.assertEqual(res['status'], "error")
        self.assertEqual(res['message'], "Header not found, user will not be authenticated.")

    def test_client_single_bets_api(self):
        Topics.objects.create(topic_name="xyz", creator_name=self.user, start_date="2017-11-21", end_date="2017-11-21",
                              date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="xyz")
        pb().place_a_bet(tpcid.topic_id, 'testuser1', 'A', 100)

        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.post('http://localhost:8000/api/v1/userbetdetails/', self.user_dict)
        res = response.json()
        self.assertEqual(res['status'], "success")
        self.assertEqual(len(res['user_bets_info']), 1)
        _betlist = res['user_bets_info'][0]
        self.assertEqual(_betlist['amount'], 100)
        self.assertEqual(_betlist['option'], "A")
        self.assertNotEquals(_betlist['bet_id'], 0)
        self.assertNotEquals(_betlist['topic_id_id'], 0)
        self.assertEqual(_betlist['username_id'], "testuser1")

    def test_client_multiple_bets_api(self):
        Topics.objects.create(topic_name="xyz", creator_name=self.user, start_date="2017-11-21", end_date="2017-11-21",
                              date_of_creation="2017-11-21")
        Topics.objects.create(topic_name="xyz1", creator_name=self.user, start_date="2017-11-21", end_date="2017-11-21",
                              date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="xyz")
        pb().place_a_bet(tpcid.topic_id, 'testuser1', 'A', 100)
        tpcid1 = Topics.objects.get(topic_name="xyz1")
        pb().place_a_bet(tpcid1.topic_id, 'testuser1', 'B', 200)
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.post('http://localhost:8000/api/v1/userbetdetails/', self.user_dict)
        res = response.json()

        self.assertEqual(res['status'], "success")
        self.assertEqual(len(res['user_bets_info']), 2)

        _betlist = res['user_bets_info'][0]
        self.assertEqual(_betlist['amount'], 100)
        self.assertEqual(_betlist['option'], "A")
        self.assertNotEquals(_betlist['bet_id'], 0)
        self.assertNotEquals(_betlist['topic_id_id'], 0)
        self.assertEqual(_betlist['username_id'], "testuser1")

        _betlist = res['user_bets_info'][1]
        self.assertEqual(_betlist['amount'], 200)
        self.assertEqual(_betlist['option'], "B")
        self.assertNotEquals(_betlist['bet_id'], 0)
        self.assertNotEquals(_betlist['topic_id_id'], 0)
        self.assertEqual(_betlist['username_id'], "testuser1")



