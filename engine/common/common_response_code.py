#!/usr/bin/python
# -*- coding: UTF-8 -*

from enum import Enum, unique


@unique
class ErrorCodeEnum(Enum):
    SUCCESS = 200
    LOGIN_IS_FAIL = 1001
    PASS_WORD_INFO_NOT_FILL = 1002
    TWO_PASS_WORD_DIFFERENT = 1003
    OLD_PASS_WORD_IS_NOT_FAIL = 1004
    LOGIN_FAIL = 1005
    PASS_WORD_RESET_FAIL = 1006
    USER_NOT_EXIST = 1007
    IMPORT_CSV_FAIL = 1008
    IMPORT_CSV_SUCCESS = 1009
    RECORD_EXIST = 1010
    ADD_DATA_FAIL = 1011
    UPDATE_DATA_FAIL = 1012
    DELETE_DATA_FAIL = 1013
    GET_DATA_FAIL = 1014
    REQUEST_VERSION_ISEXISTENCE = 1015
    ALREADY_HANDLED = 1016
    DATA_IS_NOT_EXIST = 1017
    REQUEST_PARAM_MISSED = 1018
    EQUEST_PARAM_FORMAT_ERROR = 1019
    OPENTSDB_ERROR = 1020
    DATA_BASE_ERROR = 1021
    NOT_FOUND = 404
    BAD_REQUEST = 400
    FORBIDDEND = 403
    WRONGVALUE = 1022
    CHECK_EXIST_ERROR = 1023
    EXCEPTION_DB = 1024


