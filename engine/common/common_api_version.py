#!/usr/bin/python
# -*- coding: UTF-8 -*
"""
"""
from enum import Enum, unique


@unique
class apiVersion(Enum):
    """
    api 版本枚举
    """
    version1 = 'v1'
    version2 = 'v2'
