from django.test import TestCase
from beton.BusinessLayer.GetBetDetails import BetDetails as bd
from beton.models import Userinfo, Topics, BetInfo, Bets
import requests

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

    def test_get_bet_details_blank_data_api(self):
        response = requests.get('http://127.0.0.1:8000/api/v1/betdetails/?topic_id=100')
        details = response.json()
        self.assertEqual(details,dict())

    def test_get_bet_details_one_row_api(self):
        response = requests.get('http://127.0.0.1:8000/api/v1/betdetails/?topic_id=2')
        details = response.json()
        self.assertEqual(len(details), 1)
        self.assertEqual(details.keys(), ['A'])
        self.assertEqual(details['A']['number_of_users'], 1)
        self.assertEqual(details['A']['amount__sum'], 100)



    def test_get_bet_details_multiple_rows_api(self):
        response = requests.get('http://127.0.0.1:8000/api/v1/betdetails/?topic_id=1')
        details = response.json()
        self.assertEqual(len(details), 2)
        self.assertEqual(details.keys(), ['A', 'B'])
        self.assertEqual(details['A']['number_of_users'], 2)
        self.assertEqual(details['A']['amount__sum'], 211)
        self.assertEqual(details['B']['number_of_users'], 2)
        self.assertEqual(details['B']['amount__sum'], 211)