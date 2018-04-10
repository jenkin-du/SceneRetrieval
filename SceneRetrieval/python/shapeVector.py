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

    pointLists = [[]]
    polygons = []

    with arcpy.da.SearchCursor(shapeName, ["OID@", "SHAPE@", "SHAPE@XY"]) as cursor:
        for row in cursor:
            polygon = Polygon()
            print(row[1].partCount)
            for part in row[1]:
                pointList = []
                for pnt in part:
                    if pnt:
                        pointList.append(pnt)
                    print "pointList :len= ",
                    print(len(pointList))
                pointLists.append(pointList)
                print "pointLists :len= ",
                print(len(pointLists))

            polygon.pointLists = pointLists
            polygon.oid = shapeName.split(".")[0] + "-" + bytes(row[0])
            polygon.gravity = Point(row[2][0], row[2][1])

            polygons.append(polygon)

    return polygons


print(Path)
