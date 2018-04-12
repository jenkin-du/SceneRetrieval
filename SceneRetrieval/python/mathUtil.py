# -*- coding:utf-8 -*-

import numpy as np
from model.Point import *


# 将坐标旋转给定的角度,角度单位为°
def rotateCoord(gp, pt, angle=0):
    # 换算成弧度
    rad = np.deg2rad(angle)

    x=pt.x
    y=pt.y
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
