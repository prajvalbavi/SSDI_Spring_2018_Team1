from singleton_decorator import singleton
from interface import implements
from beton.BusinessLayer.AuthInterface import AuthInterface
from beton.models import BetOnAdmins as admins
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import jwt

@singleton
class AdminAuthorization(implements(AuthInterface)):

    def authenticate(self, authentication_data):

        identifier = authentication_data.get_identifier()
        password = authentication_data.get_password()
        secret_key = authentication_data.get_secretkey()

        print ("Admin keys", identifier, password, secret_key)
        try:
            admins.objects.get(Q(admin_identity=identifier.lower())
                               & Q(password=password) & Q(secret_key=secret_key))
            return True, "Admin authenticated", identifier
        except ObjectDoesNotExist as o:
            print(str(o))
            return False, "Invalid credentials", ''
        except MultipleObjectsReturned as m:
            print(str(m))
            return False, "There is a bug in the system, unique result expected for an admin.", ''

    def generate_token(self, username):
        try:
            print ("generate token for admin", username)
            r_obj = admins.objects.get(Q(admin_identity=username.lower()))
            payload_data = {"username": r_obj.admin_identity}
            paraphrase = '' if r_obj.secret_key is None else r_obj.secret_key
            return True, jwt.encode(payload_data, 'ThisU$erI$LoggedInBetoInfo' +
                              paraphrase, algorithm="HS256").decode('utf-8')
        except Exception:
            return False, None
