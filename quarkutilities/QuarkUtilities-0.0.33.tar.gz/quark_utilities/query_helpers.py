from bson.json_util import loads
import logging


def get_skip(self):
    skip = self.get_argument('skip', 0)
    return int(skip)


def get_limit(self, check_max_limit=True):
    max_limit = 1000
    limit = 0
    limit = self.get_argument('limit', None)
    if limit:
        if check_max_limit and int(limit) > max_limit:
            limit = max_limit
        return int(limit)


def get_select(self):
    select = None
    select_param = self.get_argument('select', None)
    if select_param:
        select = {}
        fields = select_param.split(',')
        for field in fields:
            field = field.strip()
            if field:
                select[field] = 1

    return select


def get_where(self):
    where = None
    where = self.request.body
    if where:
        try:
            json = loads(where)
            return json
        except Exception as ex:
            logging.error(ex)
            return None


def get_sort(handler):
    sort = None
    order_by = handler.get_argument('sort', None)
    if order_by:
        sort = []
        clauses = order_by.split(',')
        for clause in clauses:
            clause = clause.strip()
            if clause:
                if ' ' not in clause:
                    clause = clause + ' asc'
                sort.append(
                    (clause.split(' ')[0], -1 if clause.split(' ')[1] == 'desc' else 1))

    return sort
