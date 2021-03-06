import abc
from db.base import DbBase
from common.common_request_process import req
from common.common_response_code import response_code
from db.connection_pool import MysqlConn
from utils.status_code import response_code
from config import configuration
import logging
import traceback
import datetime
from functools import wraps

logger = logging.getLogger("main." + __name__)


class baseTask(DbBase, metaclass=abc.ABCMeta):

    api_type = 'system'
    api_name = 'baseTask'

    arguments = {}
    role_list = []
    target_project = None
    full_resource_name = None
    def __init__(self, stage_dict):
        self.stage_dict = stage_dict

    def verify_all_param(self):
        self.stage_dict = req.verify_all_param(self.stage_dict, self.arguments)


    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass

    # @abc.abstractmethod
    def message_tranfer(self, log):
        data = response_code.SUCCESS
        comment = data['msg']
        if isinstance(log, dict):
            if 'data' in log and isinstance(log['data'], str):
                comment = log['data']
            else:
                comment = log['msg']
        elif isinstance(log, str):
            comment = log
        comment = comment.replace('\'', '\"')
        return comment

    def records_resource(self, workspace_id, input_form_id, usecase_name, resource_label, resource_name):
        conn = MysqlConn()
        try:
            db_name = configuration.get_database_name()

            cond = "WORKSPACE_ID='%s' and USECASE_NAME='%s'" % (
                workspace_id, usecase_name)
            sql = self.create_select_sql(db_name, 'usecaseTable', 'ID', cond)
            usecase_info = self.execute_fetch_one(conn, sql)
            # print('1111111111111111111111 usecase_info sql:', sql)
            # print('1111111111111111111111 usecase_info:', usecase_info)
            if not usecase_info:
                usecase_id = -1
            else:
                usecase_id = usecase_info['ID']

            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fields = (
                'workspace_id', 'usecase_id', 'input_form_id', 'resource_label', 'resource_name', 'create_time', 'des')
            values = (
                workspace_id, usecase_id, input_form_id, resource_label, resource_name, create_time, '')
            sql = self.create_insert_sql(db_name, 'gcpResourceTable', '({})'.format(', '.join(fields)), values)
            _ = self.insert_exec(conn, sql)

        except Exception as e:
            logger.error("FN:records_resource error:{}".format(traceback.format_exc()))
            # return response_code.ADD_DATA_FAIL
        finally:
            conn.close()