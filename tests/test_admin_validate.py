from django.test import TestCase
from django.test import Client
import jwt
from beton.models import BetOnAdmins as admins
from beton.BusinessLayer.core.AdminValidation import ValidateAdmin


class TestAdminValidation(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = admins.objects.create(admin_identity="test_admin", password="test_password", secret_key="test_secrete_key")
        self.token = jwt.encode({"username": "test_admin"}, 'ThisU$erI$LoggedInBetoInfo' +
                                "test_secrete_key", algorithm="HS256")
        self.validate = ValidateAdmin()

    def test_unpack(self):
        flag, message = self.validate.unpack(self.token)
        self.assertFalse(flag)
        self.assertTrue(message == "Failed to unpack")

    def test_unpack_empty_token(self):
        flag, message = self.validate.unpack('')
        self.assertFalse(flag)
        self.assertTrue(message == "token is null or empty")

    def test_is_token_valid(self):
        flag, message  = self.validate.is_token_valid(self.token)
        self.assertTrue(flag)
        self.assertTrue(message == "Signature Verified")

    def test_is_token_valid_with_invalid_token(self):
        invalid_token = jwt.encode({"username": "test_admin"}, 'ThisU$erI$LoggedInBetoInfo', algorithm="HS256")
        flag, message = self.validate.is_token_valid(invalid_token)
        self.assertFalse(flag)
        self.assertTrue(message == "Invalid User")

    def test_is_token_valid_with_empty_token(self):
        flag, message = self.validate.is_token_valid('')
        self.assertFalse(flag)
        self.assertTrue(message == "Invalid token")


