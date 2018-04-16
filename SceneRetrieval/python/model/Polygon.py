# -*- coding:utf-8 -*-


from model.Point import *
from model.Envelope import *
from model.Polyline import *


class Polygon(object):
    oid = ""  # type: str # 全局唯一id

    partList = []  # type: list[list[Point]] # 面状要素的部分集合

    gravity = Point()  # 重心

    area = 0  # 面积

    def __str__(self):
        return self.oid

    pass
