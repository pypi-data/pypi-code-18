import logging
import sqlite3


class Connection(object):
    """ A sqlite3 wrapper, provide humanize API. Encouraged by Torndb
    """

    def __init__(self, database):
        self.database = database
        self._dbconn = None

    def reconnect(self, retry=3):
        """ reconnect database
        @retry default to be three times
        """
        for _ in range(retry):
            try:
                self._dbconn = sqlite3.connect(self.database)
                self._dbconn.row_factory = sqlite3.Row
                return
            except Exception:
                logging.error("unable to connect sqlite3: %s",
                              self.database, exe_info=True)

    def is_alive(self):
        """ check if the database connection is avaiable """
        return getattr(self, "_db", None) is not None

    def close(self):
        """ close database connection """
        if self.is_alive():
            self._dbconn.close()
            self._dbconn = None

    def __del__(self):
        self.close()

    def _ensure_connected(self):
        if getattr(self, "_db", None) is None:
            self.reconnect()

    def _cursor(self):
        self._ensure_connected()
        return self._dbconn.cursor()

    def _close_cursor(self, cursor):
        """ Closing the cursor would make sence regarding the alive database connection
        """
        if self.is_alive():
            cursor.close()

    def _execute(self, cursor, sql, *args, **kwargs):
        try:
            cursor.execute(sql, *args, **kwargs)
        except sqlite3.OperationalError:
            self.close()
            raise

    def find(self, sql, *args, **kwargs):
        """ SELECT """
        cursor = self._cursor()
        try:
            self._execute(cursor, sql, *args, **kwargs)
            return cursor.fetchall()
        finally:
            self._close_cursor(cursor)

    def findone(self, sql, *args, **kwargs):
        """ SELECT one """
        cursor = self._cursor()
        try:
            self._execute(cursor, sql, *args, **kwargs)
            return cursor.fetchone()
        finally:
            self._close_cursor(cursor)

    def execute_lastrowid(self, sql, *args, **kwargs):
        """ The lastrowid is only set if you issued an INSERT statement using the execute() method.
        For operations other than INSERT or when executemany() is called, lastrowid is set to None
        """
        cursor = self._cursor()
        try:
            self._execute(cursor, sql, *args, **kwargs)
            self._dbconn.commit()
            return cursor.lastrowid
        finally:
            self._close_cursor(cursor)

    def execute_rowcount(self, sql, *args, **kwargs):
        """ Excutes a SQL statement """
        cursor = self._cursor()
        try:
            self._execute(cursor, sql, *args, **kwargs)
            self._dbconn.commit()
            return cursor.rowcount
        finally:
            self._close_cursor(cursor)

    def executemany(self, sql, *args):
        """ Repeatedly excutes a SQL statement """
        cursor = self._cursor()
        try:
            cursor.executemany(sql, *args)
            self._dbconn.commit()
            return cursor.rowcount
        except sqlite3.OperationalError:
            self.close()
            raise
        finally:
            self._close_cursor(cursor)
