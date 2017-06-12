from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from unittest.mock import patch
User = get_user_model()


class AuthLoggerTestCase(TestCase):
    login_url = '/admin/login/'

    @patch('auth_logger.signals.handlers.logger')
    def test_login(self, mock_logger):
        user = User.objects.create_user(username="test", password="sometest")
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.client.post(self.login_url,
                         {'username': 'test', 'password': 'sometest'})
        mock_logger.info.assert_called()

    @patch('auth_logger.signals.handlers.logger')
    def test_failed_login(self, mock_logger):
        user = User.objects.create_user(username="test", password="sometest")
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.client.post(self.login_url,
                         {'username': 'test', 'password': 'sometest'})
        mock_logger.info.assert_called()

    @patch('auth_logger.signals.handlers.logger')
    def test_non_staff_login(self, mock_logger):
        """ Non staff user shouldn't be logged """
        User.objects.create_user(username="test", password="sometest")

        self.client.post('/admin/login/',
                         {'username': 'test', 'password': 'sometest'})
        mock_logger.info.assert_not_called()

    def test_authenticate_method(self):
        """ Django authenticate method can be called with just a tokem (no user)
        https://docs.djangoproject.com/en/1.11/topics/auth/default/#authenticating-users
        """
        authenticate(token="blarg")
