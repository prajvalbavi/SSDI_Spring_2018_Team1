from django.test import TestCase
from beton.BusinessLayer.core.FetchBalance import FetchBalance as fb
from beton.models import Userinfo, Topics, BetInfo, Bets
import requests
import jwt
from django.test import Client



class TestFetchBalance(TestCase):
    def test_fetch_balance(self):
        Userinfo.objects.create(username="testuser500", password="Welcome@2018", emailID="test@gmail.com", balance=500)
        balance = fb().fetch_balance('testuser500')
        self.assertEqual(balance,500)

    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="testuser400", password="Welcome2018",
                                            emailID="testuser400@gmail.com", balance = 200)
        self.user_dict = {"username": self.user.username}
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo',
                                          algorithm="HS256")


    def test_fetch_balance_api(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.get('http://127.0.0.1:8000/api/v1/fetch_balance/?username=testuser400')
        print("*****************Fetch Balance*******************")
        print(response)
        print("done")
        self.assertEqual(response.status_code, 200)