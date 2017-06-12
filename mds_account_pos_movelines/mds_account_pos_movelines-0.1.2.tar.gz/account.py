# -*- coding: utf-8 -*-

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from sql.functions import Substring, ToChar
from sqlextension import Concat2

__all__ = ['AccountMoveLine']
__metaclass__ = PoolMeta

sel_mvstate = [('draft', 'Draft'),('posted', 'Posted')]


class AccountMoveLine:
    __name__ = 'account.move.line'
    
    ml_number = fields.Function(fields.Char(string=u'Number', readonly=True), 
            'get_ml_linedata', searcher='search_ml_number')
    ml_crdate = fields.Function(fields.DateTime(string=u'Create date', readonly=True), 
            'get_ml_linedata')
    ml_account = fields.Function(fields.Char(string=u'Account', readonly=True), 
            'get_ml_linedata', searcher='search_ml_account')
    ml_accountname = fields.Function(fields.Char(string=u'Account name', readonly=True), 
            'get_ml_linedata', searcher='search_ml_accountname')
    ml_debit = fields.Function(fields.Numeric(string=u'Debit', readonly=True, digits=(16, 2)), 
            'get_ml_linedata', searcher='search_ml_debit')
    ml_credit = fields.Function(fields.Numeric(string=u'Credit', readonly=True, digits=(16, 2)), 
            'get_ml_linedata', searcher='search_ml_credit')
    ml_descr = fields.Function(fields.Char(string=u'Description', readonly=True), 
            'get_ml_linedata', searcher='search_ml_descr')
    ml_invoice = fields.Function(fields.Char(string=u'Invoice', readonly=True), 
            'get_ml_invoice', searcher='search_ml_invoice')
    ml_invoice_id = fields.Function(fields.Many2One(string=u'Invoice', readonly=True,
            model_name='account.invoice'), 'get_ml_invoice')
    ml_mvstate = fields.Function(fields.Selection(string=u'Move state', readonly=True, 
            selection=sel_mvstate), 'get_ml_linedata', searcher='search_ml_mvstate')
    ml_mvdate = fields.Function(fields.Date(string=u'Effective Date', readonly=True), 
            'get_ml_linedata', searcher='search_ml_mvdate')
    ml_postdate = fields.Function(fields.Date(string=u'Post date', readonly=True), 
            'get_ml_linedata', searcher='search_ml_postdate')
    ml_postno = fields.Function(fields.Char(string=u'Post No.', readonly=True), 
            'get_ml_linedata', searcher='search_ml_postno')
    ml_postdescr = fields.Function(fields.Char(string=u'Post description', readonly=True), 
            'get_ml_linedata', searcher='search_ml_postdescr')
    ml_journname = fields.Function(fields.Char(string=u'Journal name', readonly=True), 
            'get_ml_linedata', searcher='search_ml_journname')
    ml_journcode = fields.Function(fields.Char(string=u'Journal code', readonly=True), 
            'get_ml_linedata', searcher='search_ml_journcode')
    ml_journtype = fields.Function(fields.Char(string=u'Journal type', readonly=True), 
            'get_ml_linedata', searcher='search_ml_journtype')
    ml_pername = fields.Function(fields.Char(string=u'Period name', readonly=True), 
            'get_ml_linedata', searcher='search_ml_pername')
    ml_perstart = fields.Function(fields.Date(string=u'Period start', readonly=True), 
            'get_ml_linedata', searcher='search_ml_perstart')
    ml_perend = fields.Function(fields.Date(string=u'Period end', readonly=True), 
            'get_ml_linedata', searcher='search_ml_perend')
    ml_perstate = fields.Function(fields.Char(string=u'Period state', readonly=True), 
            'get_ml_linedata', searcher='search_ml_perstate')

    @classmethod
    def __setup__(cls):
        super(AccountMoveLine, cls).__setup__()
        cls._order.insert(0, ('ml_crdate', 'DESC'))

    @staticmethod
    def order_ml_debit(tables):
        tab_accmvline, _ = tables[None]
        return [tab_accmvline.debit]

    @staticmethod
    def order_ml_credit(tables):
        tab_accmvline, _ = tables[None]
        return [tab_accmvline.credit]

    @staticmethod
    def order_ml_descr(tables):
        tab_accmvline, _ = tables[None]
        return [tab_accmvline.description]

    @staticmethod
    def order_ml_crdate(tables):
        tab_accmvline, _ = tables[None]
        return [tab_accmvline.create_date]

    @staticmethod
    def order_ml_number(tables):
        tab_accmvline, _ = tables[None]
        return [tab_accmvline.move]

    @classmethod
    def search_ml_number(cls, name, clause):
        """ sql-code to search in number
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.mvnumber, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_perstate(cls, name, clause):
        """ sql-code to search in perstate
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.perstate, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_perend(cls, name, clause):
        """ sql-code to search in perend
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.perend, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_perstart(cls, name, clause):
        """ sql-code to search in perstart
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.perstart, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_pername(cls, name, clause):
        """ sql-code to search in pername
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.pername, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_journtype(cls, name, clause):
        """ sql-code to search in journtype
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.journtype, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_journcode(cls, name, clause):
        """ sql-code to search in journcode
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.journcode, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_journname(cls, name, clause):
        """ sql-code to search in journname
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.journname, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_postdescr(cls, name, clause):
        """ sql-code to search in postdescr
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.postdescr, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_postno(cls, name, clause):
        """ sql-code to search in postno
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.postno, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_postdate(cls, name, clause):
        """ sql-code to search in postdate
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.postdate, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_mvdate(cls, name, clause):
        """ sql-code to search in mvdate
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.mvdate, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_mvstate(cls, name, clause):
        """ sql-code to search in mvstate
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.mvstate, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_descr(cls, name, clause):
        """ sql-code to search in descr
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.descr, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_credit(cls, name, clause):
        """ sql-code to search in credit
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.credit, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_debit(cls, name, clause):
        """ sql-code to search in debit
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.debit, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_accountname(cls, name, clause):
        """ sql-code to search in accountname
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.accountname, clause[2])
                )
        return [('id', 'in', qu1)]

    @classmethod
    def search_ml_account(cls, name, clause):
        """ sql-code to search in account
        """
        Operator = fields.SQL_OPERATORS[clause[1]]
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(tab_sql.id_line,
                    where=Operator(tab_sql.account, clause[2])
                )
        return [('id', 'in', qu1)]
        
    @classmethod
    def get_ml_sql_table(cls):
        """ create sql-view
        """
        pool = Pool()
        AccountMove = pool.get('account.move')
        AccountMoveLine = pool.get('account.move.line')
        Account = pool.get('account.account')
        AccountJournal = pool.get('account.journal')
        AccountPeriod = pool.get('account.period')
        
        tab_accmv = AccountMove.__table__()
        tab_accmvline = AccountMoveLine.__table__()
        tab_acc = Account.__table__()
        tab_accjourn = AccountJournal.__table__()
        tab_accper = AccountPeriod.__table__()
        
        qu1 = tab_accmvline.join(tab_acc, condition=tab_acc.id==tab_accmvline.account
                ).join(tab_accmv, condition=tab_accmv.id==tab_accmvline.move
                ).join(tab_accjourn, condition=tab_accjourn.id==tab_accmv.journal
                ).join(tab_accper, condition=tab_accper.id==tab_accmv.period
                ).select(tab_accmvline.id.as_('id_line'),
                    tab_acc.code.as_('account'),
                    tab_acc.name.as_('accountname'),
                    tab_accmvline.create_date.as_('crdate'),
                    tab_accmvline.debit,
                    tab_accmvline.credit,
                    tab_accmvline.description.as_('descr'),
                    ToChar(tab_accmv.id, 'FM9999999999').as_('mvnumber'),
                    tab_accmv.state.as_('mvstate'),
                    tab_accmv.date.as_('mvdate'),
                    tab_accmv.post_date.as_('postdate'),
                    tab_accmv.post_number.as_('postno'),
                    tab_accmv.description.as_('postdescr'),
                    tab_accjourn.name.as_('journname'),
                    tab_accjourn.code.as_('journcode'),
                    tab_accjourn.type.as_('journtype'),
                    tab_accper.name.as_('pername'),
                    tab_accper.start_date.as_('perstart'),
                    tab_accper.end_date.as_('perend'),
                    tab_accper.state.as_('perstate'),
                )
        return qu1

    @classmethod
    def get_ml_linedata(cls, movelines, names):
        """ collect data
        """
        cursor = Transaction().cursor
        
        erg1 = {'ml_account': {}, 'ml_accountname':{}, 'ml_debit':{},
                'ml_credit':{}, 'ml_descr':{}, 'ml_mvstate': {},
                'ml_mvdate': {}, 'ml_postdate': {}, 'ml_postno': {},
                'ml_postdescr': {}, 'ml_journname': {}, 'ml_journcode': {},
                'ml_journtype':{}, 'ml_pername':{}, 'ml_perstart': {},
                'ml_perend': {}, 'ml_perstate':{}, 'ml_crdate':{}, 'ml_number':{},
            }
        
        tab_sql = cls.get_ml_sql_table()
        qu1 = tab_sql.select(where=tab_sql.id_line.in_([x.id for x in movelines]))

        cursor.execute(*qu1)
        l1 = cursor.fetchall()
        
        for i in l1:
            (id_line, account, accountname, crdate, debit, credit, descr, 
             mvnumber, mvstate, mvdate, postdate, postno, postdescr, 
             journname, journcode, journtype, pername, perstart, perend, perstate) = i

            erg1['ml_number'][id_line] = mvnumber
            erg1['ml_crdate'][id_line] = crdate
            erg1['ml_account'][id_line] = account
            erg1['ml_accountname'][id_line] = accountname
            erg1['ml_debit'][id_line] = debit
            erg1['ml_credit'][id_line] = credit
            erg1['ml_descr'][id_line] = descr
            erg1['ml_mvstate'][id_line] = mvstate
            erg1['ml_mvdate'][id_line] = mvdate
            erg1['ml_postdate'][id_line] = postdate
            erg1['ml_postno'][id_line] = postno
            erg1['ml_postdescr'][id_line] = postdescr
            erg1['ml_journname'][id_line] = journname
            erg1['ml_journcode'][id_line] = journcode
            erg1['ml_journtype'][id_line] = journtype
            erg1['ml_pername'][id_line] = pername
            erg1['ml_perstart'][id_line] = perstart
            erg1['ml_perend'][id_line] = perend
            erg1['ml_perstate'][id_line] = perstate
            
        for i in erg1.keys():
            if not i in names:
                del erg1[i]
        
        return erg1

    @classmethod
    def search_ml_invoice(cls, name, clause):
        """ sql-code to search in invoice
        """
        Operator = fields.SQL_OPERATORS[clause[1]]

        pool = Pool()
        AccountMove = pool.get('account.move')
        AccountMoveLine = pool.get('account.move.line')
        AccountInvoice = pool.get('account.invoice')
        AccountInvoice_AccountMoveLine = pool.get('account.invoice-account.move.line')
        
        tab_accmov = AccountMove.__table__()
        tab_accmov2 = AccountMove.__table__()
        tab_accmovln = AccountMoveLine.__table__()
        tab_accmovln2 = AccountMoveLine.__table__()
        tab_accinv = AccountInvoice.__table__()
        tab_accinv_accmvln = AccountInvoice_AccountMoveLine.__table__()
        
        # origin: account.invoice,...
        qu1 = tab_accmovln.join(tab_accmov, condition=tab_accmov.id==tab_accmovln.move
                ).join(tab_accinv, condition=tab_accinv.move==tab_accmov.id
                ).select(tab_accmovln.id,
                    where=(Substring(tab_accmov.origin, 1, 16) == u'account.invoice,') &
                        Operator(Concat2(ToChar(tab_accinv.invoice_date, u'YYYY'), u'-', tab_accinv.number), clause[2])
                )

        # origin: Null
        tab_moveinv = tab_accinv.join(tab_accinv_accmvln, condition=tab_accinv_accmvln.invoice==tab_accinv.id
                ).join(tab_accmovln, condition=tab_accmovln.id==tab_accinv_accmvln.line
                ).select(tab_accmovln.move.as_('id_move'),
                    Concat2(ToChar(tab_accinv.invoice_date, u'YYYY'), u'-', tab_accinv.number).as_('inv_no'),
                )
        qu2 = tab_accmovln2.join(tab_moveinv, condition=tab_moveinv.id_move==tab_accmovln2.move
                ).join(tab_accmov2, condition=tab_accmov2.id==tab_accmovln2.move
                ).select(tab_accmovln2.id,
                    where=(tab_accmov2.origin == None) & 
                        Operator(tab_moveinv.inv_no, clause[2])
                )

        return ['OR', ('id', 'in', qu1), ('id', 'in', qu2)]

    @classmethod
    def get_ml_invoice(cls, movelines, names):
        """ collect invoice-data
        """
        cursor = Transaction().cursor
        pool = Pool()
        erg1 = {'ml_invoice': {}, 'ml_invoice_id': {}}
        
        AccountMove = pool.get('account.move')
        AccountMoveLine = pool.get('account.move.line')
        AccountInvoice = pool.get('account.invoice')
        AccountInvoice_AccountMoveLine = pool.get('account.invoice-account.move.line')
        
        tab_accmov = AccountMove.__table__()
        tab_accmov2 = AccountMove.__table__()
        tab_accmovln = AccountMoveLine.__table__()
        tab_accmovln2 = AccountMoveLine.__table__()
        tab_accinv = AccountInvoice.__table__()
        tab_accinv_accmvln = AccountInvoice_AccountMoveLine.__table__()

        mvln_list = [x.id for x in movelines]
        # prep result
        for i in mvln_list:
            erg1['ml_invoice'][i] = u'n.a.'
            erg1['ml_invoice_id'][i] = None
        
        # origin: account.invoice,...
        qu1 = tab_accmovln.join(tab_accmov, condition=tab_accmov.id==tab_accmovln.move
                ).join(tab_accinv, condition=tab_accinv.move==tab_accmov.id
                ).select(tab_accmovln.id.as_('id_line'),
                    Concat2(ToChar(tab_accinv.invoice_date, u'YYYY'), u'-', tab_accinv.number).as_('inv_no'),
                    tab_accinv.id.as_('id_inv'),
                    where=(Substring(tab_accmov.origin, 1, 16) == u'account.invoice,') &
                        (tab_accmovln.id.in_(mvln_list))
                )
        cursor.execute(*qu1)
        l1 = cursor.fetchall()
        for i in l1:
            (id_line, inv_no, id_inv) = i
            erg1['ml_invoice'][id_line] = inv_no
            erg1['ml_invoice_id'][id_line] = id_inv

        # origin: Null
        tab_moveinv = tab_accinv.join(tab_accinv_accmvln, condition=tab_accinv_accmvln.invoice==tab_accinv.id
                ).join(tab_accmovln, condition=tab_accmovln.id==tab_accinv_accmvln.line
                ).select(tab_accmovln.move.as_('id_move'),
                    Concat2(ToChar(tab_accinv.invoice_date, u'YYYY'), u'-', tab_accinv.number).as_('inv_no'),
                    tab_accinv.id.as_('id_inv')
                )
        qu2 = tab_accmovln2.join(tab_moveinv, condition=tab_moveinv.id_move==tab_accmovln2.move
                ).join(tab_accmov2, condition=tab_accmov2.id==tab_accmovln2.move
                ).select(tab_accmovln2.id.as_('id_line'),
                    tab_moveinv.inv_no,
                    tab_moveinv.id_inv,
                    where=(tab_accmov2.origin == None) & 
                        (tab_accmovln2.id.in_(mvln_list))
                )
        
        cursor.execute(*qu2)
        l2 = cursor.fetchall()
        for i in l2:
            (id_line, inv_no, id_inv) = i
                
            erg1['ml_invoice'][id_line] = inv_no
            erg1['ml_invoice_id'][id_line] = id_inv

        for i in erg1.keys():
            if not i in names:
                del erg1[i]
        return erg1
        
# ende AccountMoveLine
