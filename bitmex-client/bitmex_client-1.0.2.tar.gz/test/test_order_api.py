# coding: utf-8

"""
    BitMEX API

    ## REST API for the BitMEX Trading Platform  [Changelog](/app/apiChangelog)  ----  #### Getting Started   ##### Fetching Data  All REST endpoints are documented below. You can try out any query right from this interface.  Most table queries accept `count`, `start`, and `reverse` params. Set `reverse=true` to get rows newest-first.  Additional documentation regarding filters, timestamps, and authentication is available in [the main API documentation](https://www.bitmex.com/app/restAPI).  *All* table data is available via the [Websocket](/app/wsAPI). We highly recommend using the socket if you want to have the quickest possible data without being subject to ratelimits.  ##### Return Types  By default, all data is returned as JSON. Send `?_format=csv` to get CSV data or `?_format=xml` to get XML data.  ##### Trade Data Queries  *This is only a small subset of what is available, to get you started.*  Fill in the parameters and click the `Try it out!` button to try any of these queries.  * [Pricing Data](#!/Quote/Quote_get)  * [Trade Data](#!/Trade/Trade_get)  * [OrderBook Data](#!/OrderBook/OrderBook_getL2)  * [Settlement Data](#!/Settlement/Settlement_get)  * [Exchange Statistics](#!/Stats/Stats_history)  Every function of the BitMEX.com platform is exposed here and documented. Many more functions are available.  ----  ## All API Endpoints  Click to expand a section. 

    OpenAPI spec version: 1.2.0
    Contact: jose.oliveros.1983@gmail.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest

import bitmex_client
from bitmex_client.rest import ApiException
from bitmex_client.apis.order_api import OrderApi


class TestOrderApi(unittest.TestCase):
    """ OrderApi unit test stubs """

    def setUp(self):
        self.api = bitmex_client.apis.order_api.OrderApi()

    def tearDown(self):
        pass

    def test_order_amend(self):
        """
        Test case for order_amend

        Amend the quantity or price of an open order.
        """
        pass

    def test_order_amend_bulk(self):
        """
        Test case for order_amend_bulk

        Amend multiple orders.
        """
        pass

    def test_order_cancel(self):
        """
        Test case for order_cancel

        Cancel order(s). Send multiple order IDs to cancel in bulk.
        """
        pass

    def test_order_cancel_all(self):
        """
        Test case for order_cancel_all

        Cancels all of your orders.
        """
        pass

    def test_order_cancel_all_after(self):
        """
        Test case for order_cancel_all_after

        Automatically cancel all your orders after a specified timeout.
        """
        pass

    def test_order_close_position(self):
        """
        Test case for order_close_position

        Close a position. [Deprecated, use POST /order with execInst: 'Close']
        """
        pass

    def test_order_get_orders(self):
        """
        Test case for order_get_orders

        Get your orders.
        """
        pass

    def test_order_new(self):
        """
        Test case for order_new

        Create a new order.
        """
        pass

    def test_order_new_bulk(self):
        """
        Test case for order_new_bulk

        Create multiple new orders.
        """
        pass


if __name__ == '__main__':
    unittest.main()
