# -*- coding:utf-8 -*-

import numpy as np
import arcpy


# 将坐标旋转给定的角度,角度单位为°
def rotateCoord(gp, pt, deg):
    rad = np.deg2rad(deg)
    X = pt.X
    Y = pt.Y
    pt.X = (X - gp.X) * np.cos(rad) - (Y - gp.Y) * np.sin(rad) + gp.X
    pt.Y = (X - gp.X) * np.sin(rad) + (Y - gp.Y) * np.cos(rad) + gp.Y


# 获得多边形的重心，输入为多边形的顺序坐标
def calculateGravity(pointList):
    # 重心坐标
    centroid = arcpy.Point()

    p1 = pointList[0]
    p2 = pointList[1]

    x1 = p1.X
    y1 = p1.Y

    sum_x = 0
    sum_y = 0
    sum_area = 0
    for i in range(2, len(pointList)):
        x2 = p2.X
        y2 = p2.Y

        p3 = pointList[i]
        x3 = p3.X
        y3 = p3.Y

        area = ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2.0

        sum_x += (x1 + x2 + x3) * area
        sum_y += (y1 + y2 + y3) * area
        sum_area += area

        p2 = p3

    centroid.X = sum_x / sum_area / 3.0
    centroid.Y = sum_y / sum_area / 3.0

    return centroid


'''
    计算两个坐标点的距离
'''


def pointDistance(p1, p2):
    return np.sqrt(np.square(p1.X - p2.X) + np.square(p1.Y - p2.Y))


'''
    将多个多边形的外包矩形合并为一个最大的
'''


def getExtent(extentList):
    #

    xMax = 0
    yMax = 0

    xMin = 0
    yMin = 0

    for extent in extentList:

        if xMin > extent.XMin:
            xMin = extent.XMin
        if xMax < extent.XMax:
            xMax = extent.XMax
        if yMin > extent.YMin:
            yMin = extent.YMin
        if yMax < extent.YMax:
            yMax = extent.YMax

    return arcpy.Extent(xMin, yMin, xMax, yMax)

    pass


'''
    计算多边形的对角线长度,并将重心移到原点
'''


def polygonCatercorner(polygon):
    # 正对角线长度
    dis = pointDistance(polygon.extent.lowerLeft, polygon.extent.upperRight)

    # 将重心移到原点
    centroid = polygon.centroid
    polylineList = []
    for part in polygon:
        array = arcpy.Array()
        for pnt in part:
            point = arcpy.Point()
            point.X = pnt.X - centroid.X
            point.Y = pnt.Y - centroid.Y

            array.append(point)
        polygon = arcpy.Polygon(array)
        polylineList.append(polygon)

    return dis, polylineList


'''
    给定两个点，算方位角
'''


def pointAzimuth(originPoint, angularPoint):
    dx = angularPoint.X - originPoint.X
    dy = angularPoint.Y - originPoint.Y

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
