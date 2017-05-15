# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /       
"""

from tests import IntegrationTestCase
from tests.holodeck import Request
from twilio.base.exceptions import TwilioException
from twilio.http.response import Response


class WorkspaceStatisticsTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.taskrouter.v1.workspaces(sid="WSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                     .statistics().fetch()
        
        self.holodeck.assert_has_request(Request(
            'get',
            'https://taskrouter.twilio.com/v1/Workspaces/WSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Statistics',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "cumulative": {
                    "avg_task_acceptance_time": 0.0,
                    "end_time": "2015-08-18T17:03:13Z",
                    "reservations_accepted": 0,
                    "reservations_canceled": 0,
                    "reservations_created": 0,
                    "reservations_rejected": 0,
                    "reservations_rescinded": 0,
                    "reservations_timed_out": 0,
                    "start_time": "2015-08-18T16:48:13Z",
                    "tasks_canceled": 0,
                    "tasks_created": 0,
                    "tasks_deleted": 0,
                    "tasks_moved": 0,
                    "tasks_timed_out_in_workflow": 0
                },
                "realtime": {
                    "activity_statistics": [
                        {
                            "friendly_name": "Offline",
                            "sid": "WAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "workers": 1
                        },
                        {
                            "friendly_name": "Idle",
                            "sid": "WAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "workers": 0
                        },
                        {
                            "friendly_name": "80fa2beb-3a05-11e5-8fc8-98e0d9a1eb73",
                            "sid": "WAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "workers": 0
                        },
                        {
                            "friendly_name": "Reserved",
                            "sid": "WAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "workers": 0
                        },
                        {
                            "friendly_name": "Busy",
                            "sid": "WAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "workers": 0
                        },
                        {
                            "friendly_name": "817ca1c5-3a05-11e5-9292-98e0d9a1eb73",
                            "sid": "WAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                            "workers": 0
                        }
                    ],
                    "longest_task_waiting_age": 0,
                    "longest_task_waiting_sid": null,
                    "tasks_by_status": {
                        "assigned": 0,
                        "pending": 0,
                        "reserved": 0
                    },
                    "total_tasks": 0,
                    "total_workers": 1
                },
                "workspace_sid": "WSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            }
            '''
        ))
        
        actual = self.client.taskrouter.v1.workspaces(sid="WSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                          .statistics().fetch()
        
        self.assertIsNotNone(actual)
