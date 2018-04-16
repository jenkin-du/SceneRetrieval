# -*- coding:utf-8 -*-

import numpy as np
import sympy as sym
from model.Point import *
from model.Constant import *
import arcpy


# 将坐标旋转给定的角度,角度单位为°
def rotateCoord(gp, pt, deg):
    rad = np.deg2rad(deg)
    x = pt.x
    y = pt.y
    pt.x = (x - gp.x) * np.cos(rad) - (y - gp.y) * np.sin(rad) + gp.x
    pt.y = (x - gp.x) * np.sin(rad) + (y - gp.y) * np.cos(rad) + gp.y


# 获得多边形的重心，输入为多边形的顺序坐标
def calculateGravity(pointList):
    # 重心坐标
    gravity = Point()

    p1 = pointList[0]
    p2 = pointList[1]

    x1 = p1.x
    y1 = p1.y

    sum_x = 0
    sum_y = 0
    sum_area = 0
    for i in range(2, len(pointList)):
        x2 = p2.x
        y2 = p2.y

        p3 = pointList[i]
        x3 = p3.x
        y3 = p3.y

        area = ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2.0

        sum_x += (x1 + x2 + x3) * area
        sum_y += (y1 + y2 + y3) * area
        sum_area += area

        p2 = p3

    gravity.x = sum_x / sum_area / 3.0
    gravity.y = sum_y / sum_area / 3.0

    return gravity


# 计算两个坐标点的距离
def pointDistance(p1, p2):
    return np.sqrt(np.square(p1.x - p2.x) + np.square(p1.y - p2.y))


# 计算两个polygon的相似性
def matchVector(sceneVector, retrievalVector):
    """

    :type sceneVector: list[float]
    :type retrievalVector: list[float]
    """
    sv = sceneVector
    rv = retrievalVector

    # 两个polygon的差异度
    d = 0
    for i in range(len(sv)):
        d += np.abs(sv[i] - rv[i])
    d /= len(sv)

    # 返回匹配度
    return 1 - d


# 计算两个图形的相似性
def matchPolygon(sourcePolygon, retrievalPolygon):
    # 将重心移到原点
    sg = sourcePolygon.gravity
    sourcePartList = []
    for part in sourcePolygon.partList:
        sourcePart = []
        for pnt in part:
            point = Point()
            point.x = pnt.x - sg.x
            point.y = pnt.y - sg.y

            sourcePart.append(point)
        sourcePartList.append(sourcePart)

    rg = retrievalPolygon.gravity
    retrievalPartList = []
    for part in retrievalPolygon.partList:
        retrievalPart = []
        for pnt in part:
            point = Point()
            point.x = pnt.x - rg.x
            point.y = pnt.y - rg.y

            retrievalPart.append(point)
        retrievalPartList.append(retrievalPart)
    """
       计算出polygon的外包矩形
    """
    # 两个顶点
    s_rt = Point()
    s_lb = Point()
    s_parts = sourcePartList
    s_rt.x = s_lb.x = s_parts[0][0].x
    s_rt.y = s_lb.y = s_parts[0][0].y

    for i in range(len(s_parts)):
        for k in range(len(s_parts[i])):
            if s_parts[i][k].x < s_lb.x:
                s_lb.x = s_parts[i][k].x
            if s_parts[i][k].x > s_rt.x:
                s_rt.x = s_parts[i][k].x

            if s_parts[i][k].y < s_lb.y:
                s_lb.y = s_parts[i][k].y
            if s_parts[i][k].y > s_rt.y:
                s_rt.y = s_parts[i][k].y

    # 正对角线长度
    s_len = pointDistance(s_rt, s_lb)

    # 计算出polygon的外包矩形
    # 两个顶点
    r_rt = Point()
    r_lb = Point()
    r_parts = retrievalPartList
    r_rt.x = r_lb.x = r_parts[0][0].x
    r_rt.y = r_lb.y = r_parts[0][0].y

    for i in range(len(r_parts)):
        for k in range(len(r_parts[i])):
            if r_parts[i][k].x < r_lb.x:
                r_lb.x = r_parts[i][k].x
            if r_parts[i][k].x > r_rt.x:
                r_rt.x = r_parts[i][k].x

            if r_parts[i][k].y < r_lb.y:
                r_lb.y = r_parts[i][k].y
            if r_parts[i][k].y > r_rt.y:
                r_rt.y = r_parts[i][k].y

    # 正对角线长度
    r_len = pointDistance(r_rt, r_lb)

    minLen = min(s_len, r_len)
    maxLen = max(s_len, r_len)

    scale = maxLen / minLen
    if minLen == s_len:
        for part in sourcePartList:
            for pnt in part:
                pnt.x *= scale
                pnt.y *= scale
    else:
        for part in retrievalPartList:
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
    return 1 - d
