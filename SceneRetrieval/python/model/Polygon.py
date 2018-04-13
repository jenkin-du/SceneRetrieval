# -*- coding:utf-8 -*-


from model.Point import *
from model.Envelope import *
from model.Polyline import *


class Polygon(object):
    oid = ""  # type: str # 全局唯一id

    partList = []  # type: List[List[Point]] # 面状要素的部分集合

    vector = []  # type: List[int] # 形状矢量

    mainVector = 0     #主方向的顺序特征描述量

    gravity = Point()  # 重心

    envelope = Envelope()  # 外包矩形

    dlList = []  # type: List[Polyline] # 分割线列表 每个分割线由两个坐标构成

    gravityLine = Polyline()  # 穿过重心位置的分割线

    def __str__(self):
        return self.oid

    pass
