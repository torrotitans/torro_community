#!/usr/bin/python
# -*- coding: UTF-8 -*

import json

from common.common_time import get_system_datetime
from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn
from utils.status_code import response_code
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class DbLogMgr(DbBase):

    def get_pages_operation_log(self, current_page, page_size, search_data, time_scope):
        """
        :param current_page:
        :param page_size:
        :param search_data:
        :param time_scope:
        :return:
        """
        db_conn = MysqlConn()
        try:
            start_page = str((current_page - 1) * page_size)
            db_name = configuration.get_database_name()
            table_name = 'system_oper_log'
            fields = 'log_key, (select name from %s.users where id = user_key) as user_name,user_key,ip_address,level,description,time_create' % db_name

            condition = ''
            # 给定了查询字段
            if len(json.loads(search_data)) > 0:
                condition = self.create_vague_condition_sql(search_data)
            # 给定了查询时间类型
            if time_scope:
                time_scope = eval(time_scope)
                start_time = time_scope[0]
                end_time = time_scope[1]
                if condition:
                    condition += ' and time_create between ' + str(start_time) + ' and ' + str(end_time)
                else:
                    condition += 'time_create between ' + str(start_time) + ' and ' + str(end_time)
            condition += ' order by time_create desc'
            sql_count, sql = self.create_get_page_sql(db_name, table_name, fields, start_page, page_size, condition)
            result = self.execute_fetch_pages(db_conn, sql_count, sql, current_page, page_size)
            data = response_code.SUCCESS
            data['data'] = result.get('data_list')
            data['total'] = result.get('total_count')
            return data

        except Exception as e:
            logger.error("FN:DbLogMgr_get_pages_operation_log error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def add_operation_log(self, user_key, ip_address, level, description):
        """
        添加操作日志
        :param user_key:
        :param ip_address:
        :param level:
        :param description:
        :return:
        """
        try:
            db_conn = MysqlConn()
            time_create = get_system_datetime()
            db_name = configuration.get_database_name()
            table_name = 'system_oper_log'
            fields = '(user_key,ip_address,level,description,time_create)'
            pla_data = (user_key, ip_address, level, description, time_create)
            sql = DbBase.create_insert_sql(self, db_name, table_name, fields, pla_data)
            DbBase.execute_sql_return_count(self, db_conn, sql)
            db_conn.close()

        except:
            logger.error("FN:DbLogMgr_add_operation_log error:{}".format(traceback.format_exc()))
            
        finally:
            db_conn.close()

    def get_pages_system_log(self, current_page, page_size, search_data, time_scope):
        """
        page query system log
        :param current_page:
        :param page_size:
        :param search_data:
        :param time_scope:
        :return:
        """
        db_conn = MysqlConn()
        try:
            start_page = str((current_page - 1) * page_size)
            db_name = configuration.get_database_name()
            table_name = 'system_log'
            fields = 'log_key,title,source,ip_address,level,status,' \
                     'opinion,opinion_user,opinion_time,time_create,description'
            condition = ''
            # Check if search keyword exists
            if len(json.loads(search_data)) > 0:
                condition = self.create_vague_condition_sql(search_data)
            # Search specific time period
            if time_scope:
                time_scope = eval(time_scope)
                start_time = time_scope[0]
                end_time = time_scope[1]
                if condition:
                    condition += ' and TIME_CREATE between ' + str(start_time) + ' and ' + str(end_time)
                else:
                    condition += 'TIME_CREATE between ' + str(start_time) + ' and ' + str(end_time)
            sql_count, sql = self.create_get_page_sql(db_name, table_name, fields, start_page, page_size, condition)
            # Execute the query
            result = self.execute_fetch_pages(db_conn, sql_count, sql, current_page, page_size)
            data = response_code.SUCCESS
            data['data'] = result.get('data_list')
            data['total'] = result.get('total_count')
            return data
        except Exception as e:
            logger.error("FN:DbLogMgr_get_pages_system_log error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def update_system_log(self, log_key, opinion, opinion_user, status):
        """
        :param log_key
        :param opinion
        :param opinion_user
        :param status
        :return:
        """
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'system_log'
            condition = "log_key=%s" % log_key
            # check log status if it has been updated
            sql = self.create_select_sql(db_name, table_name, 'status', condition)
            log = self.execute_fetch_one(db_conn, sql)
            if log.get('status') == 2:
                return response_code.ALREADY_HANDLED
            # update the log
            opinion_time = get_system_datetime()
            update_group_fields = ['opinion', 'opinion_user', 'status', 'opinion_time']
            update_group_fields_value = [opinion, opinion_user, status, opinion_time]
            update_group_sql = self.create_update_sql(db_name, table_name, update_group_fields,
                                                      update_group_fields_value,
                                                      condition)
            self.updete_exec(db_conn, update_group_sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:DbLogMgr_update_system_log error:{}".format(traceback.format_exc()))
            return response_code.UPDATE_DATA_FAIL
        finally:
            db_conn.close()

    def get_pages_message(self, user_id, current_page, page_size, search_data):
        """
        :param user_id:
        :param current_page:
        :param page_size:
        :param search_data:
        :return:
        """
        db_conn = MysqlConn()
        try:
            start_page = str((current_page - 1) * page_size)
            db_name = configuration.get_database_name()
            table_name = 'inform_message'
            fields = 'id,title,content,create_time,status'
            condition = "user_id=%s" % user_id
            # check if search keyword exists
            if search_data:
                condition += ' and ' + self.create_vague_condition_sql(search_data)
            sql_count, sql = self.create_get_page_sql(db_name, table_name, fields, start_page, page_size, condition)
            logger.error("FN:DbLogMgr_get_pages_message {}_sql:{}".format(table_name,sql))
            result = self.execute_fetch_pages(db_conn, sql_count, sql, current_page, page_size)
            data = response_code.SUCCESS
            data['data'] = result.get('data_list')
            data['total'] = result.get('total_count')
            return data
        except Exception as e:
            logger.error("FN:DbLogMgr_get_pages_message error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    def update_message_status(self, id_list):
        """
        :param message_id:
        :return:
        """
        db_conn = MysqlConn()
        try:

            db_name = configuration.get_database_name()
            table_name = 'inform_message'
            for message_id in eval(id_list):
                condition = "id=%s" % message_id
                # Update system info
                update_fields = ['state']
                update_fields_value = [1]
                update_sql = self.create_update_sql(db_name, table_name, update_fields, update_fields_value, condition)

                self.updete_exec(db_conn, update_sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:DbLogMgr_update_message_status error:{}".format(traceback.format_exc()))
            return response_code.UPDATE_DATA_FAIL
        finally:
            db_conn.close()

    def get_message_count(self, creator):
        db_conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            table_name = 'inform_message'
            data = response_code.SUCCESS
            fields = 'id,title,content,create_time,state'
            condition = " state = 0"
            # 给定了查询字段
            sql_count, sql = self.create_get_page_sql(db_name, table_name, fields, 0, 9000000, condition)
            # 执行查询
            result = self.execute_fetch_pages(db_conn, sql_count, sql, 1, 9000000)
            data['data'] = result

            return data
        except Exception as e:
            logger.error("FN:DbLogMgr_get_message_count error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()


db_log = DbLogMgr()
