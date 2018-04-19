# -*- coding:utf-8 -*-

from model.Polygon import *

'''
    匹配的多边形
'''


class MatchedPolygon(object):
    # 原矢量
    origin = None  # type:Polygon
    # 匹配的polygon列表
    matchingList = []  # type:list[Polygon]
    # 匹配度
    mdList = []  # type:list[float]
    # 匹配时，原矢量的缩放比率
    scaleList = []  # type:list[float]
