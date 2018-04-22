from beton.models import Userinfo
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import jwt
from beton.BusinessLayer.ValidateInterface import  ValidateInterface
from interface import implements


#Checks if this user exists and token is verified.
class ValidateUser(implements(ValidateInterface)):

    def unpack(self, token):
        try:
            pay_load = jwt.decode(token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
            return True, pay_load
        except Exception:
            return False, "Failed to unpack"

    def get_username(self, token):
        if token is None or token == '':
            return False, None

        result, pay_load = self.unpack(token)
        if result:
            return True, pay_load['username']
        else:
            return False, None


        try:
            Userinfo.objects.get(Q(username=name.lower()) | Q(emailID=name.lower()))
            return True, "Valid User"
        except ObjectDoesNotExist:
            return False, "Invalid User"
        except MultipleObjectsReturned:
            return False, "There is a bug in the system, username and email should not be same."

    def is_token_valid(self, token):
        try:
            print ('request to validate user')
            pay_load = jwt.decode(token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
            print(pay_load)
            return True, "Signature Verified"
        except jwt.DecodeError as d:
            print ("Failed to decode token")
            return False, "Signature verification failed"

