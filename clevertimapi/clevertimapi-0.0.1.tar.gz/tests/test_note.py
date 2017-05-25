import json
from copy import deepcopy
from clevertimapi.session import Session
from clevertimapi.note import Note, EmailInfo, EmailRecipient
from clevertimapi.contact import Contact
from clevertimapi.company import Company
from clevertimapi.case import Case
from clevertimapi.user import User
from clevertimapi.comment import Comment
from clevertimapi.file import File, LinkedFile
from clevertimapi.opportunity import Opportunity
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


class TestNote(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.session = Session('API_KEY')

        self.note1 = {
            'id': 445,
            'desc': 'This is a simple note in the system',
            'type': 'S',
            'fmt': 'T',
            'ao': '2017-04-23T12:23:22Z',
            'userId': 95,
            'is_deleted': False,
            'cust': [33, 43, 53],
            'case': 23,
            'opportunity': 31,
            'delvry': 'N',
            'hl': 'headline',
            'email': {
                'f': 'mike.toto@gmail.com',
                's': 'subject of email',
                't': [{
                    'e': 'to_recipient1@gmail.com',
                    's': 's'
                }, {
                    'e': 'to_recipient2@yahoo.com',
                    's': 'b',
                    't': 'Invalid email address'
                }, {
                    'e': 'to_recipient3@gaga.com',
                    's': 'b',
                    't': 'Mail system full'
                }
                ],
                'c': [{
                    'e': 'cc_recipient3@gaga.com',
                    's': 'b',
                    't': 'Mail system full'
                }, {
                    'e': 'cc_recipient1@gmail.com',
                    's': 's'
                }, {
                    'e': 'cc_recipient2@yahoo.com',
                    's': 'b',
                    't': 'Invalid email address'
                }
                ],
                'b': [{
                    'e': 'bcc_recipient3@gaga.com',
                    's': 'b',
                    't': 'Mail system full'
                }, {
                    'e': 'bcc_recipient2@yahoo.com',
                    's': 'b',
                    't': 'Invalid email address'
                }, {
                    'e': 'bcc_recipient1@gmail.com',
                    's': 's'
                }
                ]
            },
            'files': [22, 34],
            'lfiles': [120, 330, 454],
            'comments': [78, 99, 120]
        }
        self.note1_ret = deepcopy(self.note1)
        self.note1_ret.update({
            'id': 445,
        })
        self.note2 = {
        }

    def _compare_against_note1_ret(self, c):
        self.assertEqual(c.key, 445)
        self.assertEqual(c.description, 'This is a simple note in the system')
        self.assertEqual(c.note_type, Note.NOTE_TYPES.EMAIL_NOTE)
        self.assertEqual(c.who, [Contact(self.session, key=33), Company(self.session, key=43), Company(self.session, key=53)])
        self.assertEqual(c.case, Case(self.session, key=23, lazy_load=True))
        self.assertEqual(c.opportunity, Opportunity(self.session, key=31, lazy_load=True))
        self.assertEqual(c.created_by, User(self.session, key=95, lazy_load=True))
        self.assertEqual(c.sms_delivery_info, Note.NOTE_DELIVERY_TYPES.NO_EXTERNAL_DELIVERY)
        self.assertEqual(c.comments, [
            Comment(self.session, key=78, lazy_load=True),
            Comment(self.session, key=99, lazy_load=True),
            Comment(self.session, key=120, lazy_load=True),
        ])
        self.assertEqual(c.files, [
            File(self.session, key=22, lazy_load=True),
            File(self.session, key=34, lazy_load=True),
        ])
        self.assertEqual(c.linked_files, [
            LinkedFile(self.session, key=120, lazy_load=True),
            LinkedFile(self.session, key=330, lazy_load=True),
            LinkedFile(self.session, key=454, lazy_load=True),
        ])
        self.assertIsInstance(c.email_info, EmailInfo)
        self.assertEqual(c.email_info.sender, 'mike.toto@gmail.com')
        self.assertEqual(c.email_info.subject, 'subject of email')
        self.assertIsInstance(c.email_info.to, tuple)

        self.assertTrue(all(isinstance(ei, EmailRecipient) for ei in c.email_info.to))
        self.assertTrue(all(isinstance(ei, EmailRecipient) for ei in c.email_info.cc))
        self.assertTrue(all(isinstance(ei, EmailRecipient) for ei in c.email_info.bcc))

        self.assertEqual(c.email_info.to[0].email_address, 'to_recipient1@gmail.com')
        self.assertEqual(c.email_info.to[0].status, EmailRecipient.SENT)
        self.assertIsNone(c.email_info.to[0].bounce_reason)
        self.assertEqual(c.email_info.to[1].email_address, 'to_recipient2@yahoo.com')
        self.assertEqual(c.email_info.to[1].status, EmailRecipient.BOUNCED)
        self.assertEqual(c.email_info.to[1].bounce_reason, 'Invalid email address')
        self.assertEqual(c.email_info.to[2].email_address, 'to_recipient3@gaga.com')
        self.assertEqual(c.email_info.to[2].status, EmailRecipient.BOUNCED)
        self.assertEqual(c.email_info.to[2].bounce_reason, 'Mail system full')

        self.assertEqual(c.email_info.cc[1].email_address, 'cc_recipient1@gmail.com')
        self.assertEqual(c.email_info.cc[1].status, EmailRecipient.SENT)
        self.assertIsNone(c.email_info.cc[1].bounce_reason)
        self.assertEqual(c.email_info.cc[2].email_address, 'cc_recipient2@yahoo.com')
        self.assertEqual(c.email_info.cc[2].status, EmailRecipient.BOUNCED)
        self.assertEqual(c.email_info.cc[2].bounce_reason, 'Invalid email address')
        self.assertEqual(c.email_info.cc[0].email_address, 'cc_recipient3@gaga.com')
        self.assertEqual(c.email_info.cc[0].status, EmailRecipient.BOUNCED)
        self.assertEqual(c.email_info.cc[0].bounce_reason, 'Mail system full')

        self.assertEqual(c.email_info.bcc[2].email_address, 'bcc_recipient1@gmail.com')
        self.assertEqual(c.email_info.bcc[2].status, EmailRecipient.SENT)
        self.assertIsNone(c.email_info.bcc[2].bounce_reason)
        self.assertEqual(c.email_info.bcc[1].email_address, 'bcc_recipient2@yahoo.com')
        self.assertEqual(c.email_info.bcc[1].status, EmailRecipient.BOUNCED)
        self.assertEqual(c.email_info.bcc[1].bounce_reason, 'Invalid email address')
        self.assertEqual(c.email_info.bcc[0].email_address, 'bcc_recipient3@gaga.com')
        self.assertEqual(c.email_info.bcc[0].status, EmailRecipient.BOUNCED)
        self.assertEqual(c.email_info.bcc[0].bounce_reason, 'Mail system full')

    @mock.patch('requests.get')
    def test_load_note(self, mockRequestsGET):
        setup_requests_call_mock(mockRequestsGET, {
            '/note/445': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [
                        self.note1_ret
                    ]
                })
            ),
            '/contact/33': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [{
                        'id': 33,
                        'fn': 'Miky Gory',
                    }]
                })
            ),
            '/contact/43': (
                404,
                json.dumps({
                    'status': 'ERROR',
                    'content': []
                })
            ),
            '/contact/53': (
                404,
                json.dumps({
                    'status': 'ERROR',
                    'content': []
                })
            ),
            '/company/43': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [{
                        'id': 43,
                        'cn': 'IBM Ltd.',
                    }]
                })
            ),
            '/company/53': (
                200,
                json.dumps({
                    'status': 'OK',
                    'content': [{
                        'id': 53,
                        'cn': 'Redhat',
                    }]
                })
            ),
        })

        c = Note(self.session, key=445)
        self.assertFalse(c.is_new())
        self._compare_against_note1_ret(c)
