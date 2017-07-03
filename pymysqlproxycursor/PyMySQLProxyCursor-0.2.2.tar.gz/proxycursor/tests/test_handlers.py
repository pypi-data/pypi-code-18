# -*- coding: utf-8 -*-
import pymysql
import proxycursor

from proxycursor.tests import base


__all__ = ['TestHandlers']


def sale_reco_idx_on_insert(cursor, tblname):
    cursor.execute('SELECT idx FROM {0} WHERE idx = (SELECT LAST_INSERT_ID())'.format(tblname))
    result = cursor.fetchone()
    print result
    return result['idx']


def sale_reco_idx_on_update(cursor, tblname):
    cursor.execute('SELECT idx FROM {0} ORDER BY updated_at DESC LIMIT 1'.format(tblname))
    result = cursor.fetchone()
    print result
    return result['idx']


def sync_available_room(cursor, sale_reco_idx):
    query = """
        UPDATE
            sale_reco S
        SET
            S.available_rooms = S.cap - (
                SELECT
                    count(*) AS count
                FROM
                    reservation_rec_single RS
                LEFT JOIN reservation_rec RR
                    ON RS.idx = RR.reservation_rec_single_idx
                WHERE 1=1
                    AND RR.saleidx = %s
        )
        WHERE 1=1
            AND S.idx = %s
    """
    cursor.execute(query, (sale_reco_idx,sale_reco_idx))


class SaleRecoSync(object):
    def __init__(self):
        self.tblname = 'sale_reco'

    def after_insert(self, **kwargs):
        cursor = kwargs['cursor']
        idx = sale_reco_idx_on_insert(cursor, self.tblname)
        sync_available_room(cursor, idx)

    def after_update(self, **kwargs):
        cursor = kwargs['cursor']
        idx = sale_reco_idx_on_update(cursor, self.tblname)
        sync_available_room(cursor, idx)


class TestHandlers(base.PyMySQLProxyCursorTestCase):

    def setUp(self):
        super(TestHandlers, self).setUp()
        conn = self.connections[0]
        self.cursor = proxycursor.wrap(conn.cursor(pymysql.cursors.DictCursor), handlers=[SaleRecoSync()])

    def test_hook_after_insert(self):
        query = """
          INSERT INTO 
            `sale_reco` (
              `hotelidx`, 
              `roomidx`, 
              `price`, 
              `discount`, 
              `sday`, 
              `cap`, 
              `checkin`, 
              `checkout`, 
              `deposit`, 
              `bed_type`, 
              `hide`, 
              `selling_price`, 
              `delta_price`, 
              `site_special_code`, 
              `is_block`, 
              `hold_by_hotel`, 
              `is_dailychoice`, 
              `available_rooms`, 
              `regdate`, 
              `updated_at`
            ) VALUES (
              26201, 
              237194, 
              0, 
              30000, 
              '2018-01-01', 
              10, 
              '2018-01-10 00:00:00', 
              '2018-01-10 00:00:00', 
              26400, 
              5, 
              0, 
              30000, 
              0, 
              1, 
              0, 
              0, 
              1,
              0, 
              '2017-07-21 11:34:30', 
              '2017-07-21 11:34:30'
            )
        """
        self.cursor.execute(query)

