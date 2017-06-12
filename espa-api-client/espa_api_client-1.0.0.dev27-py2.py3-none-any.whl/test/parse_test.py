import unittest
import espa_api_client.parse as api


class ParseTest(unittest.TestCase):

    def test_search_landsat_tiles_collection_id(self):
        """
        Tests if the LANDSAT IDs meet the new collection ID standard
        :return:
        """
        l8_expected = ['LC08L1TP015033201610222017021901T1']
        l7_expected = ['LE07L1TP015033201610142016110901T1']
        l8 = api.search_landsat_tiles("LC08_L1TP_015033_20161022_20170219_01_T1")
        l7 = api.search_landsat_tiles("LE07_L1TP_015033_20161014_20161109_01_T1")
        self.assertEqual(l8, l8_expected)
        self.assertEqual(l7, l7_expected)

    def test_search_landsat_tiles_invalid_id(self):
        """
        Tests if nothing is returned when fed a bad ID
        :return:
        """
        result = api.search_landsat_tiles("bad id")
        self.assertEqual(result, [])

    def test_search_modis_tiles_valid_id(self):
        """
        Tests if the MODIS ID is properly inputted
        :return:
        """
        expected = ['MYD13A1A2016345H11V050052016362010425']
        result = api.search_modis_tiles("MYD13A1.A2016345.h11v05.005.2016362010425")
        self.assertEqual(result, expected)

    def test_search_modis_tiles_invalid_id(self):
        """
        Tests if nothing is returned when fed a bad ID
        :return:
        """
        result = api.search_modis_tiles("bad id")
        self.assertEqual(result, [])
