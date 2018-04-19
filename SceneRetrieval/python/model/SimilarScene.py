# -*- coding:utf-8 -*-

import arcpy

from model.Envelope import Envelope


class SimilarScene(object):
    # 找到的相似场景中的polygon的id
    polygonList = []  # type:list[str]

    # 相似度
    md = 0

    #外接矩形
    envelope=Envelope()

