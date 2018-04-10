# -*- coding:utf-8 -*-

from Class.Point import *


class Polygon(object):
    oid = ""  # 全局唯一id
    pointLists = [[]]  # 面状要素的所有点坐标
    vector = []  # 形状矢量
    gravity = Point()  # 重心

    def __str__(self):
        return self.oid + ":len:" + bytes(len(self.pointLists))

    pass
