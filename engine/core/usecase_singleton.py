#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.usecase.db_usecase_mgr import usecase_mgr

__all__ = {"usecaseSingleton"}


class usecaseSingleton():

    def add_new_usecase_setting(self, usecase):
        """

        :return:
        """
        return usecase_mgr.add_new_usecase_setting(usecase)

    def get_usecase_info_by_ad_group(self, account_id):
        return usecase_mgr.get_usecase_info_by_ad_group(account_id)

    def update_usecase(self, usecase):
        return usecase_mgr.update_usecase_info(usecase)

    def get_usecase_details_info_by_id(self, id):

        return usecase_mgr.get_usecase_details_info_by_id(id)
usecaseSingleton_singleton = usecaseSingleton()


