# -*- coding:utf-8 -*-
import arcpy

from model.Programme import *
from model.Constant import *
from model.Polygon import *
from model.Time import Time

import tool.MathUtil as mu

program = Programme()
program.start()

if __name__ == '__main__':

    shapeName = "scene.shp"
    workspace = dataPath + "scene\\"
    # 多边形列表
    readTime = Time("read " + shapeName)
    readTime.start()

    # 设置工作空间
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    polygonList = []  # type: list[Polygon]

    # 获得矩形的坐标点
    with arcpy.da.SearchCursor(shapeName, ["OID@", "SHAPE@"]) as cursor:
        for row in cursor:
            polygon = row[1]
            polygon.oid = shapeName.split(".")[0] + "_" + bytes(row[0])
            polygon.catercorner = mu.pointDistance(polygon.extent.lowerLeft, polygon.extent.upperRight)
            polygon.isCreated = False
            # 获得高宽比
            polygon.hwRatio = polygon.extent.height / polygon.extent.width
            polygonList.append(polygon)

        del cursor

    readTime.stop()


    # 设置工作空间
    shapeName="building.shp"
    readTime = Time("read " + shapeName)
    readTime.start()

    workspace = dataPath
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True

    polygonList = []  # type: list[Polygon]

    # 获得矩形的坐标点
    with arcpy.da.SearchCursor(shapeName, ["OID@", "SHAPE@"]) as cursor:
        for row in cursor:
            polygon = row[1]
            polygon.oid = shapeName.split(".")[0] + "_" + bytes(row[0])
            polygon.catercorner = mu.pointDistance(polygon.extent.lowerLeft, polygon.extent.upperRight)
            polygon.isCreated = False
            # 获得高宽比
            polygon.hwRatio = polygon.extent.height / polygon.extent.width
            polygonList.append(polygon)

        del cursor

    readTime.stop()
