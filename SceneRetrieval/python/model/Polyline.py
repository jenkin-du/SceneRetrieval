# -*- coding:utf-8 -*-

'''
    线段类
'''

from model.Point import *


class Polyline(object):
    # id
    oid = ""
    # 起止点
    startPoint = Point()
    endPoint = Point()
    lines = []  # type: List[Line]
    # 长度
    _length = 0

    def getLength(self):
        if self._length == 0:
            for seg in self.lines:
                self._length += seg.getLength()

        return self._length


class Line(object):
    # id
    oid = ""
    # 起止点
    startPoint = Point()
    endPoint = Point()
    # 长度
    length = 0
    # 顶点序列
    pointList = []  # type: List[Point]

    # def getLength(self):
    #
    #     if self.length == 0:
    #         p1 = self.pointList[0]
    #         for i in range(2, len(self.pointList)):
    #             p2 = self.pointList[i]
    #             self.length += mu.pointDistance(p1, p2)
    #             p1 = p2
    #
    #     return self.length
