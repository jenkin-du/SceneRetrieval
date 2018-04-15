# -*- coding:utf-8 -*-

import numpy as np
import sympy as sym
from model.Point import *


# 将坐标旋转给定的角度,角度单位为°
def rotateCoord(gp, pt, rad=0):
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
def matchPolygon(scenePolygon, retrievalPolygon):
    """

    :type scenePolygon: Polygon
    :type retrievalPolygon: Polygon
    """
    sv = scenePolygon.vector
    rv = retrievalPolygon.vector

    # 两个polygon的差异度
    d = 0
    for i in range(len(sv)):
        d += np.abs(sv[i] - rv[i])
    d /= len(sv)

    # 返回匹配度
    return 1 - d


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


# 计算一个矢量要素的主方向
def getMainDirection(polygon):
    # 重心位置
    gravity = polygon.gravity

    # 计算主方向：某点与重心连线最长为其主方向
    length = pointDistance(gravity, polygon.partList[0][0])
    partList = polygon.partList

    # 找到最大长度的
    for i in range(len(partList)):
        for j in range(len(partList[i])):
            l = pointDistance(gravity, partList[i][j])
            if l > length:
                length = l

    # 找到相同的主方向
    mainPointList = []  # type: List[Point]
    for i in range(len(partList)):
        for j in range(len(partList[i])):
            l = pointDistance(gravity, partList[i][j])
            if l == length:
                mainPointList.append(partList[i][j])

    radList = []  # type:List[float]
    # 计算主方向，方向角，弧度
    for pnt in mainPointList:

        dx = pnt.x - gravity.x
        dy = pnt.y - gravity.y
        if dx > 0 and dy >= 0:
            radList.append(np.pi / 2 - np.arctan(dy / dx))
        if dx > 0 > dy:
            radList.append(np.pi / 2 + np.arctan(np.abs(dy) / dx))
        if dx < 0 <= dy:
            radList.append(np.pi * 3 / 2 + np.arctan(dy / np.abs(dx)))
        if dx < 0 and dy < 0:
            radList.append(np.pi * 3 / 2 - np.arctan(np.abs(dy) / np.abs(dx)))
        if dx == 0 and dy >= 0:
            radList.append(0)
        if dx == 0 and dy < 0:
            radList.append(np.pi)

    return radList
