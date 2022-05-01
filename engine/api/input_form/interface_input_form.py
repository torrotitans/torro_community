#!/usr/bin/python
# -*- coding: UTF-8 -*
from common.common_input_form_status import status as Status
from utils.smtp_helper import notify_approvers
from core.governance_singleton import governance_singleton
from flask import request
from flask_restful import Resource
from core.input_form_singleton import input_form_singleton
from core.form_singleton import formSingleton_singleton
from core.org_singleton import orgSingleton_singleton
import os
from utils.status_code import response_code
from common.common_model_enum import modelEnum
from common.common_response_process import response_result_process
from common.common_login_helper import login_required
from common.common_request_process import req
from db.input_form.db_input_form_parameter import inputFormApiPara
import time
from db.gcp.task_operator import taskOperator
import traceback
import logging

logger = logging.getLogger("main." + __name__)

class interfaceInputForm(Resource):
    # @api_version
    @login_required
    def post(self,):
        xml = request.args.get('format')
        request_data = req.request_process(request, xml, modelEnum.department.value)
        # # print('request: ', request_data)

        if isinstance(request_data, bool):
            request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
            return response_result_process(request_data, xml=xml)

        request_data = req.verify_all_param(request_data, inputFormApiPara.input_form_data_POST_request)
        workspace_id = req.get_workspace_id()

        try:
            user_key = req.get_user_key()
            account_id = req.get_user_account_id()
            # print('user id:', user_key)
        except:
            data = response_code.GET_DATA_FAIL
            data['msg'] = 'Token error or expired, please login again.'
            logger.error("FN:interfaceInputForm_post data_error:{}".format(data))
            logger.error("FN:interfaceInputForm_post error:{}".format(traceback.format_exc()))
            return response_result_process(data, xml=xml)

        try:
            form_id = request_data['form_id']
            form_data = formSingleton_singleton.get_details_form_by_id(form_id)
            field_ids = {}
            if form_data['code'] == 200:
                for field in form_data["data"]["fieldList"]:
                    field_id = field['id']
                    field_style = field['style']
                    field_ids[field_id] = field_style

            file_list = request.files.items()
            # # print('request_data: ', request_data)
            # # print('request.form:', request.form)
            # # print('request.files: ', request.files)

            print('file_list: ', file_list)
            for file in file_list:
                file_id = file[0][:2]
                # print("file_id:", file_id)
                if file_id not in request_data['form_field_values_dict']:
                    request_data['form_field_values_dict'][file_id] = []
                file_contents = file[1]
                # print('file_contents: ', type(file_contents), file_contents)

                if not isinstance(file_contents, list):
                    file_contents = [file_contents]
                for file in file_contents:
                    t = int(time.time())
                    upload_path = './data/input_form_file/%s/%s-%s-%s/' % (user_key, form_id, file_id, t)
                    if not os.path.exists(upload_path):
                        os.makedirs(upload_path)
                    upload_path += file.filename
                    file.save(upload_path)
                    print('file_contents: ', type(file_contents), file_contents)
                    request_data['form_field_values_dict'][file_id].append(upload_path)
            request_data['field_ids'] = field_ids
            # print('request_data: ', request_data)
            # exit(0)
            data = input_form_singleton.input_form_data(user_key, request_data, workspace_id)
            # return data
            if data['code'] == 200:
                response_data = data['data']
                input_form_id = data['data']['id']
                text = ''
                if 'msg' in data:
                    text = data['msg']
                if len(data['data']['approvers']) == 0:
                    approval_data = {'form_status': Status.approved,
                                     'id': input_form_id,
                                     'comment': ''}
                    data = governance_singleton.change_status(user_key, account_id, workspace_id, approval_data, no_approval=True)
                    # print('change status data: ', data)
                    logger.info("FN:interfaceGovernance_post change_status_data:{}".format(data))
                    # if begin to execute task
                    data1 = response_code.BAD_REQUEST
                    # system form operations
                    # if data['code'] == 200 and form_id == 2 and data['msg'] == 'request successfully':
                    #     data1 = governance_singleton.add_new_usecase(input_form_id, form_id, user_key, workspace_id)
                    # if data['code'] == 200 and form_id == 3 and data['msg'] == 'request successfully':
                    #     data1 = governance_singleton.add_new_policy_tags(input_form_id, form_id, user_key, workspace_id)
                    # trigger gcp task
                    if data['code'] == 200 and 'data' in data and 'is_approved' in data['data'] and data['data'][
                        'is_approved'] == 1:
                        # if data['code'] == 200 and 'data' in data and data['data']['is_approved'] == 1 and data['data']['tasks']\
                        #     and data['data']['gcp_tasks']:
                        gcp_tasks = data['data'].get('gcp_tasks', [])
                        tasks = data['data'].get('tasks', [])
                        return_msg_list = taskOperator.execute_tasks(gcp_tasks, workspace_id, form_id, input_form_id,
                                                                     user_key)
                        data1 = governance_singleton.updateTask(user_key, account_id, input_form_id, workspace_id,
                                                                tasks, return_msg_list)
                    if 'data' in data and 'notice_ids' in data['data'] and data['code'] == 200:
                        logger.debug("FN:interfaceGovernance_post res_data:{}".format(data))
                        notice_ids = data['data']['notice_ids']
                        text = ''
                        if 'msg' in data:
                            text = data['msg']
                        data2 = notify_approvers(input_form_id, notice_ids, text=text)
                        data3 = orgSingleton_singleton.insert_notification(notice_ids + [account_id], input_form_id,
                                                                           data['data']['history_id'], text)
                        if data2 and data2['code'] == 200:
                            # data['data'] = req.verify_all_param(data['data'], governanceApiPara.changeStatus_POST_response)
                            data = response_code.SUCCESS
                        else:
                            data = response_code.UPDATE_DATA_FAIL
                            data['msg'] = 'Create new form success, fail to send email to approves'

                else:
                    data2 = notify_approvers(data['data']['id'], data['data']['approvers'])
                    data3 = orgSingleton_singleton.insert_notification(data['data']['approvers']+[account_id], data['data']['id'], data['data']['history_id'], text)
                    if data2 and data2['code'] == 200:
                        data['data'] = req.verify_all_param(response_data, inputFormApiPara.input_form_data_POST_response)
                    else:

                        data = response_code.UPDATE_DATA_FAIL
                        data['msg'] = 'Create new form success, fail to send email to approves'
                        logger.error("FN:interfaceInputForm_post data_error:{}".format(data))
            else:
                data = response_code.UPDATE_DATA_FAIL
                data['msg'] = 'Create new form success, fail to send email to approves'
                logger.error("FN:interfaceInputForm_post data_error:{}".format(data))

        except:
            data = response_code.GET_DATA_FAIL
            data['msg'] = 'Something went wrong. Please double check your input.'
            logger.error("FN:interfaceInputForm_post data_error:{}".format(data))
            logger.error("FN:interfaceInputForm_post error:{}".format(traceback.format_exc()))

        logger.debug("FN:interfaceInputForm_post data:{}".format(data))
        return response_result_process(data, xml=xml)

    @login_required
    def put(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)


            request_data = req.verify_all_param(request_data, inputFormApiPara.input_form_data_PUT_request)
            workspace_id = req.get_workspace_id()
            try:
                user_key = req.get_user_key()
                account_id = req.get_user_account_id()
                # print('user id:', user_key)
            except:
                data = response_code.GET_DATA_FAIL
                # print(traceback.format_exc())
                data['msg'] = 'Token error or expired, please login again.'
                return response_result_process(data, xml=xml)
            try:
                form_id = request_data['form_id']
                form_data = formSingleton_singleton.get_details_form_by_id(form_id)
                field_ids = {}
                if form_data['code'] == 200:
                    for field in form_data["data"]["fieldList"]:
                        field_id = field['id']
                        field_style = field['style']
                        field_ids[field_id] = field_style

                file_list = request.files.items()


                # # print('file_list: ', file_list)
                for file in file_list:
                    file_id = file[0][:2]
                    # print("file_id:", file_id)
                    if file_id not in request_data['form_field_values_dict']:
                        request_data['form_field_values_dict'][file_id] = []
                    file_contents = file[1]
                    # print('file_contents: ', type(file_contents), file_contents)

                    if not isinstance(file_contents, list):
                        file_contents = [file_contents]
                    for file in file_contents:
                        t = int(time.time())
                        upload_path = './data/input_form_file/%s/%s-%s-%s/' % (user_key, form_id, file_id, t)
                        if not os.path.exists(upload_path):
                            os.makedirs(upload_path)
                        upload_path += file.filename
                        file.save(upload_path)
                        print('file_contents: ', type(file_contents), file_contents)
                        request_data['form_field_values_dict'][file_id].append(upload_path)
                request_data['field_ids'] = field_ids
                # print('request_data: ', request_data)
                data = input_form_singleton.update_form_data(user_key, request_data, workspace_id)
                # return data
                if data['code'] == 200:
                    response_data = data['data']
                    input_form_id = data['data']['id']

                    text = ''
                    if 'msg' in data:
                        text = data['msg']
                    if len(data['data']['approvers']) == 0:
                        approval_data = {'form_status': Status.approved,
                                         'id': input_form_id,
                                         'comment': ''}
                        data = governance_singleton.change_status(user_key, account_id, workspace_id, approval_data)
                        # print('change status data: ', data)
                        logger.info("FN:interfaceGovernance_post change_status_data:{}".format(data))
                        # if begin to execute task
                        data1 = response_code.BAD_REQUEST
                        # system form operations
                        # if data['code'] == 200 and form_id == 2 and data['msg'] == 'request successfully':
                        #     data1 = governance_singleton.add_new_usecase(input_form_id, form_id, user_key, workspace_id)
                        # if data['code'] == 200 and form_id == 3 and data['msg'] == 'request successfully':
                        #     data1 = governance_singleton.add_new_policy_tags(input_form_id, form_id, user_key, workspace_id)
                        # trigger gcp task
                        if data['code'] == 200 and 'data' in data and 'is_approved' in data['data'] and data['data'][
                            'is_approved'] == 1:
                            # if data['code'] == 200 and 'data' in data and data['data']['is_approved'] == 1 and data['data']['tasks']\
                            #     and data['data']['gcp_tasks']:
                            gcp_tasks = data['data'].get('gcp_tasks', [])
                            tasks = data['data'].get('tasks', [])
                            return_msg_list = taskOperator.execute_tasks(gcp_tasks, workspace_id, form_id,
                                                                         input_form_id,
                                                                         user_key)
                            data1 = governance_singleton.updateTask(user_key, account_id, input_form_id, workspace_id,
                                                                    tasks, return_msg_list)
                        if 'data' in data and 'notice_ids' in data['data'] and data['code'] == 200:
                            logger.debug("FN:interfaceGovernance_post res_data:{}".format(data))
                            notice_ids = data['data']['notice_ids']
                            text = ''
                            if 'msg' in data:
                                text = data['msg']
                            data2 = notify_approvers(input_form_id, notice_ids, text=text)
                            data3 = orgSingleton_singleton.insert_notification(notice_ids + [account_id], input_form_id,
                                                                               data['data']['history_id'], text)
                            if data2 and data2['code'] == 200:
                                # data['data'] = req.verify_all_param(data['data'], governanceApiPara.changeStatus_POST_response)
                                data = response_code.SUCCESS
                            else:
                                data = response_code.UPDATE_DATA_FAIL
                                data['msg'] = 'Create new form success, fail to send email to approves'
                    else:
                        data2 = notify_approvers(data['data']['id'], data['data']['approvers'])
                        data3 = orgSingleton_singleton.insert_notification(data['data']['approvers'] + [account_id],
                                                                           data['data']['id'], data['data']['history_id'],
                                                                           text)


                        if data2 and data2['code'] == 200:
                            data['data'] = req.verify_all_param(response_data, inputFormApiPara.input_form_data_POST_response)
                        else:
                            data = response_code.UPDATE_DATA_FAIL
                            data['msg'] = 'Create new form success, fail to send email to approves'
            except:
                data = response_code.GET_DATA_FAIL
                logger.error("FN:interfaceInputForm_put data_error:{}".format(data))
                logger.error("FN:interfaceInputForm_put error:{}".format(traceback.format_exc()))

            logger.error("FN:interfaceInputForm_put data:{}".format(data))
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceInputForm_put error:{}".format(traceback.format_exc()))
            error_data = response_code.GET_DATA_FAIL
            return response_result_process(error_data, xml=xml)

    # delete the workspace info
    @login_required
    def delete(self,):
        xml = request.args.get('format')
        try:
            request_data = req.request_process(request, xml, modelEnum.department.value)
            # # print('request_data:', request_data)
            if isinstance(request_data, bool):
                request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
                return response_result_process(request_data, xml=xml)

            request_data = req.verify_all_param(request_data, inputFormApiPara.deleteForm_POST_request)
            try:
                user_key = req.get_user_key()
                # print('user id:', user_key)
            except:
                data = response_code.GET_DATA_FAIL
                # print(traceback.format_exc())
                data['msg'] = 'Token error or expired, please login again.'
                return response_result_process(data, xml=xml)
            data = input_form_singleton.delete_form_data(user_key, request_data)
            if data['code'] == 200:
                response_data = data['data']
                data['data'] = req.verify_all_param(response_data, inputFormApiPara.deleteForm_POST_response)
            # # print(data)
            return response_result_process(data, xml=xml)

        except Exception as e:
            logger.error("FN:interfaceInputForm_delete error:{}".format(traceback.format_exc()))
            error_data = response_code.ADD_DATA_FAIL
            return response_result_process(error_data, xml=xml)


