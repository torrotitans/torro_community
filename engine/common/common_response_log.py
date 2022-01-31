#!/usr/bin/python
# -*- coding: UTF-8 -*

class ResponseLog:


    @staticmethod
    def null_value(param):
        """
        :param param:
        :return:
        """
        return "param '%s' is null ." % (param)

    @staticmethod
    def wrong_value(param, value):
        """
        :param param:
        :param value:
        :return:
        """
        return "param '%s' improper value %s." % (param, value)

    @staticmethod
    def record_exist(unique_key, value):
        """
        :param unique_key:
        :param value:
        :return:
        """
        return "unique key '(%s,%s)' is exist." % (unique_key, value)

    @staticmethod
    def delete_record_in_use(code, value):
        """
        :param code:
        :param value:
        :return:
        """
        return "delete record '%s:%s' is in use." % (code, value)

    @staticmethod
    def wrong_time_format(key, value):
        """
        :param key: key phases
        :param value: time
        :return:
        """
        return "improper time format: param '%s:[%s]'." % (key, value)

    @staticmethod
    def wrong_param_type(key, value):
        """
        :param key: Input name
        :param value: Input value
        :return:
        """
        return "The argument '%s must be %s'." % (key, value)

    @staticmethod
    def wrong_param_must(key):
        """
        :param key:
        :return:
        """
        return "The argument '" + key + "' is missed."

    @staticmethod
    def database_exception(error_code=None):
        """
        :return:
        """
        if error_code:
            if error_code == 1022:
                msg = "Failure of database connection."
            elif error_code == 1024:
                msg = "Database operation exception."
            else:
                msg = ""
            return msg
        else:
            return ""

    @staticmethod
    def operation_success(data_name=None, operation_name=None):
        """
        :param data_name:
        :param operation_name:
        :return:
        """
        return "%s data %s success." % (data_name, operation_name)

    @staticmethod
    def record_not_exist(data, value):
        """
        :param data:
        :param value:
        :return:
        """
        return "Data '(%s,%s)' is  not exist." % (data, value)

    @staticmethod
    def mission_db_exist(sat_code):
        """
        :param sat_code:
        :return:
        """
        return "Mission db with this '%s' name already exists" % (sat_code)

    @staticmethod
    def relation_not_exist(v1, v2):
        """
        :param data:
        :param value:
        :return:
        """
        return "Relationship between '(%s,%s)' is  not exist." % (v1, v2)
