# -*- coding:utf-8 -*-

import arcpy

class Polygon(arcpy.Polygon):
    oid = ""  # type: str # 全局唯一id

    def __str__(self):
        return self.oid

    pass
