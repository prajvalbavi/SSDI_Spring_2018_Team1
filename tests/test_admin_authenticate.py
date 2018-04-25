import jwt
from django.test import TestCase
from beton.BusinessLayer.core.AdminAuthorization import AdminAuthorization
from beton.models import BetOnAdmins as admins
from django.test.client import RequestFactory
from unittest.mock import patch
from beton.BusinessLayer.core.AuthenticationData import AuthenticationData


class TestAuthenticate(TestCase):
    def setUp(self):
        self.admin = admins.objects.create(admin_identity="test_admin", password="test_password", secret_key="test_key")
        self.auth = AdminAuthorization()
        self.admin_identity = "test_admin"
        self.password = "test_password"
        self.secret_key = "test_key"

    def side_effect_success(self, key, default):  # Helps in faking request object with all data present.
        print("side effect key", key, "default:", default)

        if key == "identifier":
            return self.admin_identity
        if key == "password":
            return self.password
        if key == "secret_key":
            return self.secret_key
        if key == "is_admin":
            return "true"

    @patch('django.test.client.RequestFactory')
    def test_authenticate_data(self, mock_req):
        mock_req.get.side_effect = self.side_effect_success
        auth_data = AuthenticationData(mock_req)

        print("identifier", auth_data.get_identifier())

        self.assertTrue(auth_data.get_identifier() == self.admin_identity)
        self.assertTrue(auth_data.get_isadmin() == True)
        self.assertTrue(auth_data.get_password() == self.password)
        self.assertTrue(auth_data.get_secretkey() == self.secret_key)

        flag, message, identifier = self.auth.authenticate(auth_data)
        print("Flag:", flag, "Identifier:", identifier, "message:", message)

    @patch('beton.BusinessLayer.core.AuthenticationData.AuthenticationData')
    def test_authenticate_valid_admin(self, mock_auth_data):
        mock_auth_data.get_identifier.return_value = self.admin_identity
        mock_auth_data.get_password.return_value = self.password
        mock_auth_data.get_secretkey.return_value = self.secret_key

        flag, message, identifier = self.auth.authenticate(mock_auth_data)
        self.assertTrue(flag)
        self.assertTrue(message == "Admin authenticated")
        self.assertTrue(identifier == self.admin_identity)


    @patch('beton.BusinessLayer.core.AuthenticationData.AuthenticationData')
    def test_authenticate_invalid_identity(self, mock_auth_data):
        mock_auth_data.get_identifier.return_value = 'Nikhil101'
        mock_auth_data.get_password.return_value = self.password
        mock_auth_data.get_secretkey.return_value = self.secret_key

        flag, message, identifier = self.auth.authenticate(mock_auth_data)
        print(flag, message, identifier)
        self.assertFalse(flag)
        self.assertTrue(message == "Invalid credentials")

    @patch('beton.BusinessLayer.core.AuthenticationData.AuthenticationData')
    def test_authenticate_invalid_password(self, mock_auth_data):
        mock_auth_data.get_identifier.return_value = self.admin_identity
        mock_auth_data.get_password.return_value = 'Nikhil12345'
        mock_auth_data.get_secretkey.return_value = self.secret_key

        flag, message, identifier = self.auth.authenticate(mock_auth_data)
        self.assertFalse(flag)
        self.assertTrue(message == "Invalid credentials")

    @patch('beton.BusinessLayer.core.AuthenticationData.AuthenticationData')
    def test_authenticate_valid_secret_key(self, mock_auth_data):
        mock_auth_data.get_identifier.return_value = self.admin_identity
        mock_auth_data.get_password.return_value = self.password
        mock_auth_data.get_secretkey.return_value = 'nikhilaaaaabbbcc'

        flag, message, identifier = self.auth.authenticate(mock_auth_data)
        self.assertFalse(flag)
        self.assertTrue(message == "Invalid credentials")

