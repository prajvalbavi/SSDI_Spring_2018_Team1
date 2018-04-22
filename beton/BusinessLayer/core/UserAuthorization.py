from singleton_decorator import singleton
from beton.models import Userinfo
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from interface import implements
import jwt
from beton.BusinessLayer.AuthInterface import AuthInterface


@singleton
class UserAuthorization(implements(AuthInterface)):

    def authenticate(self, authentication_data):

        identifier = authentication_data.get_identifier()
        password = authentication_data.get_password()

        try:
            r_obj = Userinfo.objects.get(Q(username=identifier.lower()) | Q(emailID=identifier.lower()))
            if r_obj.password == password:
                print ("returning...")
                print (True, "User Authenticated", r_obj.username)
                return True, "User Authenticated", r_obj.username
            else:
                return False, "Invalid Credentials", ''

        except ObjectDoesNotExist:
            return False, "Invalid Credentials", ''
        except MultipleObjectsReturned:
            return False, "There is a bug in the system, username and email should not be same.", ''


    def generate_token(self, username):
        try:
            r_obj = Userinfo.objects.get(Q(username=username.lower()) | Q(emailID=username.lower()))
            payload_data = {"username": r_obj.username}
            print (payload_data)
            token = jwt.encode(payload_data, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256").decode('utf-8')
            print ('sending.....')
            return True, token
        except Exception:
            return False, None
