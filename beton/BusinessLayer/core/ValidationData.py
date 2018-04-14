from rest_framework.authentication import get_authorization_header


class ValidationData:
    def __init__(self, request):
        self.isadmin = True if request.POST.get('is_admin', default = '').lower() == 'true' else False
        self.header = ''
        try:
            self.header = get_authorization_header(request).decode('utf-8')
        except Exception:
            pass

    def get_isadmin(self):
        return self.isadmin

    def get_header(self):
        return self.header
