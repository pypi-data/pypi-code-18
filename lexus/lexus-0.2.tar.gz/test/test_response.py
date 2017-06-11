# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
from lexi import lex

import unittest
from fixtures.responses import DEFAULT_RESPONSE
from fixtures.requests import DEFAULT_REQUEST

class TestResponse(unittest.TestCase):
    '''
        # Use setUp if common process before test.
        def setUp(self):

        # Use tearDown if common process after test.
        def tearDown(self):
    '''
    def test_raise_elicit_slot_without_intent_name(self):
        slots = ['Cat', 'Dog']
        with self.assertRaises(TypeError):
            lex.ResponseBuilder.elicit_slot(slots=slots)
    
    def test_raise_elicit_slot_without_slots(self):
        intent_name = 'AnimalIntent'
        with self.assertRaises(TypeError):
            lex.ResponseBuilder.elicit_slot(intent_name=intent_name)

    def test_raise_confirm_intent_without_intent_name(self):
        slots = ['Cat', 'Dog']
        with self.assertRaises(TypeError):
            lex.ResponseBuilder.confirm_intent(slots=slots)

    def test_raise_confirm_intent_without_slots(self):
        intent_name = 'AnimalIntent'
        with self.assertRaises(TypeError):
            lex.ResponseBuilder.confirm_intent(intent_name=intent_name)

    def test_raise_delegate_without_slots(self):
        with self.assertRaises(TypeError):
            lex.ResponseBuilder.delegate()

    def test_raise_close_without_fulfillment_state(self):
        with self.assertRaises(TypeError):
            lex.ResponseBuilder.close()
