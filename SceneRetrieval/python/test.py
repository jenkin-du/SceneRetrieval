# -*- coding:utf-8 -*-

import mathUtil as mu
import numpy as np
from Class.Point import *
from Class.Polygon import *
import arcpy
import os
import sys
import re
import shapeVector as sv

pass
# if __name__ == '__main__':
#
#     # with arcpy.da.SearchCursor("polygon.shp",["OID@","SHAPE@XY"]) as cursor:
#     #     for row in cursor:
#     #         ID=row[0]
#     #         x=row[1][0]
#     #         y=row[1][1]
#     #
#     #         print("id:"+bytes(ID)+",x:"+bytes(x)+",y:"+bytes(y))
#     #
#     #     pass
#     #
#     # pass
#     # 列出windows目录下的所有文件和文件名
#
#     # dir = r"H:\学习\课程\大三\实习\outData"
#     # files = os.listdir(unicode(dir, "utf-8"))
#     #
#     # features = []
#     # for file in files:
#     #     filePath = os.path.join(dir, file)
#     #     if os.path.isfile(filePath) and len(file.split(".")) == 2 and file.split(".")[1] == "shp":
#     #         features.append(file)
#     #
#     # polygons = []
#     # for featureName in features:
#     #     desc = arcpy.Describe(featureName)
#     #     if desc.shapeType == "Polygon":
#     #         print(featureName + "，" + desc.shapeType)
#
#     polygons = sv.getShapeVector("polygon.shp")
#     for poly in polygons:
#         pass
#     pass

# arcpy.env.overwriteOutput = True
# 指定输出数据的路径
# outputFeatureClass = r"D:\毕设\工程\data\polygon3.shp"

arcpy.env.overwriteOutput = True
# 指定输出数据的路径
outputFeatureClass = r"D:\毕设\工程\data\dividingLine.shp"


def drawPolygon(coord_list):
    features = []
    # 读取坐标串
    for part in coord_list:
        array = arcpy.Array()
        for coordPair in part:
            point = arcpy.Point()
            point.X = coordPair[0]
            point.Y = coordPair[1]
            array.add(point)
        line = arcpy.Polyline(array)
        features.append(line)
    # 生成要素类
    arcpy.CopyFeatures_management(features, outputFeatureClass)


if __name__ == '__main__':
    # coordList = [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]
    #
    # rad = np.deg2rad(45)
    # print(rad)
    # print(np.cos(rad))
    # print(np.sin(rad))
    # gp = [0, 0]
    # for part in coordList:
    #     for pnt in part:
    #         print("x: " + bytes(pnt[0]) + ", y: " + bytes(pnt[1]))
    #         pnt[0] = (pnt[0] - gp[0]) * np.cos(rad) - (pnt[1] - gp[1]) * np.sin(rad) + gp[0]
    #         pnt[1] = (pnt[0] - gp[0]) * np.sin(rad) + (pnt[1] - gp[1]) * np.cos(rad) + gp[1]
    #         print("x: " + bytes(pnt[0]) + ", y: " + bytes(pnt[1]))

    # for part in coordList:
    #     for pnt in part:
    #         print("x: " + bytes(pnt[0]) + ", y: " + bytes(pnt[1]))
    #         pnt[0] = pnt[0] * np.cos(rad) - pnt[1] * np.sin(rad)
    #         pnt[1] = pnt[0] * np.sin(rad) + pnt[1] * np.cos(rad)
    #         print("x: " + bytes(pnt[0]) + ", y: " + bytes(pnt[1]))
    # rad = np.deg2rad(330)
    # gp = [5, 5]
    # for part in coordList:
    #     for pnt in part:
    #         pnt[0] = (pnt[0] - gp[0]) * np.cos(rad) - (pnt[1] - gp[1]) * np.sin(rad) + gp[0]
    #         pnt[1] = (pnt[0] - gp[0]) * np.sin(rad) + (pnt[1] - gp[1]) * np.cos(rad) + gp[1]
    # drawPolygon(coordList)

    # features = []  # type: # List[Polyline]
    polygons = sv.getShapeVector("polygon.shp")

    # # pass
    # for poly in polygons:
    #     polylines = poly.dividingLines  # type: List[Polyline]
    #     for polyline in polylines:
    #         for line in polyline.lines:
    #
    #             array = arcpy.Array()
    #             for pnt in line.pointList:
    #                 point = arcpy.Point()
    #                 point.X = pnt.x
    #                 point.Y = pnt.y
    #
    #                 array.append(point)
    #             pointList = arcpy.Polyline(array)
    #             features.append(pointList)
    # #
    # # #
    # # # features.append(array)
    # # # for array in features:
    # # #     for pnt in array:
    # # #         print(pnt)
    # # # # 生成要素类
    # arcpy.CopyFeatures_management(features, outputFeatureClass)


    pass
