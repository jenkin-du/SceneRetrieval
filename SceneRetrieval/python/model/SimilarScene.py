# -*- coding:utf-8 -*-

import arcpy

from model.Envelope import Envelope


class SimilarScene(object):
    # 场景的polygon
    origin = []  # type:list[str]

    # 数据库中的polygon
    database = []  # type:list[str]

    # 相似度
    md = 0

    # 外接矩形
    envelope = Envelope()
