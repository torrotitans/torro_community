#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.workflow.db_workflow_mgr import workflow_mgr

__all__ = {"workflowSingleton"}


class workflowSingleton():

    def get_all_base_workflow(self, form_id):
        return workflow_mgr.get_all_base_workflow_by_form_id(form_id)

    def get_all_base_workflow_v2(self, workspace_id):
        return workflow_mgr.get_all_base_workflow(workspace_id)

    def get_details_workflow(self, workflow_id):
        return workflow_mgr.get_detail_workflow_by_workflow_id(workflow_id)

    def get_all_stages(self):
        """
        获取所有的stages信息
        :return:
        """
        return workflow_mgr.get_all_stages()

    def get_all_stages_v2(self, workflow_id):

        return workflow_mgr.get_all_stages_v2(workflow_id)
    def delete_workflow(self, workflow):
        """

        :return:
        """
        return workflow_mgr.delete_workflow(workflow)

    def add_new_workflow(self, workflow):
        """

        :return:
        """
        return workflow_mgr.add_new_workflow(workflow)

    def update_workflow(self, workflow):
        """

        :return:
        """
        return workflow_mgr.update_workflow(workflow)

    # def get_stages_by_(self, value):
    #     """
    #     获取所有的fields信息
    #     :return:
    #     """
    #     return workflow_mgr.get_stages_with_condition(value)

workflowSingleton_singleton = workflowSingleton()


