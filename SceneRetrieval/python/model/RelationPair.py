# -*- coding:utf-8 -*-

from model.Polygon import *
import tool.MathUtil as mu

'''
    多边形关系类
'''


class RelationPair(object):
    # 第一个polygon
    firstPolygon = Polygon()
    # 第二个polygon
    lastPolygon = Polygon()

    # 该关联对相对于原场景中的关联对的匹配度
    matchingDegree = 0

    def __init__(self, polygonA, polygonB):
        self.firstPolygon = polygonA
        self.lastPolygon = polygonB

        self.getAzimuth()
        self.getGravityDistance()

    # 两个polygon重心之间的夹角，以firstPolygon重心为原点，lastPolygon重心相对于firstPolygon重心的方位角
    _azimuth = 0

    # 两个重心之间的距离
    _distance = 0

    # 计算方位角
    def getAzimuth(self):
        if self._azimuth == 0:
            ga = self.firstPolygon.gravity
            gb = self.lastPolygon.gravity

            self._azimuth = mu.pointAzimuth(ga, gb)
        return self._azimuth

    # 计算两个polygon之间的距离
    def getGravityDistance(self):
        if self._distance == 0:
            ga = self.firstPolygon.gravity
            gb = self.lastPolygon.gravity

            self._distance = mu.pointDistance(ga, gb)
        return self._distance

    pass
