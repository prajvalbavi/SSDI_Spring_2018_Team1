from django.test import TestCase
from beton.BusinessLayer.core.BetStats import BetStats
from beton.models import Userinfo, Topics, Bets, ClosedBets
import jwt
import json
from django.test import Client
from datetime import date

class TestBetStatsAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Userinfo.objects.create(username="testuser1", password="Welcome2018",
                                            emailID="testuser1@gmail.com", balance=100)
        self.valid_token = jwt.encode({'username': self.user.username}, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
        self.invalid_token = jwt.encode({'username': self.user.username}, 'meinvalidtoken', algorithm="HS256")

    def test_client_get_bet_stats(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.get('http://localhost:8000/api/v1/betstats/')
        res = response.json()
        self.assertEqual(res['status'], "success")
        res_json = json.loads(res['stats'])
        self.assertEqual(res_json['totalBets'], 0)
        self.assertEqual(res_json['activeBets'], 0)
        self.assertEqual(res_json['numberOfWins'], 0)
        self.assertEqual(res_json['numberOfLoss'], 0)
        self.assertEqual(res_json['totalWinAmount'], 0)
        self.assertEqual(res_json['totalLostAmount'], 0)

    def test_client_get_bet_stats_invalid_client(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = self.invalid_token
        response = self.client.get('http://localhost:8000/api/v1/betstats/')
        res = response.json()
        self.assertEqual(res['status'], "error")
        self.assertEqual(res['message'], "Invalid user")

    def test_client_get_bet_stats_singlebet_placed(self):
        Topics.objects.create(topic_name="test_topic186", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic186")
        Bets.objects.create(topic_id_id=tpcid.topic_id, username_id=self.user, option="A", amount=100)
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.get('http://localhost:8000/api/v1/betstats/')
        res = response.json()
        self.assertEqual(res['status'], "success")
        res_json = json.loads(res['stats'])
        self.assertEqual(res_json['totalBets'], 1)
        self.assertEqual(res_json['activeBets'], 1)
        self.assertEqual(res_json['numberOfWins'], 0)
        self.assertEqual(res_json['numberOfLoss'], 0)
        self.assertEqual(res_json['totalWinAmount'], 0)
        self.assertEqual(res_json['totalLostAmount'], 0)

    def test_client_get_bet_stats_multiplebet_placed(self):
        Topics.objects.create(topic_name="test_topic186", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic186")
        Topics.objects.create(topic_name="test_topic187", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid1 = Topics.objects.get(topic_name="test_topic187")
        Bets.objects.create(topic_id_id=tpcid.topic_id, username_id=self.user, option="A", amount=100)
        Bets.objects.create(topic_id_id=tpcid1.topic_id, username_id=self.user, option="B", amount=100)
        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.get('http://localhost:8000/api/v1/betstats/')
        res = response.json()
        self.assertEqual(res['status'], "success")
        res_json = json.loads(res['stats'])
        self.assertEqual(res_json['totalBets'], 2)
        self.assertEqual(res_json['activeBets'], 2)
        self.assertEqual(res_json['numberOfWins'], 0)
        self.assertEqual(res_json['numberOfLoss'], 0)
        self.assertEqual(res_json['totalWinAmount'], 0)
        self.assertEqual(res_json['totalLostAmount'], 0)

    def test_client_get_bet_stats_multiplebet_placed_one_win(self):
        Topics.objects.create(topic_name="test_topic186", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic186")
        Topics.objects.create(topic_name="test_topic187", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid1 = Topics.objects.get(topic_name="test_topic187")
        b1 = Bets.objects.create(topic_id_id=tpcid.topic_id, username_id=self.user, option="A", amount=100)
        b2 = Bets.objects.create(topic_id_id=tpcid1.topic_id, username_id=self.user, option="B", amount=100)
        ClosedBets.objects.create(bet_id=b1.bet_id, topic_id=b1.topic_id_id, username=b1.username_id, option=b1.option, amount=10, date_of_placing_bet=date.today(), win=1, win_lose_amount=10)
        Bets.objects.filter(topic_id=b1.topic_id).delete()


        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.get('http://localhost:8000/api/v1/betstats/')
        res = response.json()
        self.assertEqual(res['status'], "success")
        res_json = json.loads(res['stats'])
        self.assertEqual(res_json['totalBets'], 2)
        self.assertEqual(res_json['activeBets'], 1)
        self.assertEqual(res_json['numberOfWins'], 1)
        self.assertEqual(res_json['numberOfLoss'], 0)
        self.assertEqual(res_json['totalWinAmount'], 10)
        self.assertEqual(res_json['totalLostAmount'], 0)

    def test_client_get_bet_stats_multiplebet_placed_one_loss(self):
        Topics.objects.create(topic_name="test_topic186", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic186")
        Topics.objects.create(topic_name="test_topic187", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid1 = Topics.objects.get(topic_name="test_topic187")
        b1 = Bets.objects.create(topic_id_id=tpcid.topic_id, username_id=self.user, option="A", amount=100)
        b2 = Bets.objects.create(topic_id_id=tpcid1.topic_id, username_id=self.user, option="B", amount=100)
        ClosedBets.objects.create(bet_id=b1.bet_id, topic_id=b1.topic_id_id, username=b1.username_id, option=b1.option,amount=10, date_of_placing_bet=date.today(), win=0, win_lose_amount=10)
        Bets.objects.filter(topic_id=b1.topic_id).delete()

        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.get('http://localhost:8000/api/v1/betstats/')
        res = response.json()
        self.assertEqual(res['status'], "success")
        res_json = json.loads(res['stats'])
        self.assertEqual(res_json['totalBets'], 2)
        self.assertEqual(res_json['activeBets'], 1)
        self.assertEqual(res_json['numberOfWins'], 0)
        self.assertEqual(res_json['numberOfLoss'], 1)
        self.assertEqual(res_json['totalWinAmount'], 0)
        self.assertEqual(res_json['totalLostAmount'], 10)


    def test_client_get_bet_stats_multiplebet_placed_one_win_one_loss(self):
        Topics.objects.create(topic_name="test_topic186", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic186")
        Topics.objects.create(topic_name="test_topic187", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid1 = Topics.objects.get(topic_name="test_topic187")
        b1 = Bets.objects.create(topic_id_id=tpcid.topic_id, username_id=self.user, option="A", amount=100)
        b2 = Bets.objects.create(topic_id_id=tpcid1.topic_id, username_id=self.user, option="B", amount=100)
        ClosedBets.objects.create(bet_id=b1.bet_id, topic_id=b1.topic_id_id, username=b1.username_id, option=b1.option,amount=10, date_of_placing_bet=date.today(), win=0, win_lose_amount=10)
        ClosedBets.objects.create(bet_id=b2.bet_id, topic_id=b2.topic_id_id, username=b2.username_id, option=b1.option, amount=100, date_of_placing_bet=date.today(), win=1, win_lose_amount=10)
        Bets.objects.filter(topic_id=b1.topic_id).delete()
        Bets.objects.filter(topic_id=b2.topic_id).delete()

        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.get('http://localhost:8000/api/v1/betstats/')
        res = response.json()
        self.assertEqual(res['status'], "success")
        res_json = json.loads(res['stats'])
        self.assertEqual(res_json['totalBets'], 2)
        self.assertEqual(res_json['activeBets'], 0)
        self.assertEqual(res_json['numberOfWins'], 1)
        self.assertEqual(res_json['numberOfLoss'], 1)
        self.assertEqual(res_json['totalWinAmount'], 100)
        self.assertEqual(res_json['totalLostAmount'], 10)


    def test_client_get_bet_stats_multiplebet_placed_one_win_one_loss(self):
        Topics.objects.create(topic_name="test_topic186", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic186")
        Topics.objects.create(topic_name="test_topic187", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid1 = Topics.objects.get(topic_name="test_topic187")
        Topics.objects.create(topic_name="test_topic188", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid2 = Topics.objects.get(topic_name="test_topic188")
        b1 = Bets.objects.create(topic_id_id=tpcid.topic_id, username_id=self.user, option="A", amount=100)
        b2 = Bets.objects.create(topic_id_id=tpcid1.topic_id, username_id=self.user, option="B", amount=100)
        b2 = Bets.objects.create(topic_id_id=tpcid2.topic_id, username_id=self.user, option="C", amount=100)

        ClosedBets.objects.create(bet_id=b1.bet_id, topic_id=b1.topic_id_id, username=b1.username_id, option=b1.option,amount=10, date_of_placing_bet=date.today(), win=0, win_lose_amount=10)
        ClosedBets.objects.create(bet_id=b2.bet_id, topic_id=b2.topic_id_id, username=b2.username_id, option=b1.option, amount=100, date_of_placing_bet=date.today(), win=1, win_lose_amount=10)
        Bets.objects.filter(topic_id=b1.topic_id).delete()
        Bets.objects.filter(topic_id=b2.topic_id).delete()

        self.client.defaults['HTTP_AUTHORIZATION'] = self.valid_token
        response = self.client.get('http://localhost:8000/api/v1/betstats/')
        res = response.json()
        self.assertEqual(res['status'], "success")
        res_json = json.loads(res['stats'])
        self.assertEqual(res_json['totalBets'], 3)
        self.assertEqual(res_json['activeBets'], 1)
        self.assertEqual(res_json['numberOfWins'], 1)
        self.assertEqual(res_json['numberOfLoss'], 1)
        self.assertEqual(res_json['totalWinAmount'], 100)
        self.assertEqual(res_json['totalLostAmount'], 10)


class TestBetStats(TestCase):
    def setUp(self):
        self.user = Userinfo.objects.create(username="testuser1", password="Welcome2018",
                                            emailID="testuser1@gmail.com", balance=100)



    def test_bet_stats(self):
        stats = BetStats(self.user.username)
        result = stats.get_peruser_betStats()
        self.assertEqual(result['totalBets'], 0)
        self.assertEqual(result['activeBets'], 0)
        self.assertEqual(result['numberOfWins'], 0)
        self.assertEqual(result['numberOfLoss'], 0)
        self.assertEqual(result['totalWinAmount'], 0)
        self.assertEqual(result['totalLostAmount'], 0)


    def test_bets_stats_multiple_bets(self):
        Topics.objects.create(topic_name="test_topic186", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid = Topics.objects.get(topic_name="test_topic186")
        Topics.objects.create(topic_name="test_topic187", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid1 = Topics.objects.get(topic_name="test_topic187")
        Topics.objects.create(topic_name="test_topic188", creator_name=self.user, start_date="2017-11-21",
                              end_date="2017-11-21", date_of_creation="2017-11-21")
        tpcid2 = Topics.objects.get(topic_name="test_topic188")
        b1 = Bets.objects.create(topic_id_id=tpcid.topic_id, username_id=self.user, option="A", amount=100)
        b2 = Bets.objects.create(topic_id_id=tpcid1.topic_id, username_id=self.user, option="B", amount=100)
        b2 = Bets.objects.create(topic_id_id=tpcid2.topic_id, username_id=self.user, option="C", amount=100)

        ClosedBets.objects.create(bet_id=b1.bet_id, topic_id=b1.topic_id_id, username=b1.username_id, option=b1.option,
                                  amount=10, date_of_placing_bet=date.today(), win=0, win_lose_amount=10)
        ClosedBets.objects.create(bet_id=b2.bet_id, topic_id=b2.topic_id_id, username=b2.username_id, option=b1.option,
                                  amount=100, date_of_placing_bet=date.today(), win=1, win_lose_amount=10)
        Bets.objects.filter(topic_id=b1.topic_id).delete()
        Bets.objects.filter(topic_id=b2.topic_id).delete()

        stats = BetStats(self.user.username)
        result = stats.get_peruser_betStats()
        self.assertEqual(result['totalBets'], 3)
        self.assertEqual(result['activeBets'], 1)
        self.assertEqual(result['numberOfWins'], 1)
        self.assertEqual(result['numberOfLoss'], 1)
        self.assertEqual(result['totalWinAmount'], 100)
        self.assertEqual(result['totalLostAmount'], 10)



