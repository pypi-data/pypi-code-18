# encoding=utf-8

import copy
import sys
from datetime import datetime

pyver = sys.version_info.major

if pyver == 2:
    from HTMLParser import HTMLParser
elif pyver == 3:
    from html.parser import HTMLParser
else:
    raise Exception("Not supported Python version")

DATETIME_FORMAT_LOCAL = "%Y.%m.%d %H:%M"
DATETIME_FORMAT_INTL = "%Y년%m월%d일 %H:%M"

RECEIPT_FIELDS = {'amount': '사용금액',
                  'card_name': '카드명',
                  'card_installment': '사용구분',
                  'date': '사용일시',
                  'store_name': '가맹점명',
                  'type': '구분'}

RECEIPT_INIT = {'amount': None,
                'currency': None,
                'card_name': None,
                'card_installment': None,
                'date': None,
                'store_name': None,
                'type': None}


class BccardHtmlParser(HTMLParser):
    STATUS_LIST = ('init',
                   'itemsearch', # status where searching 'filed name'
                   'valuesearch', # status where searching 'value of filed'
                   'done')

    _receipt = None
    _ctx = {'status': 'init'}
    _curItem = ''
    _jump_next_tag_flag = False # if True, jump to next sibling tag(ex. td)

    def __init__(self, receipt):
        self._receipt = receipt
        self._ctx = {'status': 'init'}
        HTMLParser.__init__(self)

    # def reset(self):
    #     self._ctx = {'status': 'init'}

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'td':
            # print("starttag:" + tag)
            if self._ctx['status'] == 'init':
                self._ctx['status'] = 'itemsearch'
                # print("_ctx:" + "init -> itemsearch")
            elif self._ctx['status'] == 'valuesearch':
                self._ctx['status'] = 'valuesearch'
                self._jump_next_tag_flag = True
                # print("_ctx:" + self._ctx['status'] + " -> valuesearch")
            else:
                pass
        else:
            pass

    def handle_data(self, data):
        # print("data:" + data)
        if self._ctx['status'] == 'valuesearch' and self._jump_next_tag_flag == True:
            self._receipt[self._curItem] = data.strip()

            # print("_ctx:" + self._ctx['status'] + " -> init")
            self._ctx['status'] = 'init'
            self._curItem = ''
            self._jump_next_tag_flag = False

        if self._ctx['status'] == 'itemsearch':
            if data == RECEIPT_FIELDS['amount']:
                self._curItem = 'amount'
                self._ctx['status'] = 'valuesearch'
            elif data == RECEIPT_FIELDS['card_name']:
                self._curItem = 'card_name'
                self._ctx['status'] = 'valuesearch'
            elif data == RECEIPT_FIELDS['card_installment']:
                self._curItem = 'card_installment'
                self._ctx['status'] = 'valuesearch'
            elif data == RECEIPT_FIELDS['date']:
                self._curItem = 'date'
                self._ctx['status'] = 'valuesearch'
            elif data == RECEIPT_FIELDS['store_name']:
                self._curItem = 'store_name'
                self._ctx['status'] = 'valuesearch'
            else:
                # print("_ctx:" + self._ctx['status'] + " -> init")
                self._ctx['status'] = 'init'
                self._curItem = ''

    def handle_endtag(self, tag):
        if tag == 'html':
            self._ctx['status'] = 'done'

    def _strip_amount(self, value):
        return value.replace(',', '').strip()


class BccardParser(object):
    _receipt = None
    _bc_html_parser = None
    _encoding = None

    def __init__(self):
        pass

    def _validate_receipt(self):
        # todo: check whether all fields of the receipt are populated
        return

    def _strip_amount(self, value):
        return value.replace(',', '').strip()

    def _post_process(self):
        # populate 'currency' and 'type'

        if pyver == 2:
            amount_str = unicode(self._receipt['amount'], 'utf-8')
        else:
            amount_str = self._receipt['amount']

        # print(unicode(amount_str, 'utf-8'))
        if amount_str[len(amount_str)-1:] == u'원':
            amount = self._strip_amount(amount_str[:len(amount_str) - 1])
            currency = 'KRW'
            type = '국내'
        elif amount_str[len(amount_str)-3:].isdigit() == False:
            amount = self._strip_amount(amount_str[:len(amount_str) - 3])
            currency = amount_str[len(amount_str)-3:]
            type = '해외'
        else:
            raise Exception('Unable to parse \'amount\'. ' + amount_str)

        self._receipt['amount'] = amount
        self._receipt['currency'] = currency
        self._receipt['type'] = type

        # convert Date String to Datetime type. Date-format of local receipt is different from intl.'s one.
        if type == '국내':
            date = datetime.strptime(self._receipt['date'], DATETIME_FORMAT_LOCAL)
        elif type == '해외':

            if pyver == 2:
                s = unicode(self._receipt['date'], 'utf-8')
            else:
                s = self._receipt['date']

            date = datetime(year=int(s[0:4]),
                            month=int(s[5:7]),
                            day=int(s[8:10]),
                            hour=int(s[12:14]),
                            minute=int(s[15:17]),
                            second=int(s[18:20]))
        else:
            raise Exception('Unsupported type: ' + type)

        self._receipt['date'] = date

    def parse(self, html, encoding):
        self._encoding = encoding
        if pyver == 2:
            if encoding != 'utf-8':
                html = html.decode(encoding).encode('utf-8')

        self._receipt = copy.deepcopy(RECEIPT_INIT)
        self._bc_html_parser = BccardHtmlParser(self._receipt)
        self._bc_html_parser.feed(html)
        self._post_process()
        self._validate_receipt()
        self._bc_html_parser.close()

    def get_result(self):
        return self._receipt
