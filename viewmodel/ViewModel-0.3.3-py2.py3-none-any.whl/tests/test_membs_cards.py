"""
 tests of pymongo interface to members and cards
"""
from unittest.mock import MagicMock

from datetime import datetime, date
from decimal import Decimal

import pytest
from objdict import (ObjDict)
from viewmodel.viewFields import (IdField, TxtField, EnumForeignField, IntField,
            DateField, TimeField, Case, DecField,
            viewModelDB, BaseField, IdAutoField )

from viewmodel import DBMongoSource, viewFields

#import saltMongDB
#from sbextend import SaltReq
from viewmodel.viewModel import BaseView
from viewmodel.memberView import MemberView, CardView


@pytest.fixture
def memberView():
    return MemberView(dict(sqlid=8)) # ObjDict(memberID='ian')

@pytest.fixture
def membersView():
    return MemberView(dict()) # ObjDict(memberID='ian')

class TestMembers:
    def test_member(self, memberView):
        mv = memberView
        assert len(mv) == 1
        assert mv.memberID == 'ian'

    def test_member_given_name(self, memberView):
        mv = memberView
        assert len(mv) == 1
        assert mv.fields_['name'].src == 0
        assert mv.fields_['name'].raw_src == ''
        assert mv.fields_['name'].src_dicts == []
        assert mv.name.givenNames == 'iann'
        assert mv.fields_['givenNames'].src == 0
        assert mv.fields_['givenNames'].raw_src == '.name'
        assert mv.fields_['givenNames'].src_dicts == ['name']
        assert mv.givenNames == 'iann'


    def test_member_given_name_set(self, memberView):
        mv = memberView
        assert len(mv) == 1
        assert mv.name.givenNames == 'iann'
        assert mv.givenNames == 'iann'
        assert mv.quickName == 'ian3'
        with mv:
            mv.quickName = 'newname'
            mv.givenNames = 'testing'
            changes = mv.changes_[0]['members'].copy()
            assert mv.givenNames == 'testing'
            assert 'name.givenNames' in changes
            #import pdb; pdb.set_trace()
            #pass

    def test_view_form(self, memberView):
        mv = memberView
        names = 'memberID', 'quickName', 'name', 'nameType', 'plan'
        for nm, fld in zip(names, mv.fields_()):
            assert fld.name == nm

        assert fld.label == 'Shaker Type' #just testing last one

    def test_members_rows(self, membersView):
        mv = membersView
        assert len(mv) == 3
        names = 'ian', 'Michael', ' default'
        for n, m in zip(names, mv.fields_.loopRows()):
            assert m.memberID == n
            assert mv != m

    def test_members_index(self, membersView):
        mv = membersView
        assert mv[1].memberID == 'Michael'

class TestFieldAccess:
    def test_members_fields(self, membersView):
        mv = membersView
        assert len(mv) == 3
        names = 'ian', 'Michael', ' default'
        for n, m in zip(names, mv.fields_.loopRows()):
            its = m.fields_.items()
            key, value = list(its)[2]
            assert value.value == n

    def test_members_fields_row_fields_items(self, membersView):
        mv = membersView
        assert len(mv) == 3
        names = 'ian', 'Michael', ' default'
        for n, m in zip(names, mv):
            its = m.fields_.items()
            key, value = list(its)[2]
            assert value.value == n
            assert value.name == 'memberID'

    def test_members_fields_new(self, membersView):
        mv = membersView
        assert len(mv) == 3
        names = 'ian', 'Michael', ' default'
        for n, m in zip(names, mv):
            its = m.fields_.items()
            key, value = list(its)[2]
            assert value.value == n
            assert value.name == 'memberID'


class TestComplexFieldsUsingCardData:
    def test_access_inside(self):
        cv = CardView(8)
        c2 = cv[1]
        assert c2.membcard['sqlid'] == 96

    def test_change_inside(self):
        cv = CardView(8)
        c2 = cv[1]
        with c2:
            vals = c2.membcard
            vals['sqlid'] = 97
            vals.id = c2.id
            c2.membcard = vals
        assert c2.membcard['sqlid'] == 97
        assert c2.membcard['id'] == c2.id

    

class TestCards:
    def test_card_read(self):
        cv = CardView(8)
        c2 = cv[1]
        assert c2.membcard['sqlid'] == 97
        assert c2.label == 'c1'
        with pytest.raises(AssertionError):
            c2.nameOnCard == 'ian'
        with c2: #restore id to enable fetch from card
            vals = c2.membcard
            vals['sqlid'] = 96
            c2.membcard = vals
        assert c2.nameOnCard == 'ian'

    def test_card_update(self):
        cv = CardView(8)
        c2 = cv[1]
        with c2:
            c2.nameOnCard = 'Fred'
        assert cv.dbRows_[1]['cards'].nameOnCard == 'Fred'
        #cv.update_()
        cv = CardView(8)
        assert cv[1].nameOnCard == 'Fred'

    def test_card_labelupdate(self):
        cv = CardView(8)
        c2 = cv[1]
        with c2:
            c2.nameOnCard = 'Fred'
            c2.label = 'new label'
        assert cv.dbRows_[1]['cards'].nameOnCard == 'Fred'
        cv = CardView(8)
        assert cv[1].nameOnCard == 'Fred'
        assert cv[1].label == 'new label'

    def test_card_label_insert(self):
        cv = CardView(8)
        cnew = cv.insert_()
        with cnew:
            cnew.nameOnCard = 'Fred'
            cnew.label = 'new card'
        assert cv.dbRows_[3]['cards'].nameOnCard == 'Fred'
        assert cv.dbRows_[3]['members.cards'].label == 'new card'
        assert '_id' in cv.dbRows_[3]['cards']
        memb = cv.dbRows_[3]['members.cards']
        assert 'key' in memb

        # testing update of second  id link as used by salt app
        # salt uses second id link to allow legacy links in legacy records
        #
        with cnew:
            cnew.sqlid = cnew.id

        cv = CardView(8)
        assert cv[3].nameOnCard == 'Fred'
        assert cv[3].label == 'new card'
        