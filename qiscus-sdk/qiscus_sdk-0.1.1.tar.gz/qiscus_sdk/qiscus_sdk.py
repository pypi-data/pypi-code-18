# -*- coding: utf-8 -*-
import json

from requests import post


class QiscusSDK(object):
    """
    Simple Qiscus SDK wrapper, NOW POST TO QISME ENGINE
    """

    @staticmethod
    def send_message(topic_id, message='', _type='text', base_url='', access_token='', payload=None):
        """
        Send message to Qiscus SDK

        :param topic_id: integer, required
        :param message: string, required if type is "text". Its optional If
                        type is "account_linking"
        :param _type: string, "text", "account_linking"
        :param payload: None if type is "text".
                payload = {
                    "url": "http://google.com",
                    "redirect_url": "http://google.com/redirect",
                    "params": {
                        "user_id": 1,
                        "topic_id": 1
                    }
                } if type is "account_linking"
        :param base_url: string
        :param access_token: string
        :return object request:
        """

        url = base_url + '/api/v1/chat/conversations/post_comment'
        data = {
            'access_token': access_token,
            'topic_id': topic_id,
            'type': _type,
            'comment': message,
            'payload': json.dumps(payload)
        }

        request = post(url, data=data)

        return request

    def send_buttons(self, topic_id, message, payload, base_url='', access_token=''):
        """
        Send buttons type messages
        :param access_token:
        :param base_url:
        :param topic_id:
        :param message:
        :param payload: expected to be a list of button object, max 3
                        [
                            {
                                "label": "button1", #any label
                                "type": "postback", #any type
                                "payload": {
                                    "url": "http://somewhere.com/button1",
                                    "method": "get",
                                    "payload": null
                                }
                            }
                        ]

        :return:
        """

        return self.send_message(
            topic_id, message=message, _type="buttons",
            base_url=base_url, access_token=access_token,
            payload=payload
        )
