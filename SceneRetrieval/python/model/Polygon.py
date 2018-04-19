# -*- coding:utf-8 -*-

import arcpy


class Polygon(arcpy.Polygon):
    oid = ""  # type: str # 全局唯一id

    scale = 1  # 匹配原场景中的图形时，该图形的缩放比率

    catercorner = -1  # 外包矩形的斜长

    uniformedPartList = []  # 将坐标归一化后的坐标

    isCreated = False  # 是否创建过

    def __str__(self):
        return self.oid

    pass
