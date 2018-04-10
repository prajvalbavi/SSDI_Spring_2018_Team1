from beton.models import Userinfo
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import jwt


#Checks if this user exists and token is verified.
class Validate:

    @staticmethod
    def unpack_token(token):
        try:
            pay_load = jwt.decode(token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
            return True, pay_load
        except Exception:
            return False, "Failed to unpack"

    @staticmethod
    def is_user_valid(token):
        if token is None or token == '':
            return False, 'Missing Token'

        result, pay_load = Validate.unpack_token(token)
        if result:
            name = pay_load['identifier']
        else:
            return False, 'Invalid User'


        try:
            Userinfo.objects.get(Q(username=name.lower()) | Q(emailID=name.lower()))
            return True, "Valid User"
        except ObjectDoesNotExist:
            return False, "Invalid User"
        except MultipleObjectsReturned:
            return False, "There is a bug in the system, username and email should not be same."

    @staticmethod
    def is_token_valid(token):
        try:
            pay_load = jwt.decode(token, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
            return True, "Signature Verified"
        except jwt.DecodeError as d:
            return False, "Signature verification failed"

