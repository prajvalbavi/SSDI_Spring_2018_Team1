from beton.models import Userinfo
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class SignupUser:

    @staticmethod
    def create_user(username, password, email_id):
        try:
            Userinfo.objects.create(username=username, password=password, emailID=email_id)
            return "Success", "User added successfully"
        except Exception as e:
            return "Exception", str(e)

    @staticmethod
    def signup(username, password, email_id):
        try:
            r_obj = Userinfo.objects.get(Q(username=username) | Q(emailId=email_id))
            if r_obj.username == username:
                return "Error", "Username already exists"
            elif r_obj.emailID == email_id:
                return "Error", "Username already exists"

        except ObjectDoesNotExist:
            return SignupUser.create_user(username,password, email_id)



