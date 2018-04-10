# -*- coding:utf-8 -*-

'''
    线段类
'''

from Class.Point import *


class Line(object):
    # 起止点
    startPoint = Point()
    endPoint = Point()
    # 长度
    length = 0

    segments = []


class LineSegment(object):
    # 起止点
    startPoint = Point()
    endPoint = Point()
    # 长度
    length = 0
    # 顶点序列
    pointList = []
