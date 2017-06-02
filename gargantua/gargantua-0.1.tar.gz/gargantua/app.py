import pymysql


class Gargantua:
    def __init__(self):
        self._type = ""
        self._table = ""
        self._insert_values = []
        self._insert_params = []
        self._select_values = []
        self._select_where_values = ""
        self._update_values = []
        self._update_params = []
        self._update_where_values = ""
        self._delete_where_values = ""

    def set_db(self, host, user, password, db):
        self._connection = pymysql.connect(host=host, user=user, passwd=password, db=db)
        self._connection = self._connection.cursor()

    def set_type(self, type):
        self._type = type

    def set_table(self, table):
        self._table = table

    def set_insert_params(self, params=[]):
        for param in params:
            self._insert_params.append(param)

    def set_insert_values(self, values=[]):
        for value in values:
            self._insert_values.append(value)

    def set_select_values(self, values=[]):
        for value in values:
            self._select_values.append(value)

    def set_select_where_values(self, values):
        self._select_where_values = values

    def set_update_values(self, values=[]):
        for value in values:
            self._update_values.append(value)

    def set_update_params(self, params=[]):
        for param in params:
            self._update_params.append(param)

    def set_update_where_values(self, values):
        self._update_where_values = values

    def set_delete_where_values(self, values):
        self._delete_where_values = values

    def reset(self):
        self._type = ""
        self._table = ""
        self._insert_values = []
        self._insert_params = []
        self._select_values = []
        self._select_where_values = ""
        self._update_values = []
        self._update_params = []
        self._update_where_values = ""
        self._delete_where_values = ""

    def query_builder(self):

        if self.__p_validation_type() == False:
            return "Type is not None"
        if self.__p_validation_table() == False:
            return "Table is not None"

        if self._type == "INSERT":
            if self._insert_values.__len__() == 0:
                return "Values is None"
            if self._insert_params.__len__() == 0:
                return "Param is None"

            result = self.__p_type_insert()
            return result

        elif self._type == "SELECT":
            if self._select_values.__len__() == 0:
                return "Values is None"

            result = self.__p_type_select()
            return result

        elif self._type == "UPDATE":
            if self._update_values.__len__() == 0:
                return "Values is None"

            result = self.__p_type_update()
            return result

        elif self._type == "DELETE":
            if self._delete_where_values.__len__() == 0:
                return "Values is None"

            result = self.__p_type_delete()
            return result

    def __p_type_insert(self):
        a = ""
        b = ""

        last_value_i = len(self._insert_values) - 1
        last_param_i = len(self._insert_params) - 1

        for i, value in enumerate(self._insert_values):
            if i != last_value_i:
                a += "'" + value + "'" + ","
            else:
                a += "'" + value + "'"

        for i, param in enumerate(self._insert_params):
            if i != last_param_i:
                b += "'" + param + "'" + ","
            else:
                b += "'" + param + "'"

        query = "INSERT INTO " + self._table + "(" + a + ")" + " VALUES " + "(" + b + ")"

        return query

    def __p_type_select(self):
        a = ""
        last_value_s = len(self._select_values) - 1

        for i, value in enumerate(self._select_values):
            if i != last_value_s:
                a += " " + value + ","
            else:
                a += " " + value

        query = "SELECT " + a + " FROM " + self._table

        if self._select_where_values is not "":
            query += " WHERE " + self._select_where_values

        return query

    def __p_type_update(self):
        a = ""
        b = ""

        last_value_u = len(self._update_values) - 1
        last_param_u = len(self._update_params) - 1

        for i, value in enumerate(self._update_values):
            if i != last_value_u:
                a += value + " , "
            else:
                a += value
                break

        a = a.split(",")

        for i, param in enumerate(self._update_params):
            a[i] += "=" + param

        c = ""
        for i, value in enumerate(a):
            if i != last_param_u:
                c += value + " ,"
            else:
                c += value

        query = "UPDATE " + self._table + " SET " + c

        if self._update_where_values is not "":
            query += " WHERE " + self._update_where_values

        return query

    def __p_type_delete(self):
        query = "DELETE FROM " + self._table + " WHERE " + self._delete_where_values

        return query

    def __p_validation_type(self):
        return (self._type != "")

    def __p_validation_table(self):
        return (self._table != "")
