# -*- coding:utf-8 -*-

import arcpy

from model.Envelope import Envelope


class Polygon(arcpy.Polygon):
    oid = ""  # type: str # 全局唯一id

    scale = 1  # 匹配原场景中的图形时，该图形的缩放比率

    catercorner = -1  # 外包矩形的斜长

    uniformedPartList = []  # 将坐标归一化后的坐标

    uniformedEnvelope = Envelope()  # 坐标归一化后的envelope

    isCreated = False  # 是否创建过

    hwRatio = 1  # 高宽比

    def __str__(self):
        return self.oid

    pass
