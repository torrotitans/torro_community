#!/usr/bin/python
# -*- coding: UTF-8 -*
from common.common_time import get_system_datetime
from db.base import DbBase
from db.connection_pool import MysqlConn
from utils.log_helper import lg
import copy
import datetime
from utils.status_code import response_code
from config import configuration
import traceback
import json
import os
from config import config
config_name = os.getenv('FLASK_CONFIG') or 'default'
Config = config[config_name]

class DbOrgMgr(DbBase):
    """
    用户相关数据库表操作类
    """
    '''
    0.为用户配置一个最初的admin账号，且orgTable表，除id和admin_id外全为空；
    1.进入登录界面：
    *第一次用给定的admin账号和密码登录；
    2.前端获取org_name名字并设置在导航页面：
    如果org_name为空，则立即跳转到org设置页面配置：
          -- 填写org基本信息
          -- 选择密码登录/ldap
          -- 重新创建admin账号/配置ldap+设置admin email
    如果org_name不为空，正常跳转到选择角色界面
    
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
            lg.error(e)
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
            print('ldapTable sql:', sql)
            ldap_id = self.insert_exec(conn, sql, return_insert_id=True)
            ldap_info['id'] = ldap_id
            data = response_code.SUCCESS
            data['data'] = ldap_info
            return data
        except Exception as e:
            lg.error(traceback.format_exc())
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()


    def __set_smtp(self, smtp_info):
        conn = MysqlConn()
        try:
            smtp_host = smtp_info['smtp_host']
            smtp_account = smtp_info['smtp_account']
            smtp_pwd = smtp_info['smtp_pwd']
            smtp_port = smtp_info['smtp_port']
            smtp_ssl = smtp_info['smtp_ssl']
            create_time = smtp_info['create_time']


            db_name = configuration.get_database_name()

            # insert form
            fields = ('MAIL_HOST', 'MAIL_USER', 'MAIL_PASS', 'PORT', 'USE_SSL', 'CREATE_TIME',
                      'TIME_MODIFY', )
            values = (smtp_host, smtp_account, smtp_pwd, smtp_port, smtp_ssl, create_time)
            sql = self.create_insert_sql(db_name, 'smtpTable', '({})'.format(', '.join(fields)), values)
            print('smtpTable sql:', sql)
            smtp_id = self.insert_exec(conn, sql, return_insert_id=True)
            smtp_info['id'] = smtp_id
            data = response_code.SUCCESS
            data['data'] = smtp_info
            return data
        except Exception as e:
            lg.error(traceback.format_exc())
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def __delete_ldap(self):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = "1=1"
            delete_table_sql = self.create_delete_sql(db_name, "ldapTable", condition)
            # print('delete_table_sql ', delete_table_sql)
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()
    def __delete_smtp(self):

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            condition = "1=1"
            delete_table_sql = self.create_delete_sql(db_name, "smtpTable", condition)
            # print('delete_table_sql ', delete_table_sql)
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
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
            # print('orgTable sql:', sql)
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
                # print('admin adgroupTable sql:', sql)
                admin_group_id = self.insert_exec(conn, sql, return_insert_id=True)
            # insert org_to_adgroupTable
            fields = ('ORG_ID', 'AD_GROUP_ID', 'ROLE_LIST')
            values = (org_id, admin_group_id, json.dumps(['admin']))
            sql = self.create_insert_sql(db_name, 'org_to_adgroupTable', '({})'.format(', '.join(fields)), values)
            # print('admin org_to_adgroupTable sql:', sql)
            self.insert_exec(conn, sql, return_insert_id=True)

            select_condition = "GROUP_MAIL='%s' " % visitor_group
            select_table_sql = self.create_select_sql(db_name, "adgroupTable", "*", select_condition)
            ad_group_info = self.execute_fetch_one(conn, select_table_sql)
            if ad_group_info:
                visitor_group_id = ad_group_info['ID']
            # insert visitor group
            else:
                fields = ('GROUP_MAIL', 'CREATE_TIME', 'DES')
                values = (visitor_group, create_time, des)
                sql = self.create_insert_sql(db_name, 'adgroupTable', '({})'.format(', '.join(fields)), values)
                # print('visitor adgroupTable sql:', sql)
                visitor_group_id = self.insert_exec(conn, sql, return_insert_id=True)
            # insert org_to_adgroupTable
            fields = ('ORG_ID', 'AD_GROUP_ID', 'ROLE_LIST')
            values = (org_id, visitor_group_id, json.dumps(['viewer']))
            sql = self.create_insert_sql(db_name, 'org_to_adgroupTable', '({})'.format(', '.join(fields)), values)
            # print('visitor org_to_adgroupTable sql:', sql)
            self.insert_exec(conn, sql, return_insert_id=True)

            org_info['org_id'] = org_id
            org_info['admin_id'] = admin_group_id
            org_info['visitor_id'] = visitor_group_id
            data = response_code.SUCCESS
            data['data'] = org_info
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()
    def __delete_org(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            condition = "1=1"
            delete_table_sql = self.create_delete_sql(db_name, "orgTable", condition)
            # print('delete_table_sql ', delete_table_sql)
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
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
            # print('delete_table_sql ', delete_table_sql)
            self.delete_exec(conn, delete_table_sql)
            return response_code.SUCCESS
        except Exception as e:
            lg.error(e)
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
            smtp_info['smtp_pwd'] = org['smtp_pwd']
            smtp_info['smtp_port'] = org['smtp_port']
            smtp_info['smtp_ssl'] = org['smtp_ssl']
            smtp_info['create_time'] = create_time
            sql = self.create_select_sql(db_name, 'ldapTable', '*')
            ldap_infos = self.execute_fetch_all(conn, sql)
            if ldap_infos:
                self.__delete_adgroup_to_org()
                self.__delete_ldap()
                self.__delete_org()
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
            lg.error(traceback.format_exc())
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
            lg.error(traceback.format_exc())
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()


    # get org info
    def get_org_info(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'orgTable', '*')
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
            lg.error(e)
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
            org_info = self.execute_fetch_one(conn, sql)
            if org_info:
                data = response_code.SUCCESS
                data['data'] = org_info
            else:
                data = response_code.GET_DATA_FAIL
            return data
        except Exception as e:
            lg.error(e)
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
            # # print(data)
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
            smtp_info['smtp_ssl'] = org['smtp_ssl']
            smtp_info['create_time'] = create_time

            sql = self.create_select_sql(db_name, 'ldapTable', '*')
            ldap_infos = self.execute_fetch_all(conn, sql)
            if ldap_infos:
                data = response_code.ADD_DATA_FAIL
                return data
            sql = self.create_select_sql(db_name, 'orgTable', '*')
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
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_roles_info(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'roleTable', '*')
            org_info = self.execute_fetch_all(conn, sql)
            if org_info:
                data = response_code.SUCCESS
                data['data'] = org_info
            else:
                data = response_code.GET_DATA_FAIL
            return data
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_smtp(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'smtpTable', '*')
            smtp_info = self.execute_fetch_all(conn, sql)
            if smtp_info:
                return '', '', '', '', ''
            else:
                mail_host = smtp_info['MAIL_HOST']
                mail_user = smtp_info['MAIL_USER']
                mail_pass = smtp_info['MAIL_PASS']
                port = smtp_info['PORT']
                is_ssl = smtp_info['USE_SSL']
                return mail_host, mail_user, mail_pass, is_ssl, port
        except Exception as e:
            lg.error(e)
            return response_code.GET_DATA_FAIL
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
            user_info = self.execute_fetch_one(conn, sql)
            ad_group_list = json.loads(user_info.get('GROUP_LIST', []))
            print('ad_group_list:', ad_group_list)
            return ad_group_list
        except Exception as e:
            lg.error(e)
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
            user_info = self.execute_fetch_one(conn, sql)
            account_cn = user_info.get('ACCOUNT_CN', None)
            print('ACCOUNT_CN:', account_cn)
            return account_cn
        except Exception as e:
            lg.error(e)
            return None, None
        finally:
            conn.close()

    # get airflow info
    def get_airflow_url(self):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'orgTable', 'AIRFLOW_URL')
            org_info = self.execute_fetch_one(conn, sql)
            if org_info:
                return org_info['AIRFLOW_URL']
            else:
                return ''
        except Exception as e:
            lg.error(e)
            return ''
        finally:
            conn.close()

org_mgr = DbOrgMgr()
