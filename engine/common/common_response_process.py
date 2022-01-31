#!/usr/bin/python
# -*- coding: UTF-8 -*

from flask import jsonify, Response
import json
import datetime

from utils.xml_json_process import json_to_xml


def response_json(data):
    """
    :param data: json data
    :return:
    """
    # return data
    return jsonify(data)

def response_xml(data,root=None):
    """
    :param data: json data
    :param root: xml data root
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
    :param data: response data
    :param xml_structure_str: If response in xml structure, the structure need to be uploaded. if no data structure, structure is not needed
    :param xml: Check if xml response
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
