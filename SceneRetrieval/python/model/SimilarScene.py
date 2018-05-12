# -*- coding:utf-8 -*-

import arcpy

from model.Envelope import Envelope


class SimilarScene(object):

    # 数据库中的polygon
    polygonList = []  # type:list[str]

    # 相似度
    md = 0  # type:float

