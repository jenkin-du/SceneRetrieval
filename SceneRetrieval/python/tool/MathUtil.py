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


'''
    计算两个坐标点的距离
'''


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


'''
    计算多边形的对角线长度
'''


def polygonCatercorner(polygon):
    # 将重心移到原点
    gravity = polygon.gravity
    partList = []
    for part in polygon.partList:
        p = []
        for pnt in part:
            point = Point()
            point.x = pnt.x - gravity.x
            point.y = pnt.y - gravity.y

            p.append(point)
        partList.append(p)

    # 两个顶点
    rt = Point()
    lb = Point()
    rt.x = lb.x = partList[0][0].x
    rt.y = lb.y = partList[0][0].y

    for i in range(len(partList)):
        for k in range(len(partList[i])):
            if partList[i][k].x < lb.x:
                lb.x = partList[i][k].x
            if partList[i][k].x > rt.x:
                rt.x = partList[i][k].x

            if partList[i][k].y < lb.y:
                lb.y = partList[i][k].y
            if partList[i][k].y > rt.y:
                rt.y = partList[i][k].y

    # 正对角线长度
    return pointDistance(rt, lb), partList


'''
    给定两个点，算方位角
'''


def pointAzimuth(originPoint, angularPoint):
    dx = angularPoint.x - originPoint.x
    dy = angularPoint.y - originPoint.y

    azimuth = 0
    if dx > 0 and dy >= 0:
        azimuth = (np.pi / 2 - np.arctan(dy / dx))
    if dx > 0 > dy:
        azimuth = (np.pi / 2 + np.arctan(np.abs(dy) / dx))
    if dx < 0 <= dy:
        azimuth = (np.pi * 3 / 2 + np.arctan(dy / np.abs(dx)))
    if dx < 0 and dy < 0:
        azimuth = (np.pi * 3 / 2 - np.arctan(np.abs(dy) / np.abs(dx)))
    if dx == 0 and dy >= 0:
        azimuth = 0
    if dx == 0 and dy < 0:
        azimuth = np.pi

    return np.rad2deg(azimuth)
