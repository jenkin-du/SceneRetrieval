# -*- coding:utf-8 -*-


from model.Point import *
from model.Envelope import *
from model.Polyline import *


class Polygon(object):
    oid = ""  # type: str # 全局唯一id

    partList = []  # type: List[List[Point]] # 面状要素的部分集合

    vectorList = []  # type: List[List[float]] # 形状矢量

    def __str__(self):
        return self.oid

    pass
