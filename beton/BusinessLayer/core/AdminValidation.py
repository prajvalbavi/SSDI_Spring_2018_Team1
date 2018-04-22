import jwt
from interface import implements
from beton.BusinessLayer.ValidateInterface import ValidateInterface
from beton.models import BetOnAdmins as admins
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ValidateAdmin(implements(ValidateInterface)):
    def __init__(self):
        self.secret_key = 'ThisU$erI$LoggedInBetoInfo'

    def unpack(self, token):

        if token is None or token is '':
            print("token is null or empty")
            return False, None

        try:
            pay_load = jwt.decode(token, self.secret_key, algorithm="HS256")
            return True, pay_load
        except Exception:
            print ('Failed to unpack')
            return False, None

    def _get_username(self, token):

        try:
            pay_load = jwt.decode(token, verify= False)
            return True, pay_load
        except jwt.DecodeError:
            return False, None


    def is_token_valid(self, token):

        if token is None or token is '':
            print("token is null or empty")
            return False, "Invalid token"


        result, pay_load = self._get_username(token)

        if not result:
            print ("Unable to fetch username from token")
            return False, "Invalid Token"

        try:

            r_obj = admins.objects.get(admin_identity=pay_load['username'])

            if r_obj.secret_key is not None:
                self.secret_key += r_obj.secret_key

            result, pay_load = self.unpack(token)
            if(result):
                return True, "Signature Verified"
            else:
                return False, "Invalid User"

        except ObjectDoesNotExist:
            print("user doesn't exist")
            return False, "Invalid token"
        except MultipleObjectsReturned:
            print("There is a bug in the system, more than one admins returns for", pay_load['username'])
            return False, "Invalid token"