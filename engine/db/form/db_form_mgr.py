#!/usr/bin/python
# -*- coding: UTF-8 -*

import datetime
from db.base import DbBase
from db.connection_pool import MysqlConn
import copy
import traceback
from utils.status_code import response_code
from config import configuration
import json
from db.workflow.db_workflow_mgr import workflow_mgr
import traceback
import logging

logger = logging.getLogger("main." + __name__)

# from werkzeug.security import generate_password_hash, check_password_hash


class DbFormMgr(DbBase):
    """
    DB Form Operation
    """

    # form list
    def get_all_base_form(self, wp_id=0, uc_id=0, system=0):
        """
        get all form
        :return:
        """
        db_conn = MysqlConn()
        try:
            if not system:
                system = 0
            else:
                system = int(system)
            if system == 1:
                condition_list = ["available=1"]
            else:
                condition_list = ["available=1", "hide=0"]
            if wp_id != 0:
                condition_list.append('(workspace_id="%s" or workspace_id=0)' % (wp_id))
            if uc_id != 0:
                condition_list.append('usecase_id="%s"' % (uc_id))
            if len(condition_list) == 0:
                condition = 'id < 351'
            else:
                if system == 1:
                    condition = '(' + ' and '.join(condition_list) + ') or id < 351'
                else:
                    condition = '(' + ' and '.join(condition_list) + ') or (id < 351 and hide=0)'

            db_name = configuration.get_database_name()
            table_name = 'formTable'
            fields = 'id,title,fields_num,u_max_id,creator_id,create_time,updated_time,des,hide'
            sql = self.create_select_sql(db_name, table_name, fields, condition)
            logger.debug("FN:DbFormMgr_get_all_base_form {}_sql:{}".format(table_name,sql))
            result = self.execute_fetch_all(db_conn, sql)
            data = response_code.SUCCESS
            data['data'] = result
            return data

        except Exception as e:
            logger.error("FN:get_all_base_form error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            db_conn.close()

    # get base form
    def get_base_form_by_id(self, id):
        """
        get form base info
        :return:
        """
        conn = MysqlConn()
        try:
            condition = "id='%s'" % id
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'formTable',
                                         'id,title,fields_num,u_max_id,creator_id,create_time,updated_time,des',
                                         condition=condition)
            logger.debug("FN:DbFormMgr_get_base_form_by_id formTable_sql:{}".format(sql))
            form_info = self.execute_fetch_one(conn, sql)
            data = response_code.SUCCESS
            data['data'] = form_info
            return data
        except Exception as e:
            logger.error("FN:get_base_form_by_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get one form
    def get_details_form_by_id(self, id, wp_id=0, uc_id=0):
        """
        get form detail info
        :return:
        """
        conn = MysqlConn()
        try:
            condition_list = ['id="%s"' % id]
            if wp_id != 0 and id > 350:
                condition_list.append('(workspace_id="%s" or workspace_id=0)' % (wp_id))
            if uc_id != 0:
                condition_list.append('usecase_id="%s"' % (uc_id))
            if len(condition_list) == 0:
                condition = None
            else:
                condition = ' and '.join(condition_list)
            # condition = 'workspace_id="%s" and usecase_id="%s" and id="%s"' % (wp_id, uc_id, id)
            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'formTable', '*', condition=condition)
            logger.debug("FN:DbFormMgr_get_details_form_by_id formTable_sql:{}".format(sql))
            form_info = self.execute_fetch_one(conn, sql)
            if not form_info:
                data = response_code.GET_DATA_FAIL
                data['msg'] = 'cannot find form id: {}'.format(str(id))
                return data

            logger.debug("FN:DbFormMgr_get_details_form_by_id form_info:{}".format(form_info))
            form_info['fieldList'] = json.loads(form_info['fields_list'])
            del form_info['fields_list']
            region_field_info = {}
            for index, field_item in enumerate(form_info['fieldList']):
                if 's' in field_item['id']:
                    condition = "id='%s'" % str(field_item['id']).replace('s', '')
                    sql = self.create_select_sql(db_name, 'fieldTable',
                                                 'id,style,label,default_value,required,placeholder,value_num,value_list,edit,des,create_time,updated_time',
                                                 condition=condition)
                    logger.debug("FN:DbFormMgr_get_details_form_by_id fieldTable_sql:{}".format(sql))
                    field_info = self.execute_fetch_one(conn, sql)
                    if int(field_info['id']) == 1:
                        region_field_info = field_info
                        bool_mapping = {'1': True, '0': False}
                        region_field_info['required'] = bool_mapping[str(region_field_info['required'])]
                        region_field_info['options'] = json.loads(region_field_info['value_list'])
                        region_field_info['default'] = region_field_info['default_value']
                        del region_field_info['value_list'], region_field_info['default_value']
                        region_field_info['id'] = 's' + str(region_field_info['id'])
                        continue
                    field_info['options'] = json.loads(field_info['value_list'])
                    field_info['default'] = field_info['default_value']
                    del field_info['value_list'], field_info['default_value']
                    field_info['id'] = 's' + str(field_info['id'])
                    # # print(field_info)
                    form_info['fieldList'][index] = field_info
                if 'd' in field_item['id']:
                    dynamic_field_id = str(field_item['id']).replace('d', '')
                    # get dynamicField
                    condition = "id='%s'" % dynamic_field_id
                    sql = self.create_select_sql(db_name, 'dynamicFieldTable',
                                                 'id,style,label,default_value,placeholder,value_num,des,create_time',
                                                 condition=condition)
                    logger.debug("FN:DbFormMgr_get_details_form_by_id dynamicFieldTable_sql:{}".format(sql))
                    field_info = self.execute_fetch_one(conn, sql)
                    # get dynamicFieldValue
                    field_info = self.__get_dynamic_field_values(field_info, dynamic_field_id, wp_id, db_name, conn)
                    # condition = "dynamic_field_id='%s'" % dynamic_field_id
                    # sql = self.create_select_sql(db_name, 'dynamicFieldValueTable',
                    #                              'option_label,create_time', condition=condition)
                    # values_info = self.execute_fetch_all(conn, sql)
                    # field_info['options'] = []
                    # # print('field_info:', field_info)
                    # for value_info in values_info:
                    #     field_info['options'].append(
                    #         {'label': value_info['option_label'], 'value': value_info['option_label']})
                    # field_info['default'] = field_info['default_value']
                    # del field_info['default_value']
                    field_info['id'] = 'd' + str(field_info['id'])
                    # # print(field_info)
                    form_info['fieldList'][index] = field_info
                if 'u' in field_item['id']:
                    print('1111111111field_item:', field_item )
                    user_field_id = str(field_item['id']).replace('u', '')
                    # get dynamicFieldValue
                    # print('field_item:', field_item)
                    field_info = self.__get_user_field_values(field_item, user_field_id, wp_id, db_name, conn)

                    # condition = "user_field_id='%s'" % user_field_id
                    # sql = self.create_select_sql(db_name, 'dynamicFieldValueTable',
                    #                              'option_label,create_time', condition=condition)
                    # values_info = self.execute_fetch_all(conn, sql)
                    # field_info['options'] = []
                    # # print('field_info:', field_info)
                    # for value_info in values_info:
                    #     field_info['options'].append(
                    #         {'label': value_info['option_label'], 'value': value_info['option_label']})
                    # field_info['default'] = field_info['default_value']
                    # del field_info['default_value']
                    # field_info['id'] = 'u' + str(field_info['id'])
                    print('2222222222field_item::', field_info)

                    form_info['fieldList'][index] = field_info

            if wp_id != 0:
                condition = "ID=%s " % (wp_id)
                sql = self.create_select_sql(db_name, 'workspaceTable', 'REGOINS', condition)
                options = []
                regions = json.loads(self.execute_fetch_one(conn, sql)['REGOINS'])
                # print('region_field_info:', region_field_info)
                # print('regions:', regions)

                for region in regions:
                    options.append({'label': region['region'], 'value': region['region']})
                    for sub_region in region['countryList']:
                        options.append({'label': sub_region['country'], 'value': sub_region['workflow']})
                region_field_info['options'] = options
                region_field_info['value_num'] = len(options)
            if id == 2:
                form_info['fieldList'] = [region_field_info] + form_info['fieldList'][1:]
            # print('form_info: ', form_info)
            # get fields info
            data = response_code.SUCCESS
            data['data'] = form_info
            return data
        except Exception as e:
            logger.error("FN:get_details_form_by_id error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # get field template
    def get_field_template(self, style=0, wp_id=0):
        """
        get field template info
        :return:
        """
        conn = MysqlConn()
        try:
            default_id = ''
            return_info = {'style': style}
            condition_list = []
            if wp_id != 0:
                condition_list.append('(workspace_id="%s" or workspace_id=0)' % (wp_id))
            if style != 0:
                condition_list.append('style="%s"' % (style))
            if len(condition_list) == 0:
                condition = None
            else:
                condition = ' and '.join(condition_list)

            db_name = configuration.get_database_name()
            sql = self.create_select_sql(db_name, 'fieldTable',
                                         'id,u_id,style,label,default_value,required,placeholder,value_num,value_list,edit,des,create_time,updated_time',
                                         condition=condition)
            logger.debug("FN:DbFormMgr_get_field_template fieldTable_sql:{}".format(sql))
            fields_info = self.execute_fetch_all(conn, sql)
            dynamic_info = []
            region_field_info = {}
            for index, field_info in enumerate(fields_info):
                # # print("field_info['id']:", field_info['id'])
                if int(field_info['id']) == 1:
                    region_field_info = field_info
                    bool_mapping = {'1': True, '0': False}
                    region_field_info['required'] = bool_mapping[str(region_field_info['required'])]
                    region_field_info['options'] = json.loads(region_field_info['value_list'])
                    region_field_info['default'] = region_field_info['default_value']
                    del region_field_info['value_list'], region_field_info['default_value']
                    region_field_info['id'] = 's' + str(region_field_info['id'])
                    continue
                new_field_info = field_info
                # # print(new_field_info)
                new_field_info['options'] = json.loads(new_field_info['value_list'])
                new_field_info['default'] = new_field_info['default_value']
                del new_field_info['value_list'], new_field_info['default_value']
                # # print(new_field_info)
                new_field_info['id'] = 's' + str(new_field_info['id'])
                new_field_info['u_id'] = 'u' + str(new_field_info['u_id'])
                fields_info[index] = new_field_info

            if wp_id != 0:
                if style != 0:
                    condition = "style='%s' and form_id!='-1'" % (style)
                else:
                    condition = "1=1 and form_id!='-1'"
                sql = self.create_select_sql(db_name, 'dynamicFieldTable',
                                             'id,style,label,default_value,placeholder,value_num,des,create_time',
                                             condition=condition)
                logger.debug("FN:DbFormMgr_get_field_template dynamicFieldTable_sql:{}".format(sql))
                dynamic_fields_info = self.execute_fetch_all(conn, sql)
                for dynamic_field_info in dynamic_fields_info:
                    dynamic_field_id = dynamic_field_info['id']

                    # get dynamicFieldValue
                    # new_field_info = self.__get_dynamic_field_values(dynamic_field_info, dynamic_field_id, wp_id, db_name, conn)
                    if wp_id != 0:
                        condition = "workspace_id='%s' and dynamic_field_id='%s'" % (wp_id, dynamic_field_id)
                    else:
                        condition = "dynamic_field_id='%s'" % dynamic_field_id
                    sql = self.create_select_sql(db_name, 'dynamicFieldValueTable',
                                                 'option_label,create_time',
                                                 condition=condition)
                    values_info = self.execute_fetch_all(conn, sql)
                    new_field_info = dynamic_field_info
                    # # print('dynamic_field_info:', dynamic_field_info)
                    new_field_info['options'] = []
                    # # print('values_info:', values_info)
                    for value_info in values_info:
                        new_field_info['options'].append(
                            {'label': value_info['option_label'], 'value': value_info['option_label']})
                    new_field_info['default'] = new_field_info['default_value']
                    # del new_field_info['default_value']
                    # # # print(new_field_info)
                    # # exit(0)
                    new_field_info['id'] = 'd' + str(new_field_info['id'])
                    new_field_info['required'] = True
                    # # print(field_info)
                    dynamic_info.append(new_field_info)

            if wp_id != 0:
                condition = "ID='%s' " % (wp_id)
                sql = self.create_select_sql(db_name, 'workspaceTable', 'REGOINS', condition)
                logger.debug("FN:DbFormMgr_get_field_template workspaceTable_sql:{}".format(sql))
                options = []
                regions = json.loads(self.execute_fetch_one(conn, sql)['REGOINS'])
                # print('region_field_info:', region_field_info)
                # print('regions:', regions)

                for region in regions:
                    options.append({'label': region['region'], 'value': region['region']})
                    for sub_region in region['countryList']:
                        options.append({'label': sub_region['country'], 'value': sub_region['workflow']})
                region_field_info['options'] = options
                region_field_info['required'] = True
                region_field_info['value_num'] = len(options)
            fields_info = fields_info[1:]
            dynamic_info = [region_field_info] + dynamic_info
            # # # print(fields_info)
            if len(fields_info) == 0:
                return_info['default'] = []
            else:
                return_info['default'] = fields_info[0]
            return_info['templateTypeList'] = [{'title': 'system-defined', 'fieldlist': fields_info},
                                               {'title': 'dynamic-defined', 'fieldlist': dynamic_info}]
            data = response_code.SUCCESS
            data['data'] = return_info
            return data
        except Exception as e:
            logger.error("FN:get_field_template error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def add_new_system_field(self, wp_id, uc_id, field_data):
        conn = MysqlConn()
        try:

            data = response_code.SUCCESS
            return data
        except Exception as e:
            logger.error("FN:add_new_system_field error:{}".format(traceback.format_exc()))
            return response_code.ADD_DATA_FAIL
        finally:
            conn.close()

    # delete one form
    def delete_form(self, form):
        """
        Delete Form
        :return:
        """
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            # 解析参数成dict
            id = form['id']
            workspace_id = form.get('workspace_id', 0)
            usecase_id = form.get('usecase_id', 0)

            # 判断form是否已经存在
            data = self.get_details_form_by_id(id, workspace_id, usecase_id)
            workflow_data = workflow_mgr.get_all_base_workflow_by_form_id(id)
            # if have workflow, cannot be deleted
            if workflow_data['code'] == 200 and len(workflow_data['data']) > 0:
                data = response_code.DELETE_DATA_FAIL
                return data
            if data['code'] == 200:
                form_condition = "id='%s'" % id
                create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                update_time = create_time
                # update form status
                fields = ('available', 'hide', 'updated_time', 'des')
                values = (0, 1, update_time, 'deleted')
                sql = self.create_update_sql(db_name, 'formTable', fields, values, form_condition)
                logger.debug("FN:DbFormMgr_delete_form update_formTable_sql:{}".format(sql))
                return_count = self.updete_exec(conn, sql)
            else:
                data = response_code.DELETE_DATA_FAIL
                data['msg'] = 'disable form failed'
            return data

        except Exception as e:
            logger.error("FN:delete_form error:{}".format(traceback.format_exc()))
            conn.conn.rollback()
            return response_code.DELETE_DATA_FAIL
        finally:
            conn.close()

    # add new form
    def add_new_form(self, form, workspace_id=0):

        conn = MysqlConn()
        try:
            form_title = form['title']
            # workspace_id = form.get('workspace_id', 0)
            usecase_id = form.get('usecase_id', 0)
            hide = form.get('hide', 0)
            fields_num = len(form['fieldList'])
            u_max_id = 0
            u_max_num = 0
            for field in form['fieldList']:
                field_id = field['id']
                # get max u id
                tp_max_id = field.get('u_id', None)
                if not tp_max_id:
                    tp_max_id = field['id']
                if 'u' in tp_max_id:
                    # get max uid
                    if int(tp_max_id[1:]) > u_max_num:
                        u_max_num = int(tp_max_id[1:])
                        u_max_id = tp_max_id

            fields_list = json.dumps(form['fieldList'])
            creator_id = form.get('creator_id', '')
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_time = create_time
            des = form['des']

            db_name = configuration.get_database_name()

            # insert form
            fields = (
            'workspace_id', 'usecase_id', 'title', 'fields_num', 'u_max_id', 'creator_id', 'fields_list', 'hide', 'des',
            'create_time', 'updated_time')
            values = (
            workspace_id, usecase_id, form_title, fields_num, u_max_id, creator_id, fields_list, hide, des, create_time,
            update_time)
            sql = self.create_insert_sql(db_name, 'formTable', '({})'.format(', '.join(fields)), values)
            # print('form sql:', sql)
            logger.debug("FN:DbFormMgr_add_new_form insert_formTable_sql:{}".format(sql))
            form_id = self.insert_exec(conn, sql, return_insert_id=True)

            # update the copy s/d id into fields list
            copy_id_flag = False
            for index, field in enumerate(form['fieldList']):
                field_id = field['id']
                u_id = field.get('u_id', None)
                style = field['style']
                if 'u' not in field_id and u_id:
                    copy_id_flag = True
                    # link to the field
                    u_id_int = int(u_id[1:])
                    label = field.get('label', u_id)
                    field_fields = ('workspace_id', 'form_id', 'label', 'user_field_id', 'point_field_id', 'type', 'create_time')
                    values = (workspace_id, form_id, label, u_id_int, field_id, style, create_time)
                    sql = self.create_insert_sql(db_name, 'pointFieldTable', '({})'.format(', '.join(field_fields)),
                                                 values)
                    # print('dynamicFieldValueTable2 sql:', sql)
                    self.insert_exec(conn, sql, return_insert_id=True)
                    form['fieldList'][index]['id'] = u_id

            if copy_id_flag:
                fields_list = json.dumps(form['fieldList'])
                fields = ('fields_list', )
                values = ( fields_list, )
                form_condition = "id='%s'" % form_id
                sql = self.create_update_sql(db_name, 'formTable', fields, values, condition=form_condition)
                # print('form sql:', sql)
                logger.debug("FN:DbFormMgr_add_new_form insert_formTable_sql:{}".format(sql))
                _ = self.updete_exec(conn, sql)

            form['id'] = form_id
            data = response_code.SUCCESS
            data['data'] = form
            return data
        except Exception as e:
            logger.error("FN:add_new_form error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    # update form
    def update_form(self, form, account_id, workspace_id):
        def checking_field_in_workflow():
            pass

        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            form_id = form['id']
            # workspace_id = form.get('workspace_id', 0)
            usecase_id = form.get('usecase_id', 0)
            # 判断form是否已经存在
            select_form = self.get_details_form_by_id(form_id, workspace_id, usecase_id)
            if not select_form:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'cannot find the form.'

            # 1.create new form
            new_form_data = self.add_new_form(form, workspace_id)
            if new_form_data['code'] == 200:
                new_form_id = new_form_data['data']['id']

                # 2.update old form status
                form_condition = "id='%s'" % form_id
                create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                update_time = create_time
                # update form status
                fields = ('available', 'hide', 'updated_time', 'des')
                values = (0, 1, update_time, 'updated to new form id:{}'.format(str(new_form_id)))
                sql = self.create_update_sql(db_name, 'formTable', fields, values, form_condition)
                logger.debug("FN:DbFormMgr_update_form update_formTable_sql:{}".format(sql))
                return_count = self.updete_exec(conn, sql)

                # 3.disable all input form and workflow
                if return_count > 0:
                    # 3.1 make the workflow expired
                    column = ('available', 'form_id')
                    values = (0, new_form_id)
                    condition = 'form_id=%s' % form_id
                    sql = self.create_update_sql(db_name, 'workflowTable', column, values, condition)
                    logger.debug("FN:DbFormMgr_update_form update_workflowTable_sql:{}".format(sql))
                    _ = self.updete_exec(conn, sql)
                    # print('workflow sql:', sql)
                    condition = 'form_id=%s and workspace_id="%s"' % (form_id, workspace_id)
                    sql = self.create_select_sql(db_name, 'inputFormIndexTable', 'id', condition)
                    logger.debug("FN:DbFormMgr_update_form inputFormIndexTable_sql:{}".format(sql))
                    # 3.2disable all input form
                    input_form_infos = self.execute_fetch_all(conn, sql)
                    for input_form_info in input_form_infos:
                        input_form_id = input_form_info['id']
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        # update approval table
                        comment = 'the form structure was updated, please re-submit your request.'
                        fields = ('now_approval', 'is_approved', 'account_id', 'comment', 'updated_time')
                        values = (0, 0, account_id, comment, now)
                        approval_condition = "input_form_id='%s' and now_approval=1" % input_form_id
                        sql = self.create_update_sql(db_name, 'approvalTable', fields, values, approval_condition)
                        logger.debug("FN:DbFormMgr_update_form update_approvalTable_sql:{}".format(sql))
                        _ = self.updete_exec(conn, sql)
                        # update input form status
                        fields = ('form_status', 'updated_time')
                        values = (5, now)
                        update_condition = 'id=%s' % (input_form_id)
                        sql = self.create_update_sql(db_name, 'inputFormTable', fields, values, update_condition)
                        logger.debug("FN:DbFormMgr_update_form update_inputFormTable_sql:{}".format(sql))
                        _ = self.updete_exec(conn, sql)
                    data = response_code.SUCCESS
                    data['data'] = form
                else:
                    data = response_code.UPDATE_DATA_FAIL
                    data['msg'] = 'disable form failed'
            else:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'add new form failed'
            return data
        except Exception as e:
            logger.error("FN:update_form error:{}".format(traceback.format_exc()))
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def get_all_fields(self, workspace_id):

        system = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        dynamic = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        default = {
            1: {
                "style": 1,
                "label": "CheckBox",
                "default": "true,false",
                "options": [
                    {
                        "label": "true"
                    },
                    {
                        "label": "false"
                    }
                ],
                "des": "",
                "edit": 1,
                "placeholder": ""
            },
            2: {
                "style": 2,
                "label": "Dropdown",
                "default": "Option1",
                "options": [
                    {
                        "label": "Option1",
                        "value": "Option1"
                    },
                    {
                        "label": "Option2",
                        "value": "Option2"
                    }
                ],
                "des": "",
                "edit": 1,
                "required": True,
                "placeholder": ""
            },
            3: {
                "style": 3,
                "label": "Text",
                "default": "",
                "options": [],
                "des": "",
                "edit": 1,
                "maxLength": 25,
                "required": True,
                "placeholder": "",
                "rule": 0
            },
            4: {
                "style": 4,
                "label": "Upload",
                "placeholder": "",
                "default": "",
                "multiple": False,
                "options": [],
                "des": "",
                "edit": 1
            },
            5: {
                "style": 5,
                "label": "Switch",
                "default": True,
                "placeholder": "",
                "options": [],
                "des": "",
                "edit": 1
            },
            6: {
                "style": 6,
                "label": "DatePicker",
                "placeholder": "",
                "default": "",
                "options": [],
                "des": "",
                "required": True,
                "edit": 1
            }
        }
        templateTypeList = form_mgr.get_field_template(0, workspace_id)
        logger.debug("FN:DbFormMgr_get_all_fields templateTypeList:{}".format(templateTypeList['data']['templateTypeList']))
        for index, field_info in enumerate(templateTypeList['data']['templateTypeList'][0]['fieldlist']):
            if field_info:
                field_style = int(field_info['style'])
                if field_style not in system:
                    system[field_style] = []
                system[field_style].append(field_info)
        for index, field_info in enumerate(templateTypeList['data']['templateTypeList'][-1]['fieldlist']):
            if field_info:
                field_style = int(field_info['style'])
                if field_style not in dynamic:
                    dynamic[field_style] = []
                dynamic[field_style].append(field_info)
        data = response_code.SUCCESS
        data['data'] = {'system': system, 'dynamic': dynamic, 'default': default}
        return data

    # disable
    def add_point_field(self, field_info, field_type, workspace_id):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()
            field_id = field_info['id']
            field_label = field_info['label']
            style = field_info['style']
            type = field_type # system or dynamic
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # add a new dynamic field
            field_fields = ('style', 'form_id', 'label', 'default_value', 'placeholder',
                            'value_num', 'create_time')
            values = (style, '-1', field_label, '', '', 1, create_time)
            sql = self.create_insert_sql(db_name, 'dynamicFieldTable', '({})'.format(', '.join(field_fields)), values)
            # print('dynamicFieldTable2 sql:', sql)
            dynamic_field_id = self.insert_exec(conn, sql, return_insert_id=True)

            # link to the field

            field_fields = ('workspace_id', 'dynamic_field_id', 'point_field_id', 'type', 'create_time')
            values = (workspace_id, dynamic_field_id, field_id, type, create_time)
            sql = self.create_insert_sql(db_name, 'pointFieldTable', '({})'.format(', '.join(field_fields)),
                                         values)
            # print('dynamicFieldValueTable2 sql:', sql)
            self.insert_exec(conn, sql, return_insert_id=True)
            field_info['id'] = 'd'+ str(dynamic_field_id)

            data = response_code.SUCCESS
            data['data'] = field_info
            return data
        except Exception as e:
            logger.error("FN:update_form error:{}".format(traceback.format_exc()))
            # print(traceback.format_exc())
            return response_code.GET_DATA_FAIL
        finally:
            conn.close()

    def __get_dynamic_field_values(self, field_info, pass_dynamic_field_id, wp_id, db_name, conn):

        dynamic_field_id = pass_dynamic_field_id
        dynamic_field_id = str(dynamic_field_id).replace('d', '')
        # # check if it is point field
        # if wp_id != 0:
        #     condition = "workspace_id='%s' and dynamic_field_id='%s'" % (wp_id, dynamic_field_id)
        # else:
        #     condition = "dynamic_field_id='%s'" % dynamic_field_id
        # sql = self.create_select_sql(db_name, 'pointFieldTable',
        #                              'point_field_id,type', condition=condition)
        # logger.debug("FN:__get_dynamic_field_values pointFieldTable sql:{}".format(sql))
        #
        # point_field_info = self.execute_fetch_one(conn, sql)
        # if point_field_info and point_field_info['type'] == 'dynamic':
        #     dynamic_field_id = str(point_field_info['point_field_id']).replace('d', '')
        #     point_field_info = None

        # it is a dynamic field, get values from dynamicFieldValueTable
        # if not point_field_info:
        # get value from dynamic value table
        if wp_id != 0:
            condition = "workspace_id='%s' and dynamic_field_id='%s'" % (wp_id, dynamic_field_id)
        else:
            condition = "dynamic_field_id='%s'" % dynamic_field_id
        sql = self.create_select_sql(db_name, 'dynamicFieldValueTable',
                                     'option_label,create_time', condition=condition)
        logger.debug("FN:__get_dynamic_field_values dynamicFieldValueTable sql:{}".format(sql))
        values_info = self.execute_fetch_all(conn, sql)
        field_info['options'] = []
        # print('field_info:', field_info)
        for value_info in values_info:
            field_info['options'].append(
                {'label': value_info['option_label'], 'value': value_info['option_label']})
        field_info['default'] = field_info['default_value']
        del field_info['default_value']
        # elif point_field_info['type'] == 'system':
        #     system_field_id = str(point_field_info['point_field_id']).replace('s', '')
        #     if wp_id != 0:
        #         condition = "workspace_id='%s' and id='%s'" % (wp_id, system_field_id)
        #     else:
        #         condition = "id='%s'" % system_field_id
        #
        #     sql = self.create_select_sql(db_name, 'fieldTable',
        #                                  'id,style,label,default_value,required,placeholder,value_num,value_list,edit,des,create_time,updated_time',
        #                                  condition=condition)
        #     logger.debug("FN:__get_dynamic_field_values fieldTable sql:{}".format(sql))
        #     new_field_info = self.execute_fetch_one(conn, sql)
        #     if new_field_info:
        #
        #         if wp_id != 0 and int(system_field_id) == 1:
        #             condition = "ID='%s' " % (wp_id)
        #             sql = self.create_select_sql(db_name, 'workspaceTable', 'REGOINS', condition)
        #             logger.debug("FN:__get_dynamic_field_values workspaceTable REGOINS sql:{}".format(sql))
        #             options = []
        #             regions = json.loads(self.execute_fetch_one(conn, sql)['REGOINS'])
        #             # print('region_field_info:', region_field_info)
        #             # print('regions:', regions)
        #
        #             for region in regions:
        #                 options.append({'label': region['region'], 'value': region['region']})
        #                 for sub_region in region['countryList']:
        #                     options.append({'label': sub_region['country'], 'value': sub_region['workflow']})
        #             new_field_info['value_list'] = options
        #             new_field_info['required'] = True
        #             new_field_info['value_num'] = len(options)
        #         # print('new_field_info:', new_field_info)
        #         if 'options' in field_info:
        #             del field_info['options']
        #         if 'default' in field_info:
        #             del field_info['default']
        #         if 'label' in field_info:
        #             del new_field_info['label']
        #         if 'id' in field_info:
        #             del new_field_info['id']
        #         new_field_info['options'] = new_field_info['value_list']
        #         new_field_info['default'] = new_field_info['default_value']
        #         del new_field_info['value_list'], new_field_info['default_value']
        #         field_info.update(new_field_info)

        return field_info

    def __get_user_field_values(self, field_info, pass_user_field_id, wp_id, db_name, conn):

        user_field_id = pass_user_field_id
        user_field_id = str(user_field_id).replace('u', '')
        # check if it is point field
        if wp_id != 0:
            condition = "workspace_id='%s' and user_field_id='%s'" % (wp_id, user_field_id)
        else:
            condition = "user_field_id='%s'" % user_field_id
        sql = self.create_select_sql(db_name, 'pointFieldTable',
                                     'point_field_id,type,label', condition=condition)
        logger.debug("FN:__get_dynamic_field_values pointFieldTable sql:{}".format(sql))

        point_field_info = self.execute_fetch_one(conn, sql)
        if not point_field_info:
            return field_info
        field_info['label'] = point_field_info['label']
        # it is a dynamic field, get values from dynamicFieldValueTable
        if point_field_info['type'] == 'dynamic':
            point_field_id = str(point_field_info['point_field_id']).replace('d', '')
            # get value from dynamic value table
            if wp_id != 0:
                condition = "workspace_id='%s' and dynamic_field_id='%s'" % (wp_id, point_field_id)
            else:
                condition = "dynamic_field_id='%s'" % point_field_id
            sql = self.create_select_sql(db_name, 'dynamicFieldValueTable',
                                         'option_label,create_time', condition=condition)
            logger.debug("FN:__get_dynamic_field_values dynamicFieldValueTable sql:{}".format(sql))
            values_info = self.execute_fetch_all(conn, sql)
            field_info['options'] = []
            # print('field_info:', field_info)
            for value_info in values_info:
                field_info['options'].append(
                    {'label': value_info['option_label'], 'value': value_info['option_label']})
            if 'default_value' in field_info:
                field_info['default'] = field_info['default_value']
                del field_info['default_value']
        elif point_field_info['type'] == 'system':
            system_field_id = str(point_field_info['point_field_id']).replace('s', '')
            if wp_id != 0:
                condition = "workspace_id='%s' and id='%s'" % (wp_id, system_field_id)
            else:
                condition = "id='%s'" % system_field_id

            sql = self.create_select_sql(db_name, 'fieldTable',
                                         'id,style,label,default_value,required,placeholder,value_num,value_list,edit,des,create_time,updated_time',
                                         condition=condition)
            logger.debug("FN:__get_dynamic_field_values fieldTable sql:{}".format(sql))
            new_field_info = self.execute_fetch_one(conn, sql)
            if new_field_info:

                if wp_id != 0 and int(system_field_id) == 1:
                    condition = "ID='%s' " % (wp_id)
                    sql = self.create_select_sql(db_name, 'workspaceTable', 'REGOINS', condition)
                    logger.debug("FN:__get_dynamic_field_values workspaceTable REGOINS sql:{}".format(sql))
                    options = []
                    regions = json.loads(self.execute_fetch_one(conn, sql)['REGOINS'])
                    # print('region_field_info:', region_field_info)
                    # print('regions:', regions)

                    for region in regions:
                        options.append({'label': region['region'], 'value': region['region']})
                        for sub_region in region['countryList']:
                            options.append({'label': sub_region['country'], 'value': sub_region['workflow']})
                    new_field_info['value_list'] = options
                    new_field_info['required'] = True
                    new_field_info['value_num'] = len(options)
                # print('new_field_info:', new_field_info)
                if 'options' in field_info:
                    del field_info['options']
                if 'default' in field_info:
                    del field_info['default']
                if 'label' in field_info:
                    del new_field_info['label']
                if 'id' in field_info:
                    del new_field_info['id']
                new_field_info['options'] = new_field_info['value_list']
                new_field_info['default'] = new_field_info['default_value']
                del new_field_info['value_list'], new_field_info['default_value']
                field_info.update(new_field_info)

        return field_info


form_mgr = DbFormMgr()
