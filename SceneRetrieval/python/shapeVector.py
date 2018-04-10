# -*- coding:utf-8 -*-

'''

    该程序获得面状要素的形状矢量
'''


import mathUtil as mu
import os
import arcpy
from Class.Polygon import *
from Class.Polyline import *

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

    polygons = []  # type: List[Polygon]
    # 获取polygon的信息
    with arcpy.da.SearchCursor(shapeName, ["OID@", "SHAPE@", "SHAPE@XY"]) as cursor:
        for row in cursor:

            polygon = Polygon()
            parts = []  # type: List[List[Point]]

            for seg in row[1]:
                part = []  # type: List[Point]
                for pnt in seg:
                    point = Point()
                    if pnt:
                        point.x = pnt.X
                        point.y = pnt.Y
                        part.append(point)

                parts.append(part)

            polygon.parts = parts
            polygon.oid = shapeName.split(".")[0] + "-" + bytes(row[0])
            polygon.gravity = Point(row[2][0], row[2][1])

            polygons.append(polygon)

    # 将polygon旋转给定的角度
    for poly in polygons:
        parts = poly.parts
        gravity = poly.gravity

        for part in parts:
            for point in part:
                mu.rotateCoord(gravity, point, 30)

    # 计算出polygon的外包矩形
    for poly in polygons:
        parts = poly.parts
        # 两个顶点
        rt = Point()
        lb = Point()

        rt.x = lb.x = parts[0][0].x
        rt.y = lb.y = parts[0][0].y

        for i in range(len(parts)):
            for k in range(len(parts[i])):
                if parts[i][k].x < lb.x:
                    lb.x = parts[i][k].x
                if parts[i][k].x > rt.x:
                    rt.x = parts[i][k].x

                if parts[i][k].y < lb.y:
                    lb.y = parts[i][k].y
                if parts[i][k].y > rt.y:
                    rt.y = parts[i][k].y

        envelope = Envelope()
        envelope.rtPoint = rt
        envelope.lbPoint = lb
        poly.envelope = envelope

    # 根据外包矩形生成分割线
    for poly in polygons:

        rt = poly.envelope.rtPoint
        lb = poly.envelope.lbPoint

        widthSeg = (rt.x - lb.x) / N
        height = rt.y - lb.y

        dividingLines = []
        for i in range(N + 1):
            line = Line()

            line.startPoint = Point(lb.x + i * widthSeg, lb.y)
            line.endPoint = Point(lb.x + i * widthSeg, lb.y + height)

            pointList = [line.startPoint, line.endPoint]
            line.pointList = pointList

            polyline = Polyline()
            lines = [line]
            polyline.lines = lines

            polyline.oid = poly.oid + "-" + bytes(i)

            dividingLines.append(polyline)
        poly.dividingLines = dividingLines

    for poly in polygons:
        dividingLines = poly.dividingLines
        for polyline in dividingLines:
            for line in polyline.lines:
                for pnt in line.pointList:
                    mu.rotateCoord(poly.gravity, pnt, 330)

    outputFeatureClass = shapeName.split(".")[0] + "_dl.shp"
    features = []
    for poly in polygons:
        polylines = poly.dividingLines  # type: List[Polyline]
        for polyline in polylines:
            for line in polyline.lines:

                array = arcpy.Array()
                for pnt in line.pointList:
                    point = arcpy.Point()
                    point.X = pnt.x
                    point.Y = pnt.y

                    array.append(point)
                pointList = arcpy.Polyline(array)
                features.append(pointList)

     # 生成要素类
    arcpy.CopyFeatures_management(features, outputFeatureClass)

    return polygons