class responseCode(object):

    @property
    def SUCCESS(self):
        return {'code': 200, 'msg': 'Request Success!'}

    @property
    def LOGIN_IS_FAIL(self):
        return {'code': 1001, 'msg': 'Login failed, please check your username or password'}

    @property
    def PASS_WORD_INFO_NOT_FILL(self):
        return {'code': 1002, 'msg': 'Password is missing or wrong'}

    @property
    def TWO_PASS_WORD_DIFFERENT(self):
        return {'code': 1003, 'msg': 'Password does not match'}

    @property
    def OLD_PASS_WORD_IS_NOT_FAIL(self):
        return {'code': 1004, 'msg': 'old password is incorrect'}

    @property
    def LOGIN_FAIL(self):
        return {'code': 1005, 'msg': 'Login fail, please check with your system admin'}

    @property
    def PASS_WORD_RESET_FAIL(self):
        return {'code': 1006, 'msg': 'Password reset fail'}

    @property
    def USER_NOT_EXIST(self):
        return {'code': 1007, 'msg': 'User 404'}

    @property
    def IMPORT_CSV_FAIL(self):
        return {'code': 1008, 'msg': 'Import CSV failed'}

    @property
    def IMPORT_CSV_SUCCESS(self):
        return {'code': 1009, 'msg': 'CSV imported successfully'}

    @property
    def RECORD_EXIST(self):
        return {'code': 1010, 'msg': 'Record exist'}

    @property
    def ADD_DATA_FAIL(self):
        return {'code': 1011, 'msg': '??????????????????'}

    @property
    def UPDATE_DATA_FAIL(self):
        return {'code': 1012, 'msg': '??????????????????'}

    @property
    def DELETE_DATA_FAIL(self):
        return {'code': 1013, 'msg': '??????????????????'}

    @property
    def GET_DATA_FAIL(self):
        return {'code': 1014, 'msg': '??????????????????'}

    @property
    def REQUEST_VERSION_ISEXISTENCE(self):
        return {'code': 1015, 'msg': '????????????????????????'}

    @property
    def ALREADY_HANDLED(self):
        return {'code': 1016, 'msg': '??????????????????'}

    @property
    def DATA_IS_NOT_EXIST(self):
        return {'code': 1017, 'msg': '???????????????'}

    @property
    def REQUEST_PARAM_MISSED(self):
        return {'code': 1018, 'msg': '??????????????????'}

    @property
    def REQUEST_PARAM_FORMAT_ERROR(self):
        return {'code': 1019, 'msg': '????????????????????????'}

    @property
    def OPENTSDB_ERROR(self):
        return {'code': 1020, 'msg': 'opentsdb???????????????'}

    @property
    def DATA_BASE_ERROR(self):
        return {'code': 1021, 'msg': "?????????????????????"}

    @property
    def NOT_FOUND(self):
        return {'code': 404, 'msg': 'HTTP 404 Not Found'}

    @property
    def BAD_REQUEST(self):
        return {'code': 400, 'msg': 'HTTP 400 Bad Request'}

    @property
    def FORBIDDEND(self):
        return {'code': 403, 'msg': 'HTTP 403 Forbidden'}

    @property
    def WRONGVALUE(self):
        return {'code': 1022, 'msg': '???????????????????????????'}

    @property
    def CHECK_EXIST_ERROR(self):
        return {'code': 1023, 'msg': '??????????????????'}

    @property
    def EXCEPTION_DB(self):
        return {'code': 1024, 'msg': '?????????????????????'}

    def get_struct_by_error_code(self, error_code):
        if error_code == ErrorCodeEnum.SUCCESS:
            return self.SUCCESS
        if error_code == ErrorCodeEnum.LOGIN_IS_FAIL:
            return self.LOGIN_IS_FAIL
        if error_code == ErrorCodeEnum.PASS_WORD_INFO_NOT_FILL:
            return self.PASS_WORD_INFO_NOT_FILL
        if error_code == ErrorCodeEnum.TWO_PASS_WORD_DIFFERENT:
            return self.TWO_PASS_WORD_DIFFERENT
        if error_code == ErrorCodeEnum.OLD_PASS_WORD_IS_NOT_FAIL:
            return self.OLD_PASS_WORD_IS_NOT_FAIL
        if error_code == ErrorCodeEnum.LOGIN_FAIL:
            return self.LOGIN_FAIL
        if error_code == ErrorCodeEnum.PASS_WORD_RESET_FAIL:
            return self.PASS_WORD_RESET_FAIL
        if error_code == ErrorCodeEnum.USER_NOT_EXIST:
            return self.PASS_WORD_RESET_FAIL
        if error_code == ErrorCodeEnum.IMPORT_CSV_FAIL:
            return self.IMPORT_CSV_FAIL
        if error_code == ErrorCodeEnum.IMPORT_CSV_SUCCESS:
            return self.IMPORT_CSV_SUCCESS
        if error_code == ErrorCodeEnum.RECORD_EXIST:
            return self.RECORD_EXIST
        if error_code == ErrorCodeEnum.ADD_DATA_FAIL:
            return self.ADD_DATA_FAIL
        if error_code == ErrorCodeEnum.UPDATE_DATA_FAIL:
            return self.UPDATE_DATA_FAIL
        if error_code == ErrorCodeEnum.DELETE_DATA_FAIL:
            return self.DELETE_DATA_FAIL
        if error_code == ErrorCodeEnum.GET_DATA_FAIL:
            return self.DELETE_DATA_FAIL
        if error_code == ErrorCodeEnum.REQUEST_VERSION_ISEXISTENCE:
            return self.REQUEST_VERSION_ISEXISTENCE
        if error_code == ErrorCodeEnum.ALREADY_HANDLED:
            return self.ALREADY_HANDLED
        if error_code == ErrorCodeEnum.DATA_IS_NOT_EXIST:
            return self.DATA_IS_NOT_EXIST
        if error_code == ErrorCodeEnum.REQUEST_PARAM_MISSED:
            return self.REQUEST_PARAM_MISSED
        if error_code == ErrorCodeEnum.REQUEST_PARAM_FORMAT_ERROR:
            return self.REQUEST_PARAM_FORMAT_ERROR
        if error_code == ErrorCodeEnum.OPENTSDB_ERROR:
            return self.OPENTSDB_ERROR
        if error_code == ErrorCodeEnum.DATA_BASE_ERROR:
            return self.DATA_BASE_ERROR
        if error_code == ErrorCodeEnum.NOT_FOUND:
            return self.NOT_FOUND
        if error_code == ErrorCodeEnum.BAD_REQUEST:
            return self.BAD_REQUEST
        if error_code == ErrorCodeEnum.FORBIDDEND:
            return self.FORBIDDEND
        if error_code == ErrorCodeEnum.WRONGVALUE:
            return self.WRONGVALUE
        if error_code == ErrorCodeEnum.CHECK_EXIST_ERROR:
            return self.CHECK_EXIST_ERROR
        if error_code == ErrorCodeEnum.EXCEPTION_DB:
            return self.EXCEPTION_DB


response_code = responseCode()
