from django.test import TestCase
from beton.BusinessLayer.core.AdminGetTopics import AdminGetTopics
from beton.models import BetOnAdmins as admins, Topics, BetInfo
import jwt
import json
from django.test import Client
from datetime import datetime, timedelta, date
from tests.utils import *

class TestAdminCreatedTopicAPI(TestCase):
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




    def test_get_topics_not_created_today(self):
        response = self.client.get('http://localhost:8000/api/v1/admincreatedtopics/')
        res = response.json()
        self.assertEqual(res['status'], "success")
        self.assertEqual(len(res['topics']), 0)

    def test_get_topics_created_today_single(self):
        Topics.objects.create(topic_name="Try to duplicate me", start_date="2018-05-02", end_date="2018-05-09",
                              date_of_creation=date.today())
        response = self.client.get('http://localhost:8000/api/v1/admincreatedtopics/')
        res = response.json()
        self.assertEqual(res['status'], "success")
        self.assertEqual(len(res['topics']), 1)
        self.assertEqual(res['topics'][0], "Try to duplicate me")

    def test_get_topics_created_today_multiple(self):
        Topics.objects.create(topic_name="Try to duplicate me", start_date="2018-05-02", end_date="2018-05-09",
                              date_of_creation=date.today())
        Topics.objects.create(topic_name="I did duplicate you", start_date="2018-05-02", end_date="2018-05-09",
                              date_of_creation=date.today())
        response = self.client.get('http://localhost:8000/api/v1/admincreatedtopics/')
        res = response.json()
        self.assertEqual(res['status'], "success")
        self.assertEqual(len(res['topics']), 2)
        self.assertEqual(res['topics'][0], "Try to duplicate me")
        self.assertEqual(res['topics'][1], "I did duplicate you")

class TestAdminCreated(TestCase):
    def test_get_topics_not_created_today(self):
        Topics.objects.create(topic_name="Try to duplicate me", start_date="2018-05-02", end_date="2018-05-29",
                              date_of_creation="2018-04-29")
        status, _list = AdminGetTopics.get_topics(date.today())
        self.assertEqual(status, "success")
        self.assertEqual(len(_list), 0)

    def test_get_topics_created_today_single(self):
        Topics.objects.create(topic_name="Try to duplicate me", start_date="2018-05-02", end_date="2018-05-29",
                              date_of_creation=date.today())
        status, _list = AdminGetTopics.get_topics(date.today())
        self.assertEqual(status, "success")
        self.assertEqual(len(_list), 1)
        self.assertEqual(_list[0], "Try to duplicate me")

    def test_get_topics_created_today_multiple(self):
        Topics.objects.create(topic_name="Try to duplicate me", start_date="2018-05-02", end_date="2018-05-29",
                              date_of_creation=date.today())
        Topics.objects.create(topic_name="Did duplicate you", start_date="2018-05-02", end_date="2018-05-29",
                              date_of_creation=date.today())
        Topics.objects.create(topic_name="Try to duplicate me, again ?", start_date="2018-05-02", end_date="2018-05-29",
                              date_of_creation="2018-05-02")
        status, _list = AdminGetTopics.get_topics(date.today())
        self.assertEqual(status, "success")
        self.assertEqual(len(_list), 2)
        self.assertEqual(_list[0], "Try to duplicate me")
        self.assertEqual(_list[1], "Did duplicate you")






