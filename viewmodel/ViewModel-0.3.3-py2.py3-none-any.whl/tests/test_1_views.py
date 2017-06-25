
"""
named 'test_1_views to ensure this runs first as it is the most basic tests
"""
from unittest.mock import MagicMock

from datetime import datetime, date, time
from decimal import Decimal
from bson.objectid import ObjectId

import pytest
from objdict import (ObjDict)
from viewmodel.viewFields import (IdField, TxtField, EnumForeignField, IntField,
            DateField, TimeField, DateTimeField, Case, DecField,
            viewModelDB, BaseField, IdAutoField )

from viewmodel import DBMongoSource, viewFields

#import saltMongDB
#from sbextend import SaltReq
from viewmodel.viewModel import BaseView
from viewmodel.memberView import MemberView, CardView

@pytest.fixture
def req():
    res = MagicMock(spec=SaltReq)
    res.getData = {}
    res.postData = {}
    res.hostName = 'salt'
    res.saltScript = 'register'
    return res

@pytest.fixture
def testmid():
    return 8

class SampleView(BaseView):
    models_ = None
    id = IdField(name='sqlid', cases={})
    salt = IntField(cases={})
    label = TxtField('Label for Profile', 8)
    date = DateField('Date')
    time = TimeField('Time', cases={})
    datetime = DateTimeField('DateTime', cases={})
    newfield = TxtField('new', 10, cases={})
    amount = DecField()
    country = EnumForeignField('Default Country', session=viewModelDB,
                               dispFields=('countries.countryName', ),
                               values='countries.phoneCode'
                              )
    first_name = TxtField(src='.name', cases={})

    #favourites  = FavField('theFavs!')
    #extra = TxtField('used as a dummy',src=None)
    def getRows_(self):
        row = ObjDict(id=1)
        row.salt = 5
        row.label = 'Label'
        row.country = '061'
        row.amount = 270
        row.date = datetime(16, 2, 1)
        return [ObjDict(((self.row_name_, row), ))]

@pytest.fixture
def sampleView():
    return SampleView()

class SampleDefView(BaseView):
    models_ = None
    id = IdField(name='sqlid', cases={})
    salt = IntField(cases={}, value =5)
    label = TxtField('Label for Profile', 8 , value='Label')
    date = DateField('Date', datetime(16, 2, 1))
    newfield = TxtField('new', 10, cases={})
    amount = DecField(value = 270)


class SampleIdView(BaseView):
    models_ = None
    id = IdField(name='id')
    id2 = IdField(name='id')
    sid = IntField(name='sqlid')
    rawsql = BaseField(name='sqlid')
    rawid = BaseField(name='id')
    rawidu = BaseField(name='_id')
    auto = IdAutoField()
    salt = IntField(cases={})

@pytest.fixture
def sampleIdView():
    return SampleIdView()

class SampleIdView2(BaseView):
    models_ = None
    id = IdField()
    id2 = IdField(name='id')
    rawid = BaseField(name='id')
    rawidu = BaseField(name='_id')
    auto = IdAutoField()
    salt = IntField(cases={})

@pytest.fixture
def sampleIdView2():
    return SampleIdView2()

class TestFuncs:
    def test_str_to_date1(self):
        strto = viewFields.strToDate
        assert strto("2017/03/02") == datetime(2017,3,2)


class TestDefaults:
    def test_def_int(self):
        view = SampleDefView()
        assert view.dbRows_[0]['__None__'] == {} # ensure no actual data
        assert view.salt == 5 # but it looks like data through defaults
        assert view.label == 'Label'

class TestFields:
    def testText(self, sampleView):
        assert sampleView.label == 'Label'
        assert sampleView[0]['label'].value == 'Label'

    def testDateFld(self, sampleView):
        assert sampleView.date == date(16, 2, 1)
        #import pdb; pdb.set_trace()
        assert sampleView[0]['date'].strvalue == ' 1/02/0016'

    def xtestTimeFld(self, sampleView):
        assert sampleView.time == time(16, 15)
        #import pdb; pdb.set_trace()
        assert sampleView[0]['time'].strvalue == ' 1/02/0016'

    def testEnumKey(self, sampleView):
        assert sampleView.country.value == '061'

    def test_decimal_value(self, sampleView):
        assert sampleView.amount == Decimal('2.7')

    def test_new(self, sampleView):
        assert sampleView.newfield == ''

    def test_embed(self, sampleView):
        assert sampleView.first_name == ''

