# -*- coding:utf-8 -*-

'''

    该程序获得面状要素的形状矢量
'''

from Class.Point import *
import mathUtil as mu
import os
import arcpy
from Class.Point import *
from Class.Polygon import *

# 定义面状要素被分割的段数
N = 10

# 数据文件的路径
# 当前路径
pwd = os.getcwd()
Path = os.path.dirname(os.path.abspath(os.path.dirname(pwd) + os.path.sep + "..")) + "\data\ "

# 设置工作空间
arcpy.env.workspace = Path


# 旋转坐标
def rotateCoordinates(pointList, gravityPoint):
    for point in pointList:
        mu.rotateCoord(gravityPoint, point)


# 获得面状要素的形状要素
def getShapeVector(shapeName):
    # 获得面状要素的所有坐标

    polygonLists = []
    pointLists = [[]]

    with arcpy.da.SearchCursor(shapeName, ["SHAPE@"]) as cursor:
        for row in cursor:
            for part in row[0]:
                pointList = []
                for pnt in part:
                    if pnt:
                        pointList.append(pnt)
                pointLists.append(pointList)
            polygon = Polygon()
            polygon.pointLists = pointLists

    pass


print(Path)