class interfaceInputFormList(Resource):
    # @api_version
    @login_required
    def post(self,):
        xml = request.args.get('format')
        request_data = req.request_process(request, xml, modelEnum.department.value)
        # # print('request: ', request_data)

        if isinstance(request_data, bool):
            request_data = response_code.REQUEST_PARAM_FORMAT_ERROR
            return response_result_process(request_data, xml=xml)

        workspace_id = req.get_workspace_id()
        try:
            user_key = req.get_user_key()
            account_id = req.get_user_account_id()
            # print('user id:', user_key)
        except:
            data = response_code.GET_DATA_FAIL
            # print(traceback.format_exc())
            data['msg'] = 'Token error or expired, please login again.'
            return response_result_process(data, xml=xml)
        try:
            data_list = request_data.get('data', [])
            output_data = response_code.SUCCESS
            output_data['data'] = []
            for one_data in data_list:
                one_data = req.verify_all_param(one_data, inputFormApiPara.input_form_data_POST_request)
                form_id = one_data['form_id']
                form_data = formSingleton_singleton.get_details_form_by_id(form_id)
                field_ids = {}
                if form_data['code'] == 200:
                    for field in form_data["data"]["fieldList"]:
                        field_id = field['id']
                        field_style = field['style']
                        field_ids[field_id] = field_style

                file_list = request.files.items()
                # # print('request_data: ', request_data)
                # # print('request.form:', request.form)
                # # print('request.files: ', request.files)

                print('file_list: ', file_list)
                for file in file_list:
                    file_id = file[0][:2]
                    # print("file_id:", file_id)
                    if file_id not in one_data['form_field_values_dict']:
                        one_data['form_field_values_dict'][file_id] = []
                    file_contents = file[1]
                    # print('file_contents: ', type(file_contents), file_contents)

                    if not isinstance(file_contents, list):
                        file_contents = [file_contents]
                    for file in file_contents:
                        t = int(time.time())
                        upload_path = './data/input_form_file/%s/%s-%s-%s/' % (user_key, form_id, file_id, t)
                        if not os.path.exists(upload_path):
                            os.makedirs(upload_path)
                        upload_path += file.filename
                        file.save(upload_path)
                        print('file_contents: ', type(file_contents), file_contents)
                        one_data['form_field_values_dict'][file_id].append(upload_path)
                one_data['field_ids'] = field_ids

                data = input_form_singleton.input_form_data(user_key, one_data, workspace_id)

                # return data
                if data['code'] == 200:
                    response_data = data['data']
                    text = ''
                    if 'msg' in data:
                        text = data['msg']
                    data2 = notify_approvers(data['data']['id'], data['data']['approvers'])
                    data3 = orgSingleton_singleton.insert_notification(data['data']['approvers'] + [account_id],
                                                                       data['data']['id'], data['data']['history_id'],
                                                                       text)

                    if data2 and data2['code'] == 200:
                        data['data'] = req.verify_all_param(response_data,
                                                            inputFormApiPara.input_form_data_POST_response)
                    else:
                        data = response_code.UPDATE_DATA_FAIL
                        data['msg'] = 'Create new form success, fail to send email to approves'

                output_data['data'].append(data)

            return output_data

        except:
            data = response_code.ADD_DATA_FAIL
            data['msg'] = 'Something went wrong. Please double check your input.'
            logger.error("FN:interfaceInputFormList_post data_error:{}".format(data))
            logger.error("FN:interfaceInputFormList_post error:{}".format(traceback.format_exc()))

            return response_result_process(data, xml=xml)
