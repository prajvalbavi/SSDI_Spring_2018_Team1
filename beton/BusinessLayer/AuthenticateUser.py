from beton.models import Userinfo
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import jwt

class Authenticate:
    @staticmethod
    def authenticate_user(name, password):
        try:
            print ("authenticate_user")

            r_obj = Userinfo.objects.get(Q(username=name.lower()) | Q(emailID=name.lower()))
            print(r_obj.password)

            if r_obj.password == password:
                return True, "Login successful"
            else: return False, "Invalid Credentials"

        except ObjectDoesNotExist:
            return False, "Invalid Credentials"
        except MultipleObjectsReturned:
            return False, "There is a bug in the system, username and email should not be same."

    @staticmethod
    def generate_token( payload_data):
        print ("Payload", payload_data)
        return jwt.encode(payload_data, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")

