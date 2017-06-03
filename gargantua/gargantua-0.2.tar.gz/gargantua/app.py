import pymysql

from transaction import TransactionType
from constants import ConstantsMessage


class Gargantua:
    def __init__(self):
        self.__type = TransactionType.Nothing
        self.__table = ""
        self.__insert_values = []
        self.__insert_params = []
        self.__select_values = []
        self.__select_where_values = ""
        self.__update_values = []
        self.__update_params = []
        self.__update_where_values = ""
        self.__delete_where_values = ""
        self.__current_query = ""

    def reset(self):
        self.__type = ""
        self.__table = ""
        self.__insert_values = []
        self.__insert_params = []
        self.__select_values = []
        self.__select_where_values = ""
        self.__update_values = []
        self.__update_params = []
        self.__update_where_values = ""
        self.__delete_where_values = ""
        self.__current_query = ""

    def set_db(self, host, user, password, db):

        self.__connection = pymysql.connect(host=host,
                                            user=user,
                                            passwd=password,
                                            db=db,
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor)

        self.__cursor = self.__connection.cursor()

    def set_type(self, type):
        self.__type = type

    def set_table(self, table):
        self.__table = table

    def set_insert_params(self, params=[]):
        for param in params:
            self.__insert_params.append(param)

    def set_insert_values(self, values=[]):
        for value in values:
            self.__insert_values.append(value)

    def set_select_values(self, values=[]):
        for value in values:
            self.__select_values.append(value)

    def set_select_where_values(self, values):
        self.__select_where_values = values

    def set_update_values(self, values=[]):
        for value in values:
            self.__update_values.append(value)

    def set_update_params(self, params=[]):
        for param in params:
            self.__update_params.append(param)

    def set_update_where_values(self, values):
        self.__update_where_values = values

    def set_delete_where_values(self, values):
        self.__delete_where_values = values

    def close(self):
        self.__connection.close()
        self.__cursor.close()

    def query_builder(self):

        if self.__p_validation_type() == False:
            return ConstantsMessage.type_none_error

        if self.__p_validation_table() == False:
            return ConstantsMessage.table_none_error

        if self.__type == TransactionType.Insert:

            if self.__insert_values.__len__() == 0:
                return ConstantsMessage.value_none_error

            if self.__insert_params.__len__() == 0:
                return ConstantsMessage.param_none_error

            result = self.__p_type_insert()
            self.__current_query = result

            return result

        elif self.__type == TransactionType.Select:

            if self.__select_values.__len__() == 0:
                return ConstantsMessage.value_none_error

            result = self.__p_type_select()
            self.__current_query = result

            return result

        elif self.__type == TransactionType.Update:

            if self.__update_values.__len__() == 0:
                return ConstantsMessage.value_none_error

            if self.__update_params.__len__() == 0:
                return ConstantsMessage.param_none_error

            result = self.__p_type_update()
            self.__current_query = result

            return result

        elif self.__type == TransactionType.Delete:

            if self.__delete_where_values.__len__() == 0:
                return ConstantsMessage.value_none_error

            result = self.__p_type_delete()
            self.__current_query = result

            return result

    def execute(self):

        if self.__type == TransactionType.Select:

            self.__cursor.execute(self.__current_query)
            result = self.__cursor.fetchone()

            return result

        elif self.__type == TransactionType.Insert:

            self.__cursor.execute(self.__current_query, (self.__insert_params))
            self.__connection.commit()

            return True

        elif self.__type == TransactionType.Delete:

            self.__cursor.execute(self.__current_query)
            self.__connection.commit()

            return True

        elif self.__type == TransactionType.Update:

            self.__cursor.execute(self.__current_query)
            self.__connection.commit()

            return True

    def __p_type_insert(self):

        a = ""
        b = ""
        c = ""

        last_value_i = len(self.__insert_values) - 1
        last_param_i = len(self.__insert_params) - 1

        for i, value in enumerate(self.__insert_values):

            if i != last_value_i:
                a += value + ","
            else:
                a += value

        for i, param in enumerate(self.__insert_params):

            if i != last_param_i:
                c += "%s" + " ,"

                if not isinstance(param, int):
                    b += "'" + param + "'" + ","

                else:
                    b += "'" + str(param) + "'" + ","
            else:

                c += "%s"

                if not isinstance(param, int):
                    b += "'" + param + "'" + ","

                else:
                    b += "'" + str(param) + "'"

        query = "INSERT INTO " + self.__table + "(" + a + ")" + " VALUES " + "(" + c + ")"

        return query

    def __p_type_select(self):

        a = ""
        last_value_s = len(self.__select_values) - 1

        for i, value in enumerate(self.__select_values):

            if i != last_value_s:
                a += " " + value + ","

            else:
                a += " " + value

        query = "SELECT " + a + " FROM " + self.__table

        if self.__select_where_values is not "":
            query += " WHERE " + self.__select_where_values

        return query

    def __p_type_update(self):

        a = ""
        b = ""

        last_value_u = len(self.__update_values) - 1
        last_param_u = len(self.__update_params) - 1

        for i, value in enumerate(self.__update_values):

            if i != last_value_u:
                a += value + " , "

            else:
                a += value
                break

        a = a.split(",")

        for i, param in enumerate(self.__update_params):
            a[i] += "=" + "'" + param + "'"

        c = ""
        for i, value in enumerate(a):

            if i != last_param_u:
                c += value + " ,"
            else:
                c += value

        query = "UPDATE " + self.__table + " SET " + c

        if self.__update_where_values is not "":
            query += " WHERE " + self.__update_where_values

        return query

    def __p_type_delete(self):

        query = "DELETE FROM " + self.__table + " WHERE " + self.__delete_where_values

        return query

    def __p_validation_type(self):
        return (self.__type != "")

    def __p_validation_table(self):
        return (self.__table != "")
