# -*- coding:utf-8 -*-

'''
    线段类
'''

from Class.Point import *
import mathUtil as mu


class Line(object):
    # id
    oid = ""
    # 起止点
    startPoint = Point()
    endPoint = Point()
    segments = []
    # 长度
    _length = 0

    def getLength(self):
        if self._length == 0:
            for seg in self.segments:
                self._length += seg.getLength()

        return self._length


class LineSegment(object):
    # 起止点
    startPoint = Point()
    endPoint = Point()
    # 长度
    _length = 0
    # 顶点序列
    pointList = []

    def getLength(self):

        if self._length == 0:
            p1 = self.pointList[0]
            for i in range(2, len(self.pointList)):
                p2 = self.pointList[i]
                self._length += mu.getPointDistance(p1, p2)
                p1 = p2

        return self._length
