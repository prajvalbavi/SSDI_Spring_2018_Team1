from django.test import TestCase
from beton.BusinessLayer.core.FetchBalance import FetchBalance
from beton.models import Userinfo
import jwt
from django.test import Client



class TestMakePaymentAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="testuser1", password="Welcome2018",
                                            emailID="testuser1@gmail.com", balance=100)
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
        self.invalid_token = jwt.encode({'username': self.user.username}, 'meinvalidtoken', algorithm="HS256")

    def test_client_make_payment_success(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        self.amount = {"amount": 1}
        response = self.client.post('http://localhost:8000/api/v1/makepayment/', self.amount)
        res = response.json()
        self.assertEqual(res['status'], "success")
        self.assertEqual(res['message'], "Payment Successful :) Happy Betting :)")
        self.assertEqual(FetchBalance().fetch_balance("testuser1"), 110)
        self.user.balance = 100


    def test_client_make_payment_invalid_user(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.invalid_token
        self.amount = {"amount": 1}
        response = self.client.post('http://localhost:8000/api/v1/makepayment/', self.amount)
        res = response.json()
        self.assertEqual(res['status'], "error")
        self.assertEqual(res['message'], "Invalid user")

    def test_client_make_payment_failure(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        self.amount = {"amount" : 1}
        count = 1
        for i in range(10):
            response = self.client.post('http://localhost:8000/api/v1/makepayment/', self.amount)
            res = response.json()
            if res['status'] == 'error':
                self.assertEqual(res['status'], "error")
                self.assertEqual(res['message'], "Payment failure :( Try, try, but never cry :)")
            else:
                self.assertEqual(res['status'], "success")
                self.assertEqual(res['message'], "Payment Successful :) Happy Betting :)")
                self.assertEqual(FetchBalance().fetch_balance("testuser1"), 100 + 10 * count)
                count = count + 1


class TestMakePayment(TestCase):
    def setUp(self):
        self.user = Userinfo.objects.create(username="testuser1", password="Welcome2018",
                                            emailID="testuser1@gmail.com", balance=100)


    def test_make_payment_topup_balance(self):
        self.assertEqual(FetchBalance().fetch_balance("testuser1"), 100)
        status, message = FetchBalance().topup_balance("testuser1", 110)
        self.assertEqual(status, "success")
        self.assertEqual(message, "Payment Successful :) Happy Betting :)")
        self.assertEqual(FetchBalance().fetch_balance("testuser1"), 110)


    def test_make_payment_topup_balance_invalid(self):
        self.assertEqual(FetchBalance().fetch_balance("testuser1"), 100)
        status, message = FetchBalance().topup_balance("testuser2", 110)
        self.assertEqual(status, "error")
        self.assertEqual(message, "Payment Updation failure")
        self.assertEqual(FetchBalance().fetch_balance("testuser1"), 100)

