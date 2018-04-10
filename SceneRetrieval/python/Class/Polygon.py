# -*- coding:utf-8 -*-

from Class.Point import *
from Class.Envelope import *


class Polygon(object):
    oid = ""  # 全局唯一id
    parts = []  # 面状要素的部分集合
    vector = []  # 形状矢量
    gravity = Point()  # 重心
    envelope = Envelope()  # 外包矩形
    dividingLines = []  # 分割线列表 每个分割线由两个坐标构成

    def __str__(self):
        return self.oid + ":len:" + bytes(len(self.parts))

    pass