class TestSetFields:
    def testText(self, sampleView):
        assert sampleView.label == 'Label'
        assert sampleView[0]['label'].strvalue == 'Label'
        sampleView[0]['label'].strvalue = 'xLabel'
        assert sampleView[0]['label'].strvalue == 'xLabel'


    def testDateFld(self, sampleView):
        assert sampleView.date == date(16, 2, 1)
        assert sampleView[0]['date'].strvalue == ' 1/02/0016'
        #assert sampleView[0].date.strvalue == ' 1/02/0016'
        sampleView[0]['date'].strvalue = '02/03/2017'
        assert sampleView.date == date(2017, 3, 2)

    def testDateFld2(self, sampleView):
        assert sampleView.date == date(16, 2, 1)
        save = sampleView[0]['date'].strvalue
        assert save == ' 1/02/0016'
        #assert sampleView[0].date.strvalue == ' 1/02/0016'
        sampleView[0]['date'].strvalue = '02/03/2017'
        assert sampleView.date == date(2017, 3, 2)
        sampleView[0]['date'].strvalue = save
        assert sampleView.date == date(16, 2, 1)

    def test_date_from_str(self, sampleView):
        assert sampleView.date == date(16, 2, 1)
        save = sampleView[0]['date'].strvalue
        assert save == ' 1/02/0016'
        #assert sampleView[0].date.strvalue == ' 1/02/0016'
        sampleView.date = ' 2032017'
        assert sampleView.date == date(2017, 3, 2)
        sampleView[0]['date'].strvalue = save
        assert sampleView.date == date(16, 2, 1)

    def testTimeFld(self, sampleView):
        sampleView[0]['time'].strvalue = '10:15'
        assert sampleView.time == time(10, 15)

    def testDateTimeFld(self, sampleView):
        sampleView[0]['datetime'].strvalue = '2015/11/02 10:15'
        assert sampleView.datetime == datetime(2015, 11, 2, 10, 15)


    def test_dec_fld(self, sampleView):
        assert sampleView.amount == Decimal('2.7')
        assert sampleView[0]['amount'].strvalue == '2.7'
        sampleView[0]['amount'].strvalue = '3.50'
        assert sampleView.amount == Decimal('3.5')
        sampleView.amount = Decimal('1.23')
        assert sampleView.amount == Decimal('1.23')

    def test_set_embed(self, sampleView):
        assert sampleView.first_name == ''
        sampleView[0].first_name = 'fred'
        assert sampleView.first_name == 'fred'


    def test_id_fld(self, sampleIdView, sampleIdView2):
        siv, siv2 = sampleIdView, sampleIdView2
        assert siv.id == None
        assert siv.rawsql == None
        assert siv.sid == None
        assert siv.auto == None
        assert siv2.id == None
        siv.rawidu = 10
        assert siv.auto == 10
        siv.rawsql = 15
        siv.rawid = 12
        siv2.rawid = 112
        siv2.rawidu = 113
        assert siv.auto == 15
        assert siv.sid == 15
        assert siv.rawsql == 15
        assert siv.id == 12
        assert siv.id2 == 12
        assert siv2.id == 113
        assert siv2.id2 == 112

    def test_id_fld_set(self, sampleIdView, sampleIdView2):
        """ cheching type conversion on set of idfield
        """
        siv, siv2 = sampleIdView, sampleIdView2
        siv.id = None
        assert isinstance(siv.id2, ObjectId)

class TestLoops:
    """ testing row structure supports looping through rows
        and within rows through fields"""
    def test_loop_row(self, sampleView):
        loopcount = 0
        for row in sampleView:
            assert row.label == 'Label'
            loopcount += 1
        assert loopcount == 1

    def test_loop_fields(self, sampleView):
        row = sampleView[0]
        names = []
        values = []
        for field in row:
            names.append(field.name)
            values.append(field.value)
        assert names == ['label', 'date', 'amount', 'country']
        assert values == ['Label', date(16, 2, 1), Decimal('2.7'),
                          type(row.country)('061')]

    def test_loop_fields_loop(self, sampleView):
        row = sampleView[0]
        names = []
        for field in row.loop_(case=Case.allFields):
            names.append(field.name)
        assert names == ['sqlid', 'salt', 'label', 'date', 'time', 'datetime',
                         'newfield', 'amount', 'country', 'first_name']

class TestIndexAttr:
    """ testings access to attributes ViewRow """
    def test_row_index(self, sampleView):
        row = sampleView[0]
        assert row['label'].value == 'Label'
        with pytest.raises(TypeError):
            row['label'] = 5

class TestView_idx_labelsList:
    def test_view_(self, sampleView):
        assert sampleView.view_ is sampleView
        assert sampleView[0].view_ is sampleView

    def test_idx_(self, sampleView):
        assert sampleView.idx_ == 0
        with pytest.raises(AttributeError):
            sampleView.idx_ = 5

    def test_idx_row(self, sampleView):
        assert sampleView[0].idx_ == 0
        with pytest.raises(AttributeError):
            sampleView[0].idx_ = 5

    def test_labelsList(self, sampleView):
        assert sampleView.labelsList_() == ['no labels']

class EmptyView(BaseView):
    models_ = None
    id = IntField(name='sqlid', cases={})
    label = TxtField('Label for Profile', 8, value='hello')
    date = DateField('Date')


@pytest.fixture
def emptyView():
    return EmptyView()

class TestEmptyView:
    def test_init(self, emptyView):
        ev = emptyView
        assert len(ev) == 1
        assert ev.label == 'hello'




