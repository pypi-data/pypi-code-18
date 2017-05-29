# Copyright 2017 Zdenek Kraus <zdenek.kraus@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase
import libracmp
from libracmp.Comparator import Comparator
from libracmp.IgnoreComparator import IgnoreComparator
from libracmp.StrictComparator import StrictComparator


class TestResultComparatRealCases(TestCase):

    def test_result_messaging_jms_inflt_modeignore_eq(self):

        # even though there are few differences, and it would be easier to exclude
        # problematic values from comparison, this approach is more resilient
        # if there is a chance of new values appearing over time
        msg_a = [{
            'ttl': 300000, 'delivery-count': '1', 'correlation_id': 'amqp_bare_msg-LEgPm8',
            'reply-to-group-id': 'group-a', 'id': '38005bfa-e819-4778-a8b6-48fe6a73c10c:1:1:1-1',
            'subject': 'amqp_bare_message_test',
            'priority': 7,  # difference
            'user_id': 'admin',
            'durable': True, 'content': 'Message content amqp_bare_msg-LEgPm8',
            'content_encoding': None, 'redelivered': False,
            'creation-time': 1492081926039, 'absolute-expiry-time': 1492082226039,
            'content_type': None, 'address': 'test_amqp_bare_message_consistency',
            'properties': {
                'JMS_AMQP_REPLY_TO_GROUP_ID': 'group-a', 'JMSXGroupSeq': 1,
                # data we want to compare specifically
                'PI': '~3.141592', 'color': 'red', 'mapKey': 'mapValue',
                'JMSXDeliveryCount': 1, 'JMSXGroupID': 'group-a', 'JMSXUserID': 'admin'
            },
            'first-acquirer': False, 'group-id': 'group-a', 'delivery-time': 0,
            'reply_to': 'ExpiryQueue', 'group-sequence': 1
        }]

        msg_b = [{
            'ttl': 300000, 'delivery-count': '1', 'correlation_id': 'amqp_bare_msg-LEgPm8',
            'reply-to-group-id': 'group-a', 'id': '38005bfa-e819-4778-a8b6-48fe6a73c10c:1:1:1-1',
            'subject': 'amqp_bare_message_test',
            'priority': 6,  # difference
            'user_id': 'admin',
            'durable': True, 'content': 'Message content amqp_bare_msg-LEgPm8',
            'content_encoding': None, 'redelivered': False,
            'creation-time': 1492081926039, 'absolute-expiry-time': 1492082226039,
            'content_type': None, 'address': 'test_amqp_bare_message_consistency',
            'properties': {
                'JMS_AMQP_REPLY_TO_GROUP_ID': 'group-a', 'JMSXGroupSeq': 2,
                # data we want to compare specifically
                'PI': '~3.141592', 'color': 'red', 'mapKey': 'mapValue',
                'JMSXDeliveryCount': 1, 'JMSXGroupID': 'group-a', 'JMSXUserID': 'admin'
            },
            'first-acquirer': False, 'group-id': 'group-a', 'delivery-time': 0,
            'reply_to': 'ExpiryQueue', 'group-sequence': 1
        }]
        # inclusion filtered keys
        inflt = ['durable', 'ttl', 'first-acquirer', 'delivery-count', 'id', 'user_id',
                 'address', 'subject', 'reply_to', 'correlation_id', 'content_type',
                 'content_encoding', 'absolute-expiry-time', 'creation-time', 'group-id',
                 'group-sequence', 'reply-to-group-id', 'properties', 'content']
        # assume level0 ~ [], level1 ~[{}], etc.

        # apply all inclusion filtered keys onto level 1
        filters = {libracmp.All(): {k: StrictComparator for k in inflt}}

        # add specific sub-filter for level 1 key properties
        filters[libracmp.All()]['properties'] = {
            # specific keys comparisons
            'PI': StrictComparator,
            'color': StrictComparator,
            'mapKey': StrictComparator
        }
        # enabling ignore mode, so if not specified otherwise, ignoring all comparisons
        comp = libracmp.Comparator.Comparator(msg_a, msg_b, filters=filters, mode=libracmp.MODE_IGNORE)
        self.assertTrue(comp.result)

    def test_result_messaging_jms_inflt_eq(self):

        # even though there are few differences, and it would be easier to exclude
        # problematic values from comparison, this approach is more resilient
        # if there is a chance of new values appearing over time
        msg_a = [{
            'ttl': 300000, 'delivery-count': '1', 'correlation_id': 'amqp_bare_msg-LEgPm8',
            'reply-to-group-id': 'group-a', 'id': '38005bfa-e819-4778-a8b6-48fe6a73c10c:1:1:1-1',
            'subject': 'amqp_bare_message_test',
            'priority': 7,  # difference
            'user_id': 'admin',
            'durable': True, 'content': 'Message content amqp_bare_msg-LEgPm8',
            'content_encoding': None, 'redelivered': False,
            'creation-time': 1492081926039, 'absolute-expiry-time': 1492082226039,
            'content_type': None, 'address': 'test_amqp_bare_message_consistency',
            'properties': {
                'JMS_AMQP_REPLY_TO_GROUP_ID': 'group-a', 'JMSXGroupSeq': 1,
                # data we want to compare specifically
                'PI': '~3.141592', 'color': 'red', 'mapKey': 'mapValue',
                'JMSXDeliveryCount': 1, 'JMSXGroupID': 'group-a', 'JMSXUserID': 'admin'
            },
            'first-acquirer': False, 'group-id': 'group-a', 'delivery-time': 0,
            'reply_to': 'ExpiryQueue', 'group-sequence': 1
        }]

        msg_b = [{
            'ttl': 300000, 'delivery-count': '1', 'correlation_id': 'amqp_bare_msg-LEgPm8',
            'reply-to-group-id': 'group-a', 'id': '38005bfa-e819-4778-a8b6-48fe6a73c10c:1:1:1-1',
            'subject': 'amqp_bare_message_test',
            'priority': 6,  # difference
            'user_id': 'admin',
            'durable': True, 'content': 'Message content amqp_bare_msg-LEgPm8',
            'content_encoding': None, 'redelivered': False,
            'creation-time': 1492081926039, 'absolute-expiry-time': 1492082226039,
            'content_type': None, 'address': 'test_amqp_bare_message_consistency',
            'properties': {
                'JMS_AMQP_REPLY_TO_GROUP_ID': 'group-a', 'JMSXGroupSeq': 2,
                # data we want to compare specifically
                'PI': '~3.141592', 'color': 'red', 'mapKey': 'mapValue',
                'JMSXDeliveryCount': 1, 'JMSXGroupID': 'group-a', 'JMSXUserID': 'admin'
            },
            'first-acquirer': False, 'group-id': 'group-a', 'delivery-time': 0,
            'reply_to': 'ExpiryQueue', 'group-sequence': 1
        }]
        # inclusion filtered keys
        inflt = ['durable', 'ttl', 'first-acquirer', 'delivery-count', 'id', 'user_id',
                 'address', 'subject', 'reply_to', 'correlation_id', 'content_type',
                 'content_encoding', 'absolute-expiry-time', 'creation-time', 'group-id',
                 'group-sequence', 'reply-to-group-id', 'properties', 'content']
        # assume level0 ~ [], level1 ~[{}], etc.

        # apply all inclusion filtered keys onto level 1
        filters = {libracmp.All(): {k: StrictComparator for k in inflt}}

        # ignore default items on level 1
        filters[libracmp.All()][libracmp.All()] = IgnoreComparator

        # add specific sub-filter for level 1 key properties
        filters[libracmp.All()]['properties'] = {
            libracmp.All(): IgnoreComparator,  # all default values ignored
            # specific keys comparisons
            'PI': StrictComparator,
            'color': StrictComparator,
            'mapKey': StrictComparator
        }

        # relaxed mode is used, thus specific ignores are specified explicitly
        comp = libracmp.Comparator.Comparator(msg_a, msg_b, filters=filters, mode=libracmp.MODE_RELAXED)
        self.assertTrue(comp.result)

    def test_result_messaging_jms_exflt_eq(self):

        msg_a = [{
            'ttl': 300000, 'delivery-count': '1', 'correlation_id': 'amqp_bare_msg-LEgPm8',
            'reply-to-group-id': 'group-a', 'id': '38005bfa-e819-4778-a8b6-48fe6a73c10c:1:1:1-1',
            'subject': 'amqp_bare_message_test',
            'priority': 7,  # difference
            'user_id': 'admin',
            'durable': True, 'content': 'Message content amqp_bare_msg-LEgPm8',
            'content_encoding': None, 'redelivered': False,
            'creation-time': 1492081926039, 'absolute-expiry-time': 1492082226039,
            'content_type': None, 'address': 'test_amqp_bare_message_consistency',
            'properties': {
                'JMS_AMQP_REPLY_TO_GROUP_ID': 'group-a',
                'JMSXGroupSeq': 1,  # difference
                'PI': '~3.141592', 'color': 'red', 'mapKey': 'mapValue',
                'JMSXDeliveryCount': 1, 'JMSXGroupID': 'group-a', 'JMSXUserID': 'admin'
            },
            'first-acquirer': False, 'group-id': 'group-a', 'delivery-time': 0,
            'reply_to': 'ExpiryQueue', 'group-sequence': 1
        }]

        msg_b = [{
            'ttl': 300000, 'delivery-count': '1', 'correlation_id': 'amqp_bare_msg-LEgPm8',
            'reply-to-group-id': 'group-a', 'id': '38005bfa-e819-4778-a8b6-48fe6a73c10c:1:1:1-1',
            'subject': 'amqp_bare_message_test',
            'priority': 6,  # difference
            'user_id': 'admin',
            'durable': True, 'content': 'Message content amqp_bare_msg-LEgPm8',
            'content_encoding': None, 'redelivered': False,
            'creation-time': 1492081926039, 'absolute-expiry-time': 1492082226039,
            'content_type': None, 'address': 'test_amqp_bare_message_consistency',
            'properties': {
                'JMS_AMQP_REPLY_TO_GROUP_ID': 'group-a',
                'JMSXGroupSeq': 2,  # difference
                'PI': '~3.141592', 'color': 'red', 'mapKey': 'mapValue',
                'JMSXDeliveryCount': 1, 'JMSXGroupID': 'group-a', 'JMSXUserID': 'admin'
            },
            'first-acquirer': False, 'group-id': 'group-a', 'delivery-time': 0,
            'reply_to': 'ExpiryQueue', 'group-sequence': 1
        }]
        # assume level0 ~ [], level1 ~[{}], etc.

        # add exclusion (ignore) filter for specific problematic values
        filters = {
            libracmp.All(): {
                'priority': IgnoreComparator,
                'properties': {
                    'JMSXGroupSeq': IgnoreComparator,  # all default values ignored
                }
            }
        }

        comp = libracmp.Comparator.Comparator(msg_a, msg_b, filters=filters, mode=libracmp.MODE_RELAXED)
        self.assertTrue(comp.result)
