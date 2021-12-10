#!/usr/bin/python
# -*- coding: UTF-8 -*
"""

"""

from flask import jsonify, Response
import json
import datetime

from utils.xml_json_process import json_to_xml


def response_json(data):
    """
    json响应处理
    :param data: json数据
    :return:
    """
    # return data
    return jsonify(data)

def response_xml(data,root=None):
    """
    xml响应处理
    :param data: json数据
    :param root: xml数据的根
    :return:
    """
    if root is not None:
        json_str = {"response":data}
        data['data'] = {root:data.get('data')}
    else:
        json_str = {"response": data}
    info = json_to_xml(json_str)
    return Response(info, mimetype="text/xml")


def response_result_process(data,xml_structure_str=None,xml=None):
    """
    响应数据处理
    :param data: 响应数据
    :param xml_structure_str: 响应为xml结构的时候 有数据结构的时候需要传,无数据结构的时候就不需要传
    :param xml: 是否是xml响应
    :return:
    """
    if xml is None and xml_structure_str is not None:
        return response_json(data)
    elif xml is None and xml_structure_str is None:
        return response_json(data)
    elif xml is not None and xml_structure_str is None:
        return response_xml(data)
    else:
        # return response_xml(data, xmlEnum.__getattr__(xml_structure_str).value)
        return response_xml(data, xml_structure_str)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)