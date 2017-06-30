from byu_awslogin.adfs_auth import authenticate
from unittest.mock import patch, MagicMock
import os

@patch('byu_awslogin.adfs_auth.requests')
def test_authenticate(mock_requests):
    mock_session = mock_requests.Session.return_value = MagicMock()    
    
    # Mock initial login page
    script_dir = os.path.dirname(os.path.realpath(__file__))
    auth_page_text = open('{}/adfs_html_mocks/login_screen.html'.format(script_dir), 'r').read()
    auth_page_mock = MagicMock(status_code=200, text=auth_page_text)
    mock_session.get.return_value = auth_page_mock
    
    # Mock duo auth page
    duo_page_text = open('{}/adfs_html_mocks/duo_screen.html'.format(script_dir), 'r').read()
    duo_screen_mock = MagicMock(status_code=200, text=duo_page_text)
    mock_session.post.return_value = duo_screen_mock
    # authenticate('FakeUsername', 'FakePassword')
    