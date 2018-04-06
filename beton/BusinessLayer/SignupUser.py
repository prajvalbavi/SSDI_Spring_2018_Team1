from beton.models import Userinfo
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class SignupUser:

    @staticmethod
    def create_user(username, password, email_id):
        try:
            Userinfo.objects.create(username=username.lower(), password=password, emailID=email_id.lower())
            return "success", "User added successfully"
        except Exception as e:
            return "exception", str(e)

    @staticmethod
    def signup(username, password, email_id):
        try:
            print (username,password,email_id)
            r_obj = Userinfo.objects.get(Q(username=username.lower()) | Q(emailID=email_id.lower()))
            if r_obj.username == username.lower():
                return "error", "Username already exists"
            elif r_obj.emailID == email_id.lower():
                return "error", "Email already exists"

        except ObjectDoesNotExist:
            return SignupUser.create_user(username,password, email_id)
        except MultipleObjectsReturned as m:
            return "exception", "Both Username and Email already exists"


