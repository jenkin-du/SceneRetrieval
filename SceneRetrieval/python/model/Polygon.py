# -*- coding:utf-8 -*-


from model.Point import *
from model.Envelope import *
from model.Polyline import *


class Polygon(object):
    oid = ""  # type: str # 全局唯一id

    parts = []  # type: List[List[Point]] # 面状要素的部分集合

    vector = []  # type: List[int] # 形状矢量

    gravity = Point()  # 重心

    envelope = Envelope()  # 外包矩形

    dLines = []  # type: List[Polyline] # 分割线列表 每个分割线由两个坐标构成

    def __str__(self):
        return self.oid

    pass
