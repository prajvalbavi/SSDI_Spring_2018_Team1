from django.test import TestCase
from beton.BusinessLayer.core.FetchBalance import FetchBalance
from beton.models import Userinfo, Topics, BetInfo, Bets
import requests
import jwt
from django.test import Client



class TestMakePaymentAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="testuser1", password="Welcome2018",
                                            emailID="testuser1@gmail.com", balance=100)
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")

    def test_client_no_bets_api(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        self.amount = {"amount": 1}
        response = self.client.post('http://localhost:8000/api/v1/makepayment/', self.amount)
        print(response)

