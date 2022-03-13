#!/usr/bin/python
# -*- coding: UTF-8 -*
from common.common_time import get_system_datetime
from db.base import DbBase
from db.connection_pool import MysqlConn
import copy
import datetime
from utils.status_code import response_code
from config import configuration
import traceback
import json
import os
from config import config
import logging

logger = logging.getLogger("main." + __name__)

config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]

class DbOrgMgr(DbBase):
    """
    User related db operation
    """
    '''
    0. Default there is an admin account
    1. Use default admin account for first login 
    2. Setup the org_name in the UI portal
        if org_name is empty:
            then go to org setup
            -- fill in the org info
            -- setup ldap login
            -- setup smtp and airflow url
    '''
    def __delete_admin(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = "ID=%s and ACCOUNT_NAME =%s" % ('1', 'TorroAdmin')
            delete_table_sql = self.create_delete_sql(db_name, "userTable", condition)
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:__delete_admin error:{}".format(traceback.format_exc()))
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()


    def __set_ldap(self, ldap_info):
        conn = MysqlConn()
        try:
            host = ldap_info['host']
            port = ldap_info['port']
            cer_path = ldap_info['cer_path']
            use_ssl = ldap_info['use_ssl']
            admin = ldap_info['admin_dn']
            admin_pwd = ldap_info['admin_pwd']

            user_search_base = ldap_info['user_search_base']
            user_search_filter = ldap_info['user_search_filter']
            display_name_attribute = ldap_info['display_name_attribute']
            email_address_attribute = ldap_info['email_address_attribute']
            adgroup_attribute = ldap_info['adgroup_attribute']

            group_search_base = ldap_info['group_search_base']
            group_search_filter = ldap_info['group_search_filter']
            group_member_attribute = ldap_info['group_member_attribute']
            email_suffix = ldap_info['email_suffix']

            create_time = ldap_info['create_time']
            time_modify = ldap_info['time_modify']


            db_name = configuration.get_database_name()

            # insert form
            fields = ('HOST', 'PORT', 'CER_PATH', 'USE_SSL', 'ADMIN_DN', 'ADMIN_PWD',
                      'USER_SEARCH_BASE', 'USER_SERACH_FILTER', 'DISPLAY_NAME_LDAP_ATTRIBUTE', 'EMAIL_ADDRESS_LDAP_ATTRIBUTE', 'USER_ADGROUP_ATTRIBUTE',
                      'GROUP_SEARCH_BASE', 'GROUP_SERACH_FILTER', 'GROUP_MEMBER_ATTRIBUTE', 'GROUP_EMAIL_SUFFIX',
                      'CREATE_TIME', 'TIME_MODIFY')
            values = (host, port, cer_path, use_ssl, admin, admin_pwd,
                      user_search_base, user_search_filter, display_name_attribute, email_address_attribute, adgroup_attribute,
                      group_search_base, group_search_filter, group_member_attribute, email_suffix,
                      create_time, time_modify)
            sql = self.create_insert_sql(db_name, 'ldapTable', '({})'.format(', '.join(fields)), values)
            logger.debug('FN:__set_ldap ldapTable_sql:{}'.format(sql))
            ldap_id = self.insert_exec(conn, sql, return_insert_id=True)
            ldap_info['id'] = ldap_id
            data = response_code.SUCCESS
            data['data'] = ldap_info
            return data

        except Exception as e:
            logger.error("FN:__set_ldap error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL

        finally:
            conn.close()


    def __set_smtp(self, smtp_info):
        conn = MysqlConn()
        try:
            smtp_host = smtp_info['smtp_host']
            smtp_account = smtp_info['smtp_account']
            smtp_mail_box = smtp_info['Smtp_mail_box']
            smtp_pwd = smtp_info['smtp_pwd']
            smtp_port = smtp_info['smtp_port']
            smtp_tls = smtp_info['smtp_tls']
            create_time = smtp_info['create_time']


            db_name = configuration.get_database_name()

            # insert form
            fields = ('MAIL_HOST', 'MAIL_USER', 'MAIL_BOX', 'MAIL_PASS', 'PORT', 'USE_TLS', 'CREATE_TIME',
                      'TIME_MODIFY')
            values = (smtp_host, smtp_account, smtp_mail_box,  smtp_pwd, smtp_port, smtp_tls, create_time, create_time)
            sql = self.create_insert_sql(db_name, 'smtpTable', '({})'.format(', '.join(fields)), values)
            logger.debug('FN:__set_smtp smtpTable_sql:{}'.format(sql))
            smtp_id = self.insert_exec(conn, sql, return_insert_id=True)
            smtp_info['id'] = smtp_id
            data = response_code.SUCCESS
            data['data'] = smtp_info
            return data
        except Exception as e:
            logger.error("FN:__set_smtp error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def __delete_ldap(self):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = "1=1"
            delete_table_sql = self.create_delete_sql(db_name, "ldapTable", condition)
            logger.debug('FN:__delete_ldap delete_ldapTable_sql:{}'.format(sql))
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:__delete_ldap error:{}".format(traceback.format_exc()))
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()
            
    def __delete_smtp(self):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = "1=1"
            delete_table_sql = self.create_delete_sql(db_name, "smtpTable", condition)
            logger.debug('FN:__delete_smtp delete_smtpTable_sql:{}'.format(sql))
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:__delete_smtp error:{}".format(traceback.format_exc()))
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()

    def __set_org(self, org_info):

        conn = MysqlConn()
        try:
            admin_group = org_info['admin_group']
            visitor_group = org_info['base_group']
            org_name = org_info['org_name']
            airflow_url = org_info['airflow_url']
            create_time = org_info['create_time']
            des = org_info['des']
            db_name = configuration.get_database_name()

            # insert org
            fields = ('ORG_NAME', 'AIRFLOW_URL', 'CREATE_TIME', 'DES', 'PROJECT_NAME')
            values = (org_name, airflow_url, create_time, des, Config.DEFAULT_PROJECT)
            sql = self.create_insert_sql(db_name, 'orgTable', '({})'.format(', '.join(fields)), values)
            logger.debug('FN:__set_org orgTable_sql:{}'.format(sql))
            org_id = self.insert_exec(conn, sql, return_insert_id=True)

            select_condition = "GROUP_MAIL='%s' " % admin_group
            select_table_sql = self.create_select_sql(db_name, "adgroupTable", "*", select_condition)
            ad_group_info = self.execute_fetch_one(conn, select_table_sql)
            if ad_group_info:
                admin_group_id = ad_group_info['ID']
            else:
                # insert admin group
                fields = ('GROUP_MAIL', 'CREATE_TIME', 'DES')
                values = (admin_group, create_time, des)
                sql = self.create_insert_sql(db_name, 'adgroupTable', '({})'.format(', '.join(fields)), values)
                logger.debug('FN:__set_org adgroupTable_sql:{}'.format(sql))
                admin_group_id = self.insert_exec(conn, sql, return_insert_id=True)
            # insert org_to_adgroupTable
            fields = ('ORG_ID', 'AD_GROUP_ID', 'ROLE_LIST')
            values = (org_id, admin_group_id, json.dumps(['admin']))
            sql = self.create_insert_sql(db_name, 'org_to_adgroupTable', '({})'.format(', '.join(fields)), values)
            logger.debug('FN:__set_org org_to_adgroupTable_sql:{}'.format(sql))
            self.insert_exec(conn, sql, return_insert_id=True)

            select_condition = "GROUP_MAIL='%s' " % visitor_group
            select_table_sql = self.create_select_sql(db_name, "adgroupTable", "*", select_condition)
            logger.debug('FN:__set_org adgroupTable_sql:{}'.format(sql))
            ad_group_info = self.execute_fetch_one(conn, select_table_sql)
            
            if ad_group_info:
                visitor_group_id = ad_group_info['ID']
            # insert visitor group
            else:
                fields = ('GROUP_MAIL', 'CREATE_TIME', 'DES')
                values = (visitor_group, create_time, des)
                sql = self.create_insert_sql(db_name, 'adgroupTable', '({})'.format(', '.join(fields)), values)
                logger.debug('FN:__set_org adgroupTable_sql:{}'.format(sql))
                visitor_group_id = self.insert_exec(conn, sql, return_insert_id=True)
            # insert org_to_adgroupTable
            fields = ('ORG_ID', 'AD_GROUP_ID', 'ROLE_LIST')
            values = (org_id, visitor_group_id, json.dumps(['viewer']))
            sql = self.create_insert_sql(db_name, 'org_to_adgroupTable', '({})'.format(', '.join(fields)), values)
            logger.debug('FN:__set_org org_to_adgroupTable_sql:{}'.format(sql))
            self.insert_exec(conn, sql, return_insert_id=True)

            org_info['org_id'] = org_id
            org_info['admin_id'] = admin_group_id
            org_info['visitor_id'] = visitor_group_id
            data = response_code.SUCCESS
            data['data'] = org_info
            return data
        except Exception as e:
            logger.error("FN:__set_org error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()
            
    def __delete_org(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = "1=1"
            delete_table_sql = self.create_delete_sql(db_name, "orgTable", condition)
            logger.debug('FN:__delete_org delete_orgTable_sql:{}'.format(delete_table_sql))
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:__delete_org error:{}".format(traceback.format_exc()))
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()
            
    def __delete_adgroup_to_org(self, org_id=None):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            if not org_id:
                select_table_sql = self.create_select_sql(db_name, "orgTable", "*")
                org_id = self.execute_fetch_one(conn, select_table_sql)['ID']
            # select_condition = "ORG_ID=%s" % org_id
            # select_table_sql = self.create_select_sql(db_name, "org_to_adgroupTable", "*", select_condition)
            # ad_group_infos = self.execute_fetch_all(conn, select_table_sql)
            # for ad_group_info in ad_group_infos:
            #     ad_group_id = ad_group_info['AD_GROUP_ID']
            #     ad_condition = "ID=%s" % ad_group_id
            #     delete_table_sql = self.create_delete_sql(db_name, "adgroupTable", ad_condition)
            #     # print('delete_table_sql ', delete_table_sql)
            #     self.delete_exec(conn, delete_table_sql)
            delete_condition = "1=1"
            delete_table_sql = self.create_delete_sql(db_name, "org_to_adgroupTable", delete_condition)
            logger.debug('FN:__delete_adgroup_to_org delete_org_to_adgroupTable_sql:{}'.format(delete_table_sql))
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            logger.error("FN:__delete_adgroup_to_org error:{}".format(traceback.format_exc()))
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()


    def add_new_org_setting(self, org):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            org_info = {}
            org_info['admin_group'] = org['admin_group']
            org_info['base_group'] = org['base_group']
            org_info['org_name'] = org['org_name']
            org_info['airflow_url'] = org['airflow_url']
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            org_info['create_time'] = create_time
            org_info['des'] = org['des']

            ldap_info = {}
            ldap_info['host'] = org['host']
            ldap_info['port'] = org['port']
            ldap_info['cer_path'] = org['cer_path']
            ldap_info['use_ssl'] = org['use_ssl']
            ldap_info['admin_dn'] = org['admin_dn']
            ldap_info['admin_pwd'] = org['admin_pwd']

            ldap_info['user_search_base'] = org['user_search_base']
            ldap_info['user_search_filter'] = org['user_search_filter']
            ldap_info['display_name_attribute'] = org['display_name_attribute']
            ldap_info['email_address_attribute'] = org['email_address_attribute']
            ldap_info['adgroup_attribute'] = org['adgroup_attribute']

            ldap_info['group_search_base'] = org['group_search_base']
            ldap_info['group_search_filter'] = org['group_search_filter']
            ldap_info['group_member_attribute'] = org['group_member_attribute']
            ldap_info['email_suffix'] = org['email_suffix']

            ldap_info['create_time'] = create_time
            ldap_info['time_modify'] = create_time

            smtp_info = {}
            smtp_info['smtp_host'] = org['smtp_host']
            smtp_info['smtp_account'] = org['smtp_account']
            smtp_info['Smtp_mail_box'] = org['Smtp_mail_box']
            smtp_info['smtp_pwd'] = org['smtp_pwd']
            smtp_info['smtp_port'] = org['smtp_port']
            smtp_info['smtp_tls'] = org['smtp_tls']
            smtp_info['create_time'] = create_time
            sql = self.create_select_sql(db_name, 'ldapTable', '*')
            ldap_infos = self.execute_fetch_all(conn, sql)
            
            if ldap_infos:
                self.__delete_adgroup_to_org()
                self.__delete_ldap()
                self.__delete_org()
                self.__delete_smtp()
                # data = response_code.ADD_DATA_FAIL
                # return data
            # sql = self.create_select_sql(db_name, 'orgTable', '*')
            # org_infos = self.execute_fetch_all(conn, sql)
            # if org_infos:
            #     data = response_code.ADD_DATA_FAIL
            #     return data

            org_insert = self.__set_org(org_info)
            ldap_insert = self.__set_ldap(ldap_info)
            smtp_insert = self.__set_smtp(smtp_info)

            data = response_code.SUCCESS
            # self.__delete_admin()
            org['org_id'] = org_insert['data']['org_id']
            org['ldap_id'] = ldap_insert['data']['id']
            org['smtp_id'] = smtp_insert['data']['id']

            data['data'] = org
            return data
        
        except Exception as e:
            logger.error("FN:add_new_org_setting error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        
        finally:
            conn.close()


    def get_ldap_info(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'ldapTable', '*')
            ldap_info = self.execute_fetch_one(conn, sql)
            
            if ldap_info:
                data = response_code.SUCCESS
                data['data'] = ldap_info
                
            else:
                data = response_code.GET_DATA_FAIL
                
            return data
        
        except Exception as e:
            logger.error("FN:get_ldap_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        
        finally:
            conn.close()


    # get org info
    def get_org_info(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'orgTable', '*')
            logger.debug('FN:get_org_info orgTable_sql:{}'.format(sql))
            org_info = self.execute_fetch_one(conn, sql)
            if org_info:
                org_id = org_info['ID']
                db_name = configuration.get_database_name()
                condition = "ORG_ID=%s " % (org_id)
                relations = [{"table_name": "adgroupTable", "join_condition": "adgroupTable.ID=org_to_adgroupTable.AD_GROUP_ID"}]
                sql = self.create_get_relation_sql(db_name, 'org_to_adgroupTable', '*', relations, condition)
                ad_group_info = self.execute_fetch_all(conn, sql)
                org_info['ad_group_list'] = ad_group_info
                data = response_code.SUCCESS
                data['data'] = org_info
            else:
                data = response_code.GET_DATA_FAIL
            return data
        except Exception as e:
            logger.error("FN:get_org_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get org info
    def get_org_info_by_id(self, id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = "ID=%s " % (id)
            sql = self.create_select_sql(db_name, 'orgTable', '*', condition)
            logger.debug('FN:get_org_info_by_id orgTable_sql:{}'.format(sql))
            org_info = self.execute_fetch_one(conn, sql)
            if org_info:
                data = response_code.SUCCESS
                data['data'] = org_info
            else:
                data = response_code.GET_DATA_FAIL
            return data
        except Exception as e:
            logger.error("FN:get_org_info_by_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # modify org info
    def update_org_info(self, org):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            data = self.get_org_info_by_id(org['id'])
            if data['code'] != 200:
                return response_code.UPDATE_DATA_FAIL
            logger.debug("FN:update_org_info data".format(data))
            self.__delete_adgroup_to_org()
            self.__delete_ldap()
            self.__delete_org()
            self.__delete_smtp()
            org_info = {}
            org_info['admin_group'] = org['admin_group']
            org_info['base_group'] = org['base_group']
            org_info['org_name'] = org['org_name']
            org_info['airflow_url'] = org['airflow_url']
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            org_info['create_time'] = create_time
            org_info['des'] = org['des']

            ldap_info = {}
            ldap_info['host'] = org['host']
            ldap_info['port'] = org['port']
            ldap_info['cer_path'] = org['cer_path']
            ldap_info['use_ssl'] = org['use_ssl']
            ldap_info['admin_dn'] = org['admin_dn']
            ldap_info['admin_pwd'] = org['admin_pwd']

            ldap_info['user_search_base'] = org['user_search_base']
            ldap_info['user_search_filter'] = org['user_search_filter']
            ldap_info['display_name_attribute'] = org['display_name_attribute']
            ldap_info['email_address_attribute'] = org['email_address_attribute']
            ldap_info['adgroup_attribute'] = org['adgroup_attribute']

            ldap_info['group_search_base'] = org['group_search_base']
            ldap_info['group_search_filter'] = org['group_search_filter']
            ldap_info['group_member_attribute'] = org['group_member_attribute']
            ldap_info['email_suffix'] = org['email_suffix']

            ldap_info['create_time'] = create_time
            ldap_info['time_modify'] = create_time

            smtp_info = {}
            smtp_info['smtp_host'] = org['smtp_host']
            smtp_info['smtp_account'] = org['smtp_account']
            smtp_info['smtp_pwd'] = org['smtp_pwd']
            smtp_info['smtp_port'] = org['smtp_port']
            smtp_info['smtp_tls'] = org['smtp_tls']
            smtp_info['create_time'] = create_time

            sql = self.create_select_sql(db_name, 'ldapTable', '*')
            logger.debug('FN:update_org_info ldapTable_sql:{}'.format(sql))
            ldap_infos = self.execute_fetch_all(conn, sql)
            if ldap_infos:
                data = response_code.ADD_DATA_FAIL
                return data
            sql = self.create_select_sql(db_name, 'orgTable', '*')
            logger.debug('FN:update_org_info orgTable_sql:{}'.format(sql))
            org_infos = self.execute_fetch_all(conn, sql)
            if org_infos:
                data = response_code.ADD_DATA_FAIL
                return data

            org_insert = self.__set_org(org_info)
            ldap_insert = self.__set_ldap(ldap_info)
            smtp_insert = self.__set_smtp(smtp_info)
            data = response_code.SUCCESS
            self.__delete_admin()
            org['org_id'] = org_insert['data']['org_id']
            org['ldap_id'] = ldap_insert['data']['id']
            org['smtp_id'] = smtp_insert['data']['id']
            data['data'] = org
            return data
        
        except Exception as e:
            logger.error("FN:update_org_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        
        finally:
            conn.close()

    def get_roles_info(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'roleTable', '*')
            logger.debug('FN:get_roles_info roleTable_sql:{}'.format(sql))
            org_info = self.execute_fetch_all(conn, sql)
            
            if org_info:
                data = response_code.SUCCESS
                data['data'] = org_info
            else:
                data = response_code.GET_DATA_FAIL
            return data
        
        except Exception as e:
            logger.error("FN:get_roles_info error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        
        finally:
            conn.close()

    def get_smtp(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'smtpTable', '*')
            logger.debug('FN:get_smtp smtpTable_sql:{}'.format(sql))
            smtp_info = self.execute_fetch_one(conn, sql)
            
            if not smtp_info:
                return None, None, None, None, None, None
            else:
                mail_host = smtp_info['MAIL_HOST']
                mail_user = smtp_info['MAIL_USER']
                mail_box = smtp_info['MAIL_BOX']
                mail_pass = smtp_info['MAIL_PASS']
                port = smtp_info['PORT']
                is_tls = smtp_info['USE_TLS']
                return mail_host, mail_user, mail_box, mail_pass, port, is_tls
            
        except Exception as e:
            logger.error("FN:get_smtp error:{}".format(traceback.format_exc()))
            return None, None, None, None, None, None
        
        finally:
            conn.close()

    def offline_ad_group(self, account_id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # db_name2 = configuration.get_database_name('DB')
            condition = 'ACCOUNT_ID="%s"' % (account_id)
            user_fields = '*'
            sql = self.create_select_sql(db_name, 'userTable', user_fields, condition=condition)
            logger.debug('FN:offline_ad_group userTable_sql:{}'.format(sql))
            user_info = self.execute_fetch_one(conn, sql)
            ad_group_list = json.loads(user_info.get('GROUP_LIST', []))
            logger.debug('FN:offline_ad_group ad_group_list:{}'.format(ad_group_list))
            return ad_group_list
        
        except Exception as e:
            logger.error("FN:offline_ad_group error:{}".format(traceback.format_exc()))
            return None, None
        
        finally:
            conn.close()

    def get_user_cn(self, account_id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # db_name2 = configuration.get_database_name('DB')
            condition = 'ACCOUNT_ID="%s"' % (account_id)
            user_fields = '*'
            sql = self.create_select_sql(db_name, 'userTable', user_fields, condition=condition)
            logger.debug('FN:get_user_cn userTable_sql:{}'.format(sql))
            user_info = self.execute_fetch_one(conn, sql)
            account_cn = user_info.get('ACCOUNT_CN', None)
            logger.debug('FN:get_user_cn ACCOUNT_CN:{}'.format(sql))
            return account_cn
        
        except Exception as e:
            logger.error("FN:get_user_cn error:{}".format(traceback.format_exc()))
            return None, None
        
        finally:
            conn.close()

    # get airflow info
    def get_airflow_url(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'orgTable', 'AIRFLOW_URL')
            logger.debug('FN:get_airflow_url orgTable_sql:{}'.format(sql))
            org_info = self.execute_fetch_one(conn, sql)
            if org_info:
                return org_info['AIRFLOW_URL']
            else:
                return ''
        except Exception as e:
            logger.error("FN:get_airflow_url error:{}".format(traceback.format_exc()))
            return ''
        finally:
            conn.close()

    def insert_notification(self, emails, input_form_id, history_id, notify_msg):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            notify_id_list = []
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            emails = list(set(emails))
            logger.debug('FN:insert_notification emails:{} notify_msg'.format(emails, notify_msg))
            for email in emails:
                values = (email, input_form_id, history_id, notify_msg, 0, create_time)
                fields = ('account_id', 'input_form_id', 'history_id', 'comment', 'is_read', 'create_time')
                sql = self.create_insert_sql(db_name, 'inputNotifyTable', '({})'.format(', '.join(fields)), values)
                notify_id = self.insert_exec(conn, sql, return_insert_id=True)
                notify_id_list.append(str(notify_id))
            return notify_id_list
        
        except Exception as e:
            logger.error("FN:insert_notification error:{}".format(traceback.format_exc()))
            return []
        
        finally:
            conn.close()

org_mgr = DbOrgMgr()
