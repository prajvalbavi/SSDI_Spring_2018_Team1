from django.test import TestCase
from beton.BusinessLayer.GetBetDetails import BetDetails as bd
from beton.models import Userinfo, Topics, BetInfo, Bets
import requests
import jwt
from django.test import Client

class TestBetDetails(TestCase):
    def test_get_bet_details_blank_data(self):
        details = bd().get_bet_details(1)
        self.assertEqual(details,dict())

    def test_get_bet_details_one_row(self):
        Userinfo.objects.create(username="testuser1", password="Welcome@2018", emailID="test@gmail.com")
        user = Userinfo.objects.get(username='testuser1')
        Topics.objects.create(topic_name = "xyz", creator_name = user, start_date = "2017-11-21", end_date = "2017-11-21", date_of_creation = "2017-11-21")
        tpcid = Topics.objects.get(topic_name = "xyz")
        Bets.objects.create(topic_id = tpcid, username = user, option = 'A', amount = 140)
        Bets.objects.create(topic_id = tpcid, username = user, option = 'A', amount = 140)
        details = bd().get_bet_details(tpcid.topic_id)
        self.assertEqual(len(details), 1)
        self.assertEqual(details.keys(), ['A'])
        self.assertEqual(details['A']['number_of_users'], 2)
        self.assertEqual(details['A']['amount__sum'], 280)


    def test_get_bet_details_multiple_rows(self):
        Userinfo.objects.create(username="testuser2", password="Welcome@2018", emailID="test@gmail.com")
        user = Userinfo.objects.get(username='testuser2')
        Topics.objects.create(topic_name = "abc", creator_name = user, start_date = "2017-11-21", end_date = "2017-11-21", date_of_creation = "2017-11-21")
        tpcid = Topics.objects.get(topic_name = "abc")
        Bets.objects.create(topic_id = tpcid, username = user, option = 'A', amount = 100)
        Bets.objects.create(topic_id = tpcid, username = user, option = 'A', amount = 15)
        Bets.objects.create(topic_id = tpcid, username = user, option = 'B', amount = 200)
        Bets.objects.create(topic_id = tpcid, username = user, option = 'B', amount = 15)
        details = bd().get_bet_details(tpcid.topic_id)
        self.assertEqual(len(details), 2)
        self.assertEqual(details.keys(), ['A', 'B'])
        self.assertEqual(details['A']['number_of_users'], 2)
        self.assertEqual(details['A']['amount__sum'], 115)
        self.assertEqual(details['B']['number_of_users'], 2)
        self.assertEqual(details['B']['amount__sum'], 215)

    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="testuser1", password="Welcome2018",
                                            emailID="testuser1@gmail.com")
        self.user_dict = {"username": self.user.username}
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo',
                                          algorithm="HS256")


    def test_place_a_bet_api(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.post('http://127.0.0.1:8000/api/v1/placebet/?topic_id=3&username=apurva&option=Z&amount=40')
        self.assertEqual(response.status_code, 200)
        Bets.objects.filter(topic_id_id=100, username_id='apurva', option='Z', amount=40).delete()
        BetInfo.objects.filter(topic_id_id=100, option='Z').delete()

    def test_get_bet_details_multiple_rows_api(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.post('http://127.0.0.1:8000/api/v1/betdetails/?topic_id=1')
        details = response.json()
        print (details)git res
        '''self.assertEqual(len(details), 2)
        self.assertEqual(details.keys(), ['A', 'B'])
        self.assertEqual(details['A']['number_of_users'], 2)
        self.assertEqual(details['A']['amount__sum'], 211)
        self.assertEqual(details['B']['number_of_users'], 2)
        self.assertEqual(details['B']['amount__sum'], 211)'''