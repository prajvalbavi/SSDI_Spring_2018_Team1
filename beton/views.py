from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from rest_framework.decorators import api_view

from beton.models import Userinfo, Topics, BetInfo
from beton.serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from django.core import serializers
import json
from beton.BusinessLayer.SignupUser import SignupUser
from beton.BusinessLayer.GetPublicTopics import BetInformation
from beton.BusinessLayer.CheckUser import  CheckUser
# Create your views here.



@api_view(['GET'])
def get_user(request):
    if request.method == 'GET':
        posts = Userinfo.objects.all()
        json_data = serializers.serialize('json', posts, fields=('username','password','emailID'))
        return HttpResponse(json_data, content_type="application/json")

@api_view(['POST'])
def post_signup(request):
    if request.method == 'POST':
        messagedict = {}
        request_data = request.POST
        print("Username" , request_data.get('username'))
        print("Password", request_data.get('password'))
        print("Email", request_data.get('email'))
        status, message = SignupUser.signup(request_data.get('username'), request_data.get('password'),
                                            request_data.get('email') )
        messagedict['message'] = message
        messagedict['status'] = status
        messagedict['email_id'] = request_data.get('email')
        messagedict['username'] = request_data.get('username')

        server_message = json.dumps(messagedict)
        print(server_message)
        print(request.POST)
        return HttpResponse(server_message, content_type="application/json")


@api_view(['GET'])
def get_topics(request):
    if request.method == 'GET':
        topics = Topics.objects.all()
        json_data = serializers.serialize('json', topics, fields=('topic_id','topic_name','creator_name','start_date','end_date','date_of_creation'))
        return HttpResponse(json_data, content_type="application/json")


@api_view(['GET'])
def get_betinfo(request):
    if request.method == 'GET':
        topics_info = BetInfo.objects.all()
        json_data = serializers.serialize('json', topics_info, fields=('bet_id','topic_id','option','total_amount','total_users'))
        return HttpResponse(json_data, content_type="application/json")


@api_view(['GET'])
def get_bet_topics_and_info(request):
    if request.method == 'GET':
        b = BetInformation()
        message_dict = b.get_info_by_topic()
        new_dict = {'topics': [value for key, value in message_dict.items()]}
        print(new_dict)
        server_message = json.dumps(new_dict)
        return HttpResponse(server_message, content_type="application/json")

@api_view(['POST'])
def post_edituserdetails(request):
    if request.method == 'POST':
        print("Post hit")
        request_data = request.POST
        print("Username", request_data.get('username'))
        print("Password", request_data.get('password'))
        print("Email", request_data.get('email'))
        status, status_msg = CheckUser.check_user(request_data.get('username'), request_data.get('password'), request_data.get('email'))
        if "error" in status:
            new_dict = {'status': status, 'message': status_msg}
        else:
            status, status_msg = CheckUser.update_user(request_data.get('username'), request_data.get('password'), request_data.get('email'))
            new_dict = {'status': status, 'message': status_msg}

        server_message = json.dumps(new_dict)
        return HttpResponse(server_message, content_type="application/json")

@api_view(["GET"])
def post_betdetails(request):
    if request.method == 'GET':
        new_dict = {'topic':'Hello', 'option':'No', 'amount':100}
        my_dict = {"betdetails": [new_dict, new_dict]}
        server_message = json.dumps(my_dict)
        return HttpResponse(server_message, content_type="application/json")