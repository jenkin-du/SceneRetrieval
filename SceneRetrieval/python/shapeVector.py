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
from Class.Line import *

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

    polygons = []
    # 获取polygon的信息
    with arcpy.da.SearchCursor(shapeName, ["OID@", "SHAPE@", "SHAPE@XY"]) as cursor:
        for row in cursor:

            polygon = Polygon()
            parts = []

            for seg in row[1]:
                part = []
                for pnt in seg:
                    if pnt:
                        part.append(pnt)

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

        poly.envelope.lbPoint = lb
        poly.envelope.rtPoint = rt

    # 根据外包矩形生成分割线
    for poly in polygons:
        rt = poly.envelope.rtPoint
        lb = poly.envelope.lbPoint

        ltx = lb.x
        lty = rt.y
        rtx = rt.x
        rty = rt.y
        lbx = lb.x
        lby = lb.y
        rbx = rt.x
        rby = lb.y

        widthSeg = (rtx - ltx) / N
        height = lty - lby

        dividingLines = []
        for i in range(N):
            lineSeg = LineSegment()

            lineSeg.startPoint = Point(lbx + i * widthSeg, lby)
            lineSeg.endPoint = Point(lbx + i * widthSeg, lby + height)

            lineSeg.pointList.append(lineSeg.startPoint)
            lineSeg.pointList.append(lineSeg.endPoint)

            line = Line()
            line.segments.append(lineSeg)

            dividingLines.append(line)
        poly.dividingLines = dividingLines

    return polygons


print(Path)
