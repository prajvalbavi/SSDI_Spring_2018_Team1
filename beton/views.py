import json

from django.shortcuts import render, render_to_response
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view
from beton.BusinessLayer.core.CheckUser import CheckUser
from beton.BusinessLayer.core.GetBetDetails import BetDetails
from beton.BusinessLayer.core.GetPublicTopics import BetInformation
from beton.BusinessLayer.core.PlaceABet import PlaceABet
from beton.BusinessLayer.core.SignupUser import SignupUser
from beton.BusinessLayer.core.UserBetDetails import UserBetDetials
from beton.BusinessLayer.core.DailyBets import DailyBets
from beton.BusinessLayer.core.DeclareWinner import DeclareWinner
from beton.BusinessLayer.core.FetchBalance import FetchBalance
from beton.models import Userinfo, Topics, BetInfo, Bets
from beton.BusinessLayer.core.utils import Utils


# Create your views here.

#Checks token is valid and if username or email matches with decoded name in token.
@api_view(['POST'])
def get_user(request):
    if request.method == 'POST':
        print(request.POST)
        server_message = CheckUser.get_user(request.POST.get('username'))
        json_server_message = json.dumps(server_message)
        return HttpResponse(json_server_message, content_type="application/json")


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
        is_valid_user, message = Utils.validate_user(request)
        if is_valid_user:
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
        else:
            new_dict = {'status': "error", 'message': message}

        server_message = json.dumps(new_dict)
        return HttpResponse(server_message, content_type="application/json")

@api_view(["POST"])
def post_user_betdetails(request):
    if request.method == 'POST':
        print("POST hit for user_betdetails")
        print("Validate user")
        is_valid_user, message = Utils.validate_user(request)
        if is_valid_user:
            status, betlist = UserBetDetials.get_peruser_bets(request.POST.get('username'))
            if len(betlist) > 0:
                #_betdetails = [_b for _b in betlist.values()]
                print(betlist)
                _betdetails = betlist
            else:
                _betdetails = []
            server_message = json.dumps({'status': status, 'user_bets_info': _betdetails}, default=str)
        else:
            status = "error"
            server_message = json.dumps({'status':status, 'message': message})

        return HttpResponse(server_message, content_type="application/json")




@api_view(["POST"])
def post_makepayment(request):
    if request.method == 'POST':
        print("POST hit for post_makepayment")
        print("Validate user")
        is_valid_user, message = Utils.validate_user(request)
        if is_valid_user:
            server_message = json.dumps({'status':'ok', 'message':'ok'})
        else:
            server_message = json.dumps({'status': 'error', 'message': 'ok'})
        return HttpResponse(server_message, content_type="application/json")


@api_view(['POST'])
def auth_user(request):
    if request.method == 'POST':
        print ('authenticating user', request.POST)
        flag, token = Utils.generate_token(request.POST)
        if flag:
            jwt_token = {'token': token}
            print (json.dumps(jwt_token))
            return HttpResponse(json.dumps(jwt_token), content_type="application/json")
        else:
            error_message = {'errors':{'form' : "Invalid Credentials"}}
            error_message = json.dumps(error_message)
            print (error_message)
            return HttpResponse(error_message, content_type="application/json", status=401)


@api_view(['POST'])
def validate_user(request):
    if request.method == 'POST':
        print("Received request to validate_user", request.POST, request.POST.get('is_admin'));

        is_valid_user, message = Utils.validate_user(request)
        json_reply = {'isValid': is_valid_user}
        print ("Validate_user response message" , json_reply)
        json_reply = json.dumps(json_reply)
        status_ = 200 if is_valid_user else 401
        print ('*status*', status_)
        return HttpResponse(json_reply, content_type="application/json", status = status_)


@api_view(['GET'])
def get_bet_details(request):
    if request.method == 'GET':
            b = BetDetails()
            options = b.get_bet_details(request.GET['topic_id'])
            json_data = json.dumps(options)
    else:
            status = "error"
            json_data = json.dumps({'status':status, 'message': message})
    return HttpResponse(json_data, content_type="application/json")


@api_view(['GET'])
def place_a_bet(request):
    if request.method == 'GET':
        is_valid_user, message = Utils.validate_user(request)
        if is_valid_user:
            p = PlaceABet()
            response = p.place_a_bet(request.GET['topic_id'], request.GET['username'], request.GET['option'], request.GET['amount'])
            json_data = json.dumps(response)
        else:
            status = "error"
            json_data = json.dumps({'status':status, 'message': message})
        return HttpResponse(json_data, content_type="application/json")


@api_view(['GET'])
def fetch_balance(request):
    if request.method == 'GET':
        is_valid_user, message = Utils.validate_user(request)
        if is_valid_user:
            p = FetchBalance()
            response = p.fetch_balance(request.GET['username'])
            json_data = json.dumps(response)
        else:
            status = "error"
            json_data = json.dumps({'status':status, 'message': message})
        return HttpResponse(json_data, content_type="application/json")


@api_view(['GET'])
def dailybets(request):
    if request.method == 'GET':
        is_valid_user, message = Utils.validate_user(request)
        #if is_valid_user:
        p = DailyBets()
        response = p.dailybets()
        json_data = json.dumps(response)
        #else:
        #    status = "error"
        #    json_data = json.dumps({'status':status, 'message': message})
        return HttpResponse(json_data, content_type="application/json")


@api_view(['GET'])
def declare_winner(request):
    if request.method == 'GET':
        is_valid_user, message = Utils.validate_user(request)
        if is_valid_user:
            p = DeclareWinner()
            response = p.declare_winner(request.GET['topic_id'], request.GET['option'])
            json_data = json.dumps(response)
        else:
            status = "error"
            json_data = json.dumps({'status':status, 'message': message})
        return HttpResponse(json_data, content_type="application/json")

