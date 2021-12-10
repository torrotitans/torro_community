#!/usr/bin/python
# -*- coding: UTF-8 -*

from db.org.db_org_mgr import org_mgr
from db.input_form.db_input_form_mgr import input_form_mgr
from utils.smtp_helper import Smtp
__all__ = {"inputFormSingleton"}


class inputFormSingleton():

    def input_form_data(self, user_key, inputData, workspace_id=None):
        """
        :return:
        """
        return input_form_mgr.input_form_data(user_key, inputData, workspace_id)

    def update_form_data(self, user_key, inputData, workspace_id=None):
        """
        :return:
        """
        return input_form_mgr.update_form_data(user_key, inputData, workspace_id)

    def delete_form_data(self, user_key, inputData):
        """
        :return:
        """
        return input_form_mgr.deleteDataBranch(user_key, inputData)


    def get_input_form_data(self, user_id, input_form_id):

        return input_form_mgr.get_input_form_data(user_id, input_form_id)


input_form_singleton = inputFormSingleton()
