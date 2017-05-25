import json
from clevertimapi.session import Session
from clevertimapi.endpoint import ValidationError
from clevertimapi.file import Folder, File
from mock_utils import setup_requests_call_mock
import sys
try:
    import unittest.mock as mock
except ImportError:
    import mock
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestFile(unittest.TestCase):
    def setUp(self):
        self.session = Session('APIKEY')

    def test_parent_folder_needs_to_be_saved(self):
        unsaved_parent = Folder(self.session)
        folder = Folder(self.session)
        with self.assertRaises(ValidationError):
            folder.parent = unsaved_parent

    @mock.patch('requests.post')
    def test_parent_folder_needs_to_be_saved2(self, requestsMockPOST):
        setup_requests_call_mock(requestsMockPOST, {
            '/folder': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [{
                        'id': 'f1001'
                    }]
                })
            )
        })
        saved_parent = Folder(self.session, key='f111', lazy_load=True)
        folder = Folder(self.session)
        folder.name = 'New Folder'
        folder.parent = saved_parent
        folder.save()
        self.assertEqual(folder.key, 'f1001')

    def test_parent_folder_needs_to_be_saved3(self):
        unsaved_parent = Folder(self.session)
        _file = File(self.session)
        with self.assertRaises(ValidationError):
            _file.parent = unsaved_parent

    @mock.patch('requests.post')
    def test_parent_folder_needs_to_be_saved4(self, requestsMockPOST):
        setup_requests_call_mock(requestsMockPOST, {
            '/file': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [{
                        'id': 233
                    }]
                })
            )
        })
        saved_parent = Folder(self.session, key='f111', lazy_load=True)
        _file = File(self.session)
        _file.name = 'New File'
        _file.parent = saved_parent
        _file.save()
        self.assertEqual(_file.key, 233)
