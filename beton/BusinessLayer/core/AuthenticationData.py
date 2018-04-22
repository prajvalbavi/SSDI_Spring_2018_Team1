from rest_framework.authentication import get_authorization_header

class AuthenticationData:
    def __init__(self, request):

        self.isadmin = True if request.get('is_admin', default = '') == 'true' else False
        self.identifier = request.get('identifier', default= '')
        self.password = request.get('password', default= '')
        self.secret_key = request.get('secret_key', default= '')
        self.header = ''
        try:
            self.header = get_authorization_header(request)
        except Exception:
            pass


    def get_identifier(self):
        return self.identifier

    def get_password(self):
        return self.password

    def get_secretkey(self):
        return self.secret_key

    def get_isadmin(self):
        return self.isadmin

    def get_header(self):
        return self.header
