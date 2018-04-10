# -*- coding:utf-8 -*-

from Class.Point import *


class Envelope(object):
    # 外包矩形的四个顶点

    rtPoint = Point()  # 右上
    lbPoint = Point()  # 左下

    def __str__(self):
        return "rt:" + "x:" + bytes(self.rtPoint.x) + " y:" + bytes(self.rtPoint.y) + " lb:" + "x:" + bytes(
            self.lbPoint.x) + " y:" + bytes(self.lbPoint.y)
