# -*- coding:utf-8 -*-

import mathUtil as mu
from Class.Point import *
from Class.Polygon import *
import arcpy
import os
import sys
import re
import shapeVector as sv

# reload(sys)
# sys.setdefaultencoding('utf8')
arcpy.env.workspace = r"D:\毕设\工程\data"

if __name__ == '__main__':
    # with arcpy.da.SearchCursor("polygon.shp",["OID@","SHAPE@XY"]) as cursor:
    #     for row in cursor:
    #         ID=row[0]
    #         x=row[1][0]
    #         y=row[1][1]
    #
    #         print("id:"+bytes(ID)+",x:"+bytes(x)+",y:"+bytes(y))
    #
    #     pass
    #
    # pass
    # 列出windows目录下的所有文件和文件名

    # dir = r"H:\学习\课程\大三\实习\outData"
    # files = os.listdir(unicode(dir, "utf-8"))
    #
    # features = []
    # for file in files:
    #     filePath = os.path.join(dir, file)
    #     if os.path.isfile(filePath) and len(file.split(".")) == 2 and file.split(".")[1] == "shp":
    #         features.append(file)
    #
    # polygons = []
    # for featureName in features:
    #     desc = arcpy.Describe(featureName)
    #     if desc.shapeType == "Polygon":
    #         print(featureName + "，" + desc.shapeType)

    polygons = sv.getShapeVector("polygon.shp")
    # for poly in polygons:
    #     print(poly)
    #     pointList = poly.pointLists
    #     print("part:")
    #     for part in pointList:
    #         print "partLen:",
    #         print(len(part))
    #         for pnt in part:
    #             print("point:")
    #             print(pnt)
    #
    #     print(poly.gravity)
    pass
