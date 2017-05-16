import pytest

import pandas.util.testing as tm
import pandas_datareader.data as web

from pandas import DataFrame
from pandas_datareader.data import DataReader


class TestOptionsWarnings(object):

    def test_options_source_warning(self):
        with tm.assert_produces_warning():
            web.Options('aapl')


class TestDataReader(object):
    def test_read_yahoo(self):
        gs = DataReader("GS", "yahoo")
        assert isinstance(gs, DataFrame)

    def test_read_yahoo_dividends(self):
        gs = DataReader("GS", "yahoo-dividends")
        assert isinstance(gs, DataFrame)

    def test_read_google(self):
        gs = DataReader("GS", "google")
        assert isinstance(gs, DataFrame)

    def test_read_fred(self):
        vix = DataReader("VIXCLS", "fred")
        assert isinstance(vix, DataFrame)

    def test_not_implemented(self):
        with pytest.raises(NotImplementedError):
            DataReader("NA", "NA")
