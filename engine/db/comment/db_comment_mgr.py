#!/usr/bin/python
# -*- coding: UTF-8 -*
from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn
from utils.status_code import response_code
from utils.log_helper import lg
import datetime
import traceback

class DbCommentMgr(DbBase):

    def __check_table_id_exist(self, table_id, table_name, db_name, conn):
        condition = 'id="%s"' % table_id
        sql = self.create_select_sql(db_name, table_name, '*', condition)
        # print('Table: ', sql)
        form_info = self.execute_fetch_all(conn, sql)
        if form_info:
            return True
        else:
            return False
    def add_new_comment(self, user_key, account_id, request_data):
        try:
            conn = MysqlConn()
            db_name = configuration.get_database_name()

            input_form_id = request_data.get('input_form_id', None)
            comment = request_data.get('comment', None)
            table_name = 'inputFormTable'
            condition = "id='%s' order by history_id desc" % (input_form_id)
            fields = '*'
            sql = self.create_select_sql(db_name, table_name, fields, condition)
            input_form_infos = self.execute_fetch_all(conn, sql)
            if not input_form_infos:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'form not found'
                return data
            # do the user exist
            creator_id = user_key
            user_exist_flag = self.__check_table_id_exist(creator_id, 'userTable', db_name, conn)
            if not user_exist_flag:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'user not found'
                return data
            # get history id
            history_id = input_form_infos[0]['history_id']
            now = str(datetime.datetime.now())
            fields = ('input_form_id', 'history_id', 'creator_id', 'comment', 'create_time')
            values = (input_form_id, history_id, user_key, comment, now)
            sql = self.create_insert_sql(db_name, 'inputCommentTable', '({})'.format(', '.join(fields)), values)
            comment_id = self.insert_exec(conn, sql, return_insert_id=True)
            data = response_code.SUCCESS
            data['data'] = {"accountId": account_id,
                                            "comment": comment, "comment_id": comment_id,
                                            "time": now}
            return data
        except Exception as e:
            error = traceback.format_exc()
            lg.error(error)
            return response_code.ADD_DATA_FAIL

    def delete_comment(self, user_key, request_data):

        try:
            conn = MysqlConn()
            db_name = configuration.get_database_name()

            input_form_id = request_data.get('input_form_id', None)
            comment_id = request_data.get('comment_id', None)
            table_name = 'inputFormTable'
            condition = "id='%s' order by history_id desc" % (input_form_id)
            fields = '*'
            sql = self.create_select_sql(db_name, table_name, fields, condition)
            input_form_infos = self.execute_fetch_all(conn, sql)
            if not input_form_infos:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'form not found'
                return data
            # do the user exist
            creator_id = user_key
            user_exist_flag = self.__check_table_id_exist(creator_id, 'userTable', db_name, conn)
            if not user_exist_flag:
                data = response_code.ADD_DATA_FAIL
                data['msg'] = 'user not found'
                return data
            # get history id
            history_id = input_form_infos[0]['history_id']
            condition = 'id=%s and input_form_id=%s' % (comment_id, input_form_id)
            sql = self.create_delete_sql(db_name, 'inputCommentTable', condition)
            count = self.delete_exec(conn, sql)
            data = response_code.SUCCESS
            data['data'] = {'count': count}
            return data
        except Exception as e:
            error = traceback.format_exc()
            lg.error(error)
            return response_code.ADD_DATA_FAIL

comment_mgr = DbCommentMgr()
