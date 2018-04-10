from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from rest_framework.decorators import api_view

from beton.models import Userinfo, Topics, BetInfo, Bets
from beton.serializers import PostSerializer
from rest_framework.renderers import JSONRenderer
from django.core import serializers
import json
from beton.BusinessLayer.SignupUser import SignupUser
from beton.BusinessLayer.GetPublicTopics import BetInformation


from beton.BusinessLayer.AuthenticateUser import Authenticate
from beton.BusinessLayer.ValidateUser import Validate
from rest_framework.authentication import get_authorization_header

from beton.BusinessLayer.GetBetDetails import BetDetails
from beton.BusinessLayer.PlaceABet import PlaceABet
from beton.BusinessLayer.CheckUser import  CheckUser
from beton.BusinessLayer.UserBetDetails import UserBetDetials
# Create your views here.

#Checks token is valid and if username or email matches with decoded name in token.
def util_validate_user(request):
    try:
        auth = get_authorization_header(request)
        auth = auth.decode('utf-8')
        if "Bearer" in auth:
            auth = auth.split(" ")[1]
            print("Bearer in auth, so stripping it", auth)
        print("Final bearer", auth)
        is_valid_user = False
        message = ''
        if auth:
            is_valid_user, message = Validate.is_user_valid(auth)
            return is_valid_user, message
        else:
            return False, 'Header not found, user will not be authenticated.'
    except Exception:
        return False, 'Exception occurred, user will not be authenticated'


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
        is_valid_user, message = util_validate_user(request)
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
        is_valid_user, message = util_validate_user(request)
        if is_valid_user:
            status, betlist = UserBetDetials.get_peruser_bets(request.POST.get('username'))
            if len(betlist) > 0:
                _betdetails = [_b for _b in betlist.values()]
                print(_betdetails)
            else:
                _betdetails = []
            server_message = json.dumps({'status': status, 'user_bets_info': _betdetails})
        else:
            status = "error"
            server_message = json.dumps({'status':status, 'message': message})

        return HttpResponse(server_message, content_type="application/json")



@api_view(['POST'])
def auth_user(request):
    if request.method == 'POST':

        post_request = request.POST
        username = post_request.get('username')
        password  = post_request.get('password')
        print (username)
        print (password)
        result, message = Authenticate.authenticate_user(username,password)

        if result:
            print("is valid user", util_validate_user(request))
            payload_data = {"username": username}
            print (payload_data)
            token = Authenticate.generate_token(payload_data)
            token = token.decode('utf-8')
            jwt_token = {'token': token}
            print (json.dumps(jwt_token))
            return HttpResponse(json.dumps(jwt_token), content_type="application/json")
        else:
            error_message = {'errors':{'form' : message}}
            error_message = json.dumps(error_message)
            print (error_message)
            return HttpResponse(error_message, content_type="application/json", status=401)

@api_view(['POST'])
def validate_user(request):
    if request.method == 'POST':
        print("Received request to validate_user", request.method)
        is_valid_user, message = util_validate_user(request)
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
        return HttpResponse(json_data, content_type="application/json")


@api_view(['GET'])
def place_a_bet(request):
    if request.method == 'GET':
        p = PlaceABet()
        response = p.place_a_bet(request.GET['topic_id'], request.GET['username'], request.GET['option'], request.GET['amount'])
        json_data = json.dumps(response)
        return HttpResponse(json_data, content_type="application/json")


