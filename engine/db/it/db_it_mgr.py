#!/usr/bin/python
# -*- coding: UTF-8 -*

from config import configuration
from db.base import DbBase
from db.connection_pool import MysqlConn
from utils.status_code import response_code
import traceback
from common.common_input_form_status import status as Status
import logging

from db.workflow.db_stages_parameter import stageBase

logger = logging.getLogger("main." + __name__)

class DbITMgr(DbBase):

    status = Status.code
    status_history_mapping = Status.status_history_mapping

    def get_cmd_sql(self, sql):

        conn = MysqlConn()
        db_name = configuration.get_database_name()
        try:
            cmd = self.create_cmd_sql(conn, db_name, sql)
            return cmd
        except Exception as e:
            logger.error("FN:sql_execute error:{}".format(traceback.format_exc()))
            return ''
        finally:
            conn.close()

it_mgr = DbITMgr()
