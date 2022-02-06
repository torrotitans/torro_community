#!/usr/bin/python
# -*- coding: UTF-8 -*

from db.gcp.db_gcp_mgr import db_gcp_mgr
__all__ = {"gcpSingleton"}


class gcpSingleton():

    def get_gcp_tasks(self, form_id, input_form_id):

        return db_gcp_mgr.get_gpc_tasks(form_id, input_form_id)

    def get_table_schema(self, request_data, user_key, workspace_id):

        return db_gcp_mgr.get_table_schema(request_data, user_key, workspace_id)

    def list_table(self, request_data, user_key, workspace_id):

        return db_gcp_mgr.list_table(request_data, user_key, workspace_id)

gcpSingleton_singleton = gcpSingleton()


