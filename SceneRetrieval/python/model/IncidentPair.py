# -*- coding:utf-8 -*-

from IncidentNode import *


class IncidentPair(object):
    # 第一个关联顶点
    firstNode = IncidentNode()

    # 第二个关联顶点
    lastNode = IncidentNode()

    # 关联度（场景的匹配度）
    correlation = 0
