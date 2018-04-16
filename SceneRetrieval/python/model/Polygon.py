# -*- coding:utf-8 -*-


from model.Point import *
from model.Envelope import *
from model.Polyline import *


class Polygon(object):
    oid = ""  # type: str # 全局唯一id

    partList = []  # type: List[List[Point]] # 面状要素的部分集合

    vector = []  # type: List[float] # 形状矢量

    orient = 0  # 方向 方位角（0，180）

    envelope = Envelope()  # 外包矩形

    gravity = Point()  # 重心

    diff = -1  # 形状矢量的平均差异

    area = 0  # 面积

    def __str__(self):
        return self.oid

    pass
