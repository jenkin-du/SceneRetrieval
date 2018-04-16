# -*- coding:utf-8 -*-

from model.Polygon import *


class MatchedPolygon(object):
    # 原矢量
    sourcePolygon = Polygon()
    # 检索矢量
    retrievalPolygon = Polygon()
    # 匹配度
    matchingDegree = 0
    # 匹配时，原矢量的缩放比率
    scale = 1
