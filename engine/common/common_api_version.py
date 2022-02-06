#!/usr/bin/python
# -*- coding: UTF-8 -*

from enum import Enum, unique

@unique
class apiVersion(Enum):

    version1 = 'v1'
    version2 = 'v2'
