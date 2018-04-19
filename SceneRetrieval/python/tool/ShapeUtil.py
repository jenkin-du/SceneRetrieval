# -*- coding:utf-8 -*-

"""

    该程序获得面状要素的形状矢量
"""
import arcpy
import numpy as np

import MathUtil as mu
from model.Polygon import *
from model.Constant import *


# 获得多边形的顶点序列
def getPolygonList(workspace, shapeName):
    """

    :rtype: List[Polygon]
    """
    # 多边形列表

    # 设置工作空间
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True
    # 设置没内存工作空间

    polygonList = []  # type: list[Polygon]

    # 获得矩形的坐标点
    with arcpy.da.SearchCursor(shapeName, ["OID@", "SHAPE@"]) as cursor:
        for row in cursor:
            polygon = row[1]
            polygon.oid = shapeName.split(".")[0] + "_" + bytes(row[0])
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
    for polygon in sourcePartList:
        for array in polygon:
            for pnt in array:
                pnt.X *= scale
                pnt.Y *= scale

    # 构建多边形求交
    arcpy.env.workspace = dataPath
    arcpy.env.overwriteOutput = True

    workspace = ""
    suffix=".shp"
    sourceInFeature = workspace + sourcePolygon.oid + "_in"+suffix
    arcpy.CopyFeatures_management(sourcePartList, sourceInFeature)

    retrievalInFeature = workspace + retrievalPolygon.oid + "_in"+suffix
    arcpy.CopyFeatures_management(retrievalPartList, retrievalInFeature)

    # 相交取反
    diffOutFeature = workspace + retrievalPolygon.oid + "_diff"+suffix
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


def indexOfMatched(matchedList, polygon):
    '''

    :param matchedList:
    :param polygon:
    :return:
    '''

    for i in range(len(matchedList)):
        if matchedList[i].origin == polygon:
            return i
