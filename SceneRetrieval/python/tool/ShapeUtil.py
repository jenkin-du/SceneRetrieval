# -*- coding:utf-8 -*-

"""

    该程序获得面状要素的形状矢量
"""
import arcpy
import numpy as np

from model.Polygon import *
from model.Polyline import *
from model.Constant import *


# 获得多边形的顶点序列
def getPointList(workspace, shapeName):
    """

    :rtype: List[Polygon]
    """
    # 多边形列表

    # 设置工作空间
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True
    # 设置没内存工作空间

    polygonList = []  # type: List[Polygon]

    # 获得矩形的坐标点
    with arcpy.da.SearchCursor(shapeName, ["OID@", "SHAPE@", "SHAPE@XY"]) as cursor:
        for row in cursor:

            polygon = Polygon()
            parts = []

            for seg in row[1]:
                part = []
                for pnt in seg:
                    point = Point()
                    if pnt:
                        point.x = pnt.X
                        point.y = pnt.Y
                        part.append(point)
                part.pop()
                parts.append(part)

            polygon.partList = parts
            polygon.oid = shapeName.split(".")[0] + "_" + bytes(row[0])
            polygon.gravity = Point(row[2][0], row[2][1])
            polygon.area = row[1].area

            polygonList.append(polygon)

        del cursor

    return polygonList


# 计算两个图形的相似性
def matchPolygon(sourcePolygon, retrievalPolygon):
    # 正对角线长度
    s_len, sourcePartList = mu.polygonCatercorner(sourcePolygon)

    # 正对角线长度
    r_len, retrievalPartList = mu.polygonCatercorner(retrievalPolygon)

    scale = r_len / s_len
    for part in sourcePartList:
        for pnt in part:
            pnt.x *= scale
            pnt.y *= scale

    # 构建多边形求交
    arcpy.env.workspace = dataPath
    arcpy.env.overwriteOutput = True

    workspace = "in_memory\\"
    sourceInFeature = workspace + sourcePolygon.oid + "_in"

    sourceFeatures = []
    for part in sourcePartList:
        array = arcpy.Array()
        for pnt in part:
            point = arcpy.Point()
            point.X = pnt.x
            point.Y = pnt.y

            array.append(point)
        poly = arcpy.Polygon(array)
        sourceFeatures.append(poly)
    arcpy.CopyFeatures_management(sourceFeatures, sourceInFeature)

    retrievalInFeature = workspace + retrievalPolygon.oid + "_in"
    retrievalFeatures = []
    for part in retrievalPartList:
        array = arcpy.Array()
        for pnt in part:
            point = arcpy.Point()
            point.X = pnt.x
            point.Y = pnt.y

            array.append(point)
        poly = arcpy.Polygon(array)
        retrievalFeatures.append(poly)
    arcpy.CopyFeatures_management(retrievalFeatures, retrievalInFeature)

    # 相交取反
    diffOutFeature = workspace + retrievalPolygon.oid + "_diff"
    arcpy.SymDiff_analysis(sourceInFeature, retrievalInFeature, diffOutFeature)
    # 求取差异面积，求差异度
    sArea = 0
    rArea = 0
    dArea = 0

    with arcpy.da.SearchCursor(diffOutFeature, ["SHAPE@"]) as cursor:
        for row in cursor:
            dArea += row[0].area
    with arcpy.da.SearchCursor(sourceInFeature, ["SHAPE@"]) as cursor:
        for row in cursor:
            sArea += row[0].area
    with arcpy.da.SearchCursor(retrievalInFeature, ["SHAPE@"]) as cursor:
        for row in cursor:
            rArea += row[0].area

    # 删除中间数据
    arcpy.Delete_management(diffOutFeature)
    arcpy.Delete_management(sourceInFeature)
    arcpy.Delete_management(retrievalInFeature)

    d = dArea / (sArea + rArea)
    return 1 - d, scale
