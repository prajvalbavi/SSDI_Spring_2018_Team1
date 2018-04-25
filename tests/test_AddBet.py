from django.test import TestCase
from beton.BusinessLayer.core.AddBet import AddBet
from datetime import datetime, timedelta
from beton.models import Topics
from beton.models import BetInfo

class TestAddBest(TestCase):
    def setUp(self):
        self.topic_name = "test topic"
        self.option_list = ['a', 'b']
        self.options = ",".join(self.option_list)
        self.creation_date = datetime.now()
        self.start_date = self.creation_date + timedelta(1)
        self.end_date = self.creation_date + timedelta(7)
        self.bet = AddBet()

    def test_addBet_success(self):
        flag, message = self.bet.add_a_bet(self.topic_name, self.options, self.start_date.timestamp(), self.end_date.timestamp(),
                                           self.creation_date.timestamp())

        self.assertTrue(flag)
        self.assertTrue(message == "Bet saved")

        #Validate if topic in Db
        try:
            obj = Topics.objects.get(topic_name__iexact=self.topic_name)
            self.assertTrue(obj.topic_name.lower() == self.topic_name.lower())

            topic_id = obj.topic_id

            options = BetInfo.objects.filter(topic_id_id=topic_id)
            print('type of options', options)
            for option in options:
                self.assertTrue(option.option in self.option_list)

        except Exception as e:
            print(str(e))
            self.assertTrue(False)

    def test_addBet_duplicate(self):
        flag, message = self.bet.add_a_bet(self.topic_name, self.options, self.start_date.timestamp(),
                                           self.end_date.timestamp(),
                                           self.creation_date.timestamp())

        self.assertTrue(flag)
        self.assertTrue(message == "Bet saved")

        flag, message = self.bet.add_a_bet(self.topic_name, self.options, self.start_date.timestamp(),
                                           self.end_date.timestamp(),
                                           self.creation_date.timestamp())

        print(flag, message)
        self.assertFalse(flag)
        self.assertTrue(message = "Topic already exists")


