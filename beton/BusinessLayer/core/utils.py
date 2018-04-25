from rest_framework.authentication import get_authorization_header

from beton.BusinessLayer.core.AdminAuthorization import AdminAuthorization
from beton.BusinessLayer.core.UserAuthorization import UserAuthorization
from beton.BusinessLayer.core.AdminValidation import ValidateAdmin
from beton.BusinessLayer.core.UserValidation import ValidateUser
from beton.BusinessLayer.core.AuthenticationData import AuthenticationData
from beton.BusinessLayer.core.ValidationData import ValidationData



class Utils:

    @staticmethod
    def validate_user(request):
        validation_data = ValidationData(request)
        try:
            auth = validation_data.get_header()
            if auth:
                if validation_data.get_isadmin():
                    return ValidateAdmin().is_token_valid(auth)
                else:
                    return ValidateUser().is_token_valid(auth)
            else:
                return False, 'Header not found, user will not be authenticated.'
        except Exception:
            return False, 'Exception occurred, user will not be authenticated'

    @staticmethod
    def authenticate_user(request):
        authentication_data = AuthenticationData(request)
        if authentication_data is None or authentication_data.get_isadmin() == ''\
                or authentication_data.get_identifier() == '' \
                or authentication_data.get_password() == '':
            return False, "Invalid request", ''
        else:

            is_admin = authentication_data.get_isadmin()
            print ("isadmin:", is_admin)

            if is_admin:
                secret_key = authentication_data.get_secretkey()
                if secret_key == '':
                    return False, 'Invalid request', ''
                else:
                    print("Authorizing admin")
                    flag, message, user = AdminAuthorization().authenticate(authentication_data)
                    return flag, message, user, is_admin
            else:
                print("calling the daemon..")
                flag, message, user =  UserAuthorization().authenticate(authentication_data)
                print ("done calling daemon")
                return flag, message, user, is_admin

    @staticmethod
    def generate_token(request):

        flag, message, user, is_admin = Utils.authenticate_user(request)
        print ("generating...")
        print (flag, message, user, is_admin)
        if not flag:
            return False, None
        else:
            if is_admin:
                return AdminAuthorization().generate_token(user)
            else:
                return UserAuthorization().generate_token(user)


    @staticmethod
    def extract_username(request):
        _auth = ValidationData(request).get_header()
        _check, username = ValidateUser().get_username(_auth)
        if _check:
            return username






