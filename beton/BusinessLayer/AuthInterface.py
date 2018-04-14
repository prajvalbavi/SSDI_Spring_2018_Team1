from interface import Interface

class AuthInterface(Interface):

    def authenticate(self, authentication_data):
        pass

    def generate_token(self, username):
        pass
