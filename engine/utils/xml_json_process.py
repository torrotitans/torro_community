#!/usr/bin/python
# -*- coding: UTF-8 -*

import json
from json import JSONDecodeError
import xmltodict
from common.common_response_code import response_code

def xml_to_json(xml_str):
    """
    :param xml_str:
    :return:
    """
    xml_parse = xmltodict.parse(xml_str)
    json_str = json.dumps(xml_parse, indent=1).replace('\\', '\\\\')
    return json_str


def json_to_xml(json_str):
    """
    :param json_str:
    :return:
    """
    xml_str = xmltodict.unparse(json_str, pretty=1)
    return xml_str


def is_none(request_param):
    """
    :param request_param:
    :return:
    """
    if isinstance(request_param, list):
        for index, a in enumerate(request_param):
            if isinstance(a, str):
                b = request_param.copy()
                if a == None:
                    del b[index]
            else:
                c = a.copy()
                for k, v in c.items():
                    if v == None:
                        del a[k]
                    if isinstance(v, list):
                        b = v.copy()
                        for index, a in enumerate(b):
                            if a == None:
                                del v[index]
    if isinstance(request_param, dict):
        c = request_param.copy()
        for k, v in c.items():
            if v == None:
                del request_param[k]
            if isinstance(v, list):
                b = v.copy()
                for index, a in enumerate(b):
                    if a == None:
                        del v[index]

    return request_param
