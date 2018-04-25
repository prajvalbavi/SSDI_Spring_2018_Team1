import jwt
from django.test import Client
from django.test import TestCase
from beton.models import BetOnAdmins as admins, Topics, BetInfo
from datetime import datetime, timedelta
from tests.utils import *

class AddBetRequest(TestCase):
    def setUp(self):
        self.is_admin = "true"
        self.client = Client()
        self.topic_name = "test topic"
        self.option_list = ['a', 'b']
        self.options = ",".join(self.option_list)
        self.creation_date = datetime.now()
        self.start_date = self.creation_date + timedelta(1)
        self.end_date = self.creation_date + timedelta(7)
        self.admin_identity = "test_admin"
        self.password = "test_password"
        self.secret_key = "test_secret_key"
        self.admin = admins.objects.create(admin_identity=self.admin_identity, password=self.password,
                                           secret_key=self.secret_key)
        self.token = jwt.encode({"username": "test_admin"}, 'ThisU$erI$LoggedInBetoInfo' +
                                self.secret_key, algorithm="HS256")
        self.client.defaults['HTTP_AUTHORIZATION'] = self.token
        Topics.objects.create(topic_name="Try to duplicate me", start_date="2018-05-02", end_date="2018-05-29",
                              date_of_creation="2018-04-29")

    def test_create_bet_success(self):
        response = self.client.post('http://localhost:8000/api/v1/addbet/',
                                    data={'is_admin': self.is_admin,
                                          'topicName': self.topic_name, 'options': self.options,
                                          'creationDate': str(self.creation_date.timestamp()),
                                          'startDate': str(self.start_date.timestamp()),
                                          'endDate': str(self.end_date.timestamp())
                                          })

        pay_load = get_dict_from_response(response)
        print(pay_load)
        self.assertTrue('status' in pay_load)
        self.assertTrue(pay_load['status'])
        self.assertTrue('message' in pay_load)
        self.assertTrue(pay_load['message'] == 'Bet saved')


        # Validate if topic in Db
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


    def test_create_bet_duplicate(self):
        response = self.client.post('http://localhost:8000/api/v1/addbet/',
                                    data={'is_admin': self.is_admin,
                                          'topicName': "Try to duplicate me", 'options': self.options,
                                          'creationDate': str(self.creation_date.timestamp()),
                                          'startDate': str(self.start_date.timestamp()),
                                          'endDate': str(self.end_date.timestamp())
                                          })

        pay_load = get_dict_from_response(response)
        self.assertTrue('status' in pay_load)
        self.assertFalse(pay_load['status'])
        self.assertTrue('message' in pay_load)
        self.assertTrue(pay_load['message'] == 'Topic already exists')


