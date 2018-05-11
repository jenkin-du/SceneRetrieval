# -*- coding:utf-8 -*-

"""

    该程序获得面状要素的形状矢量
"""
import numpy as np
import MathUtil as mu
from model.Polygon import *
from model.Constant import *


# 获得多边形的顶点序列
from model.Time import Time


def getPolygonList(workspace, shapeName):
    """

    :rtype: List[Polygon]
    """
    # 多边形列表
    readTime=Time("read "+shapeName)
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
    return polygonList


# 计算两个图形的相似性
def matchPolygon(sourcePolygon, retrievalPolygon):
    # 先判断其外包矩形的高宽比，剔除掉外包矩形明显不相同的
    hwr_d = np.abs(sourcePolygon.hwRatio - retrievalPolygon.hwRatio)
    if hwr_d < whRatioDiff:

        # 获取归一化后的坐标
        sourcePartList = sourcePolygon.uniformedPartList

        # 计算缩放比
        scale = sourcePolygon.catercorner / retrievalPolygon.catercorner

        # 归一化，将重心移到原点
        retrievalPartList = mu.polygonUniformization(retrievalPolygon, scale)

        # 获得其外包矩形
        retrievalEnvelope = mu.uniformedEnvelope(retrievalPartList)
        #  根据其归一化的外包矩形，先大致判断其是否相交,
        emd = mu.matchEnvelope(sourcePolygon.uniformedEnvelope, retrievalEnvelope)

        if emd > envelope_precision:

            # 构建多边形求交
            arcpy.env.workspace = dataPath
            arcpy.env.overwriteOutput = True

            workspace = "in_memory\\"
            suffix = ""

            sourceInFeature = workspace + sourcePolygon.oid + "_in" + suffix
            # 如果没有创建，就新建一个
            if not sourcePolygon.isCreated:
                arcpy.CopyFeatures_management(sourcePartList, sourceInFeature)
                sourcePolygon.isCreated = True

            retrievalInFeature = workspace + retrievalPolygon.oid + "_in" + suffix
            arcpy.CopyFeatures_management(retrievalPartList, retrievalInFeature)

            # 相交取反
            diffOutFeature = workspace + retrievalPolygon.oid + "_diff" + suffix
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
            arcpy.Delete_management(retrievalInFeature)

            d = dArea / (sArea + rArea)
            return 1 - d, scale
    return 0, 1


def indexOfMatched(matchedList, polygon):
    '''

    :param matchedList:
    :param polygon:
    :return:
    '''

    for i in range(len(matchedList)):
        if matchedList[i].origin == polygon:
            return i
