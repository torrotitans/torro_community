#!/usr/bin/python
# -*- coding: UTF-8 -*


from db.form.db_form_mgr import form_mgr

__all__ = {"formSingleton"}


class formSingleton():

    def get_all_base_form(self, wp_id=0, uc_id=0, system=0):

        return form_mgr.get_all_base_form(wp_id, uc_id, system)

    def get_field_template(self, style=0, wp_id=0):

        return form_mgr.get_field_template(style, wp_id)

    def add_new_system_field(self, wp_id, uc_id, field_data):

        return form_mgr.add_new_system_field(wp_id, uc_id, field_data)


    def get_base_form_by_id(self, id):

        return form_mgr.get_base_form_by_id(id)

    def get_details_form_by_id(self, id, wp_id=0, uc_id=0):

        return form_mgr.get_details_form_by_id(id, wp_id, uc_id)


    def delete_form(self, form):

        return form_mgr.delete_form(form)

    def add_new_form(self, form, workspace_id=0):

        return form_mgr.add_new_form(form, workspace_id)

    def update_form(self, form, account_id, workspace_id=0):

        return form_mgr.update_form(form, account_id, workspace_id)

    def get_all_fields(self, workspace_id):

        return form_mgr.get_all_fields(workspace_id)


    def add_point_field(self, field_info, field_type, input_form_id, workspace_id):
        return  form_mgr.add_point_field(field_info, field_type, input_form_id, workspace_id)
formSingleton_singleton = formSingleton()


