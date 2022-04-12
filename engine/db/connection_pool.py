#!/usr/bin/python
# -*- coding: UTF-8 -*

import pymysql
from DBUtils.PooledDB import PooledDB
from config import configuration


class MysqlConn(object):

    __my_pool = None

    ### what kind of format to return the data
    TUPLE_CURSOR_MODE = pymysql.cursors.Cursor
    DICT_DICTCURSOR_MODE = pymysql.cursors.DictCursor
    TUPLE_SSCURSOR_MODE = pymysql.cursors.SSCursor
    DICT_SSDICTCURSOR_MODE = pymysql.cursors.SSDictCursor

    def __init__(self, database_name='DB', cur_type=pymysql.cursors.DictCursor):
        self.conn, self.user, self.password = MysqlConn.get_connection(database_name)
        self.cur = self.conn.cursor(cursor=cur_type)
    @staticmethod
    def get_connection(database_name):
        """
        :return:
        """
        database = configuration.get_database_configuration(database_name)
        host = database.get('host')
        port = int(database.get('port'))
        user = database.get('user')
        password = database.get('pwd')
        if MysqlConn.__my_pool is None:
            MysqlConn.__my_pool = PooledDB(creator=pymysql, mincached=1, maxcached=10, maxconnections=100,
                                           blocking=True,
                                           host=host, port=port, user=user, passwd=password,
                                           charset='utf8')
        return MysqlConn.__my_pool.connection(), user, password

    def close(self):
        """
        :return:
        """
        self.conn.close()
        self.cur.close()

