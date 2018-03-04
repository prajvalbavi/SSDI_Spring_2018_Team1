from unittest import main as testmain, mock, TestCase

from application import Application


class TestApplicationMethods(TestCase):

    def test_in_team(self):
        # Mock Application.fetch_name_from_file
        Application.fetch_name_from_file = mock.Mock()
        Application.fetch_name_from_file.return_value = 'Apurva'

        app = Application()
        self.assertTrue(app.is_in_team())

    def test_not_in_team(self):
        # Mock Application.fetch_name_from_file
        Application.fetch_name_from_file = mock.Mock()
        Application.fetch_name_from_file.return_value = 'Krishna'

        app = Application()
        self.assertFalse(app.is_in_team())


if __name__ == '__main__':
    testmain()
