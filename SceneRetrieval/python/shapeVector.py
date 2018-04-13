# -*- coding:utf-8 -*-

"""

    该程序获得面状要素的形状矢量
"""
import sys
import arcpy
import time
import sympy as sym
import numpy as np

from model.Polygon import *
from model.Polyline import *
import tool.util as util
import tool.mathUtil as mu

st = time.time()
st = int(round(st * 1000))

# 面状矢量的名字
# shapeName = sys.argv[1]
shapeName = "polygon.shp"
# 定义面状要素被分割的段数
N = 10

# 设置工作空间
arcpy.env.workspace = util.dataPath
arcpy.env.overwriteOutput = True

# 多边形列表
polygonList = []

with arcpy.da.SearchCursor(shapeName, ["OID@", "SHAPE@", "SHAPE@XY"]) as cursor:
    for row in cursor:

        polygon = Polygon()
        parts = []

        for seg in row[1]:
            part = []
            for pnt in seg:
                point = Point()
                if pnt:
                    point.x = pnt.X
                    point.y = pnt.Y
                    part.append(point)

            parts.append(part)

        polygon.partList = parts
        polygon.oid = shapeName.split(".")[0] + "_" + bytes(row[0])
        polygon.gravity = Point(row[2][0], row[2][1])

        polygonList.append(polygon)

# f = open(util.tempPath + "data.cp", 'w')

for polygon in polygonList:

    """
        将polygon旋转给定的角度
    """
    parts = polygon.partList
    gravity = polygon.gravity

    for part in parts:
        for point in part:
            # TODO 旋转主方向角度
            mu.rotateCoord(gravity, point, 30)

    """
        计算出polygon的外包矩形
    """
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
    polygon.envelope = envelope

    """
        根据外包矩形生成分割线
    """
    widthSeg = (rt.x - lb.x) / N
    dividingLines = []
    for i in range(N + 1):
        line = Line()

        line.startPoint = Point(lb.x + i * widthSeg, lb.y)
        line.endPoint = Point(lb.x + i * widthSeg, rt.y)

        pointList = [line.startPoint, line.endPoint]
        line.pointList = pointList

        pl = Polyline()
        lines = [line]
        pl.lines = lines

        pl.oid = polygon.oid + "-" + bytes(i)

        dividingLines.append(pl)
    polygon.dlList = dividingLines

    """
        生成重心分割线
    """
    gl = Line()
    gl.startPoint = Point(gravity.x, lb.y)
    gl.endPoint = Point(gravity.x, rt.y)
    # todo 旋转回主方向
    mu.rotateCoord(gravity, gl.startPoint, 330)
    mu.rotateCoord(gravity, gl.endPoint, 330)

    gpl = Polyline()
    glines = [gl]
    gpl.lines = glines
    gpl.oid = polygon.oid + "_gl"

    polygon.gravityLine = gpl

    """
         旋转回主方向
    """
    dividingLines = polygon.dlList
    for pl in dividingLines:
        for line in pl.lines:
            for pnt in line.pointList:
                # TODO 旋转回主方向
                mu.rotateCoord(gravity, pnt, 330)

    """
        生成分割线要素
    """
    outputFeatureClass = polygon.oid + "_dl.shp"
    features = []

    polylines = polygon.dlList
    for pl in polylines:
        for line in pl.lines:

            array = arcpy.Array()
            for pnt in line.pointList:
                point = arcpy.Point()
                point.X = pnt.x
                point.Y = pnt.y

                array.append(point)
            polyline = arcpy.Polyline(array)
            features.append(polyline)

    # 生成要素类
    arcpy.CopyFeatures_management(features, outputFeatureClass)

    # 生成重心分割要素
    glOutFeature = polygon.gravityLine.oid + ".shp"
    glFeatures = []
    array = arcpy.Array()
    sp = arcpy.Point()
    sp.X = gpl.lines[0].startPoint.x
    sp.Y = gpl.lines[0].startPoint.y
    array.append(sp)

    ep = arcpy.Point()
    ep.X = gpl.lines[0].endPoint.x
    ep.Y = gpl.lines[0].endPoint.y
    array.append(ep)
    glPolyline = arcpy.Polyline(array)
    glFeatures.append(glPolyline)
    arcpy.CopyFeatures_management(glFeatures, glOutFeature)

    """
         给每条线加上oid,然后取分割线和原面状要素交集
    """
    polyDLName = polygon.oid + "_dl.shp"
    arcpy.AddField_management(polyDLName, "line_id", "TEXT", "", "", 50)
    with arcpy.da.UpdateCursor(polyDLName, "line_id") as cursor:
        i = 0
        for row in cursor:
            row[0] = polyDLName.split(".")[0] + "_" + bytes(i)
            i += 1
            cursor.updateRow(row)

    # 相交
    polyFeatureName = polygon.oid.split("_")[0] + ".shp"

    inFeatures = [polyFeatureName, polyDLName]
    outFeature = polyDLName.split(".")[0] + "_in.shp"
    arcpy.Intersect_analysis(inFeatures, outFeature)

    # 重心分割线相交
    glInFeature = polygon.gravityLine.oid + ".shp"
    glInFeatures=[glInFeature,polyFeatureName]
    outFeature = polygon.gravityLine.oid + "_in.shp"
    arcpy.Intersect_analysis(glInFeatures, outFeature)

    # 删除 poly.oid + "_dl.shp"
    arcpy.Delete_management(polyDLName)
    arcpy.Delete_management(glInFeature)

    """
        分割生成的分割线
    """
    inFeature = polygon.oid + "_dl_in.shp"
    outFeature = polygon.oid + "_dl_sp.shp"
    arcpy.SplitLine_management(inFeature, outFeature)

    # 删除 poly.oid + "_dl_in.shp"
    arcpy.Delete_management(inFeature)

    # 分割生成的重心分割线
    glInFeature = polygon.gravityLine.oid + "_in.shp"
    glOutFeature = polygon.gravityLine.oid + "_sp.shp"
    arcpy.SplitLine_management(glInFeature, glOutFeature)

    # 删除 poly.gravityLine.oid + "_in.shp"
    arcpy.Delete_management(glInFeature)

    """
        将分割线加入到polygon中
    """
    lines = []  # type: List[Line]
    with arcpy.da.SearchCursor(outFeature, ["line_id", "SHAPE@"]) as cursor:
        for row in cursor:
            line = Line()

            line.oid = row[0]
            line.startPoint = Point(row[1].firstPoint.X, row[1].firstPoint.Y)
            line.endPoint = Point(row[1].lastPoint.X, row[1].lastPoint.Y)
            line.length = row[1].length
            lines.append(line)

    # 根据line_id将line放在对应的polyline中
    dLines = []  # type: List[Polyline]

    for i in range(1, N):
        pl = Polyline()
        pl.oid = polygon.oid + "_" + bytes(i)
        ls = []  # type: List[Line]
        for line in lines:
            lineIndex = int(line.oid.split("_")[-1])
            if lineIndex == i:
                ls.append(line)
        pl.lines = ls
        dLines.append(pl)

    polygon.dlList = dLines

    # 将主分割线加入到polygon中
    glspFeature = polygon.gravityLine.oid + "_sp.shp"
    glines = []  # type: List[Line]
    with arcpy.da.SearchCursor(glspFeature, "SHAPE@") as cursor:
        for row in cursor:
            line = Line()

            line.startPoint = Point(row[0].firstPoint.X, row[0].firstPoint.Y)
            line.endPoint = Point(row[0].lastPoint.X, row[0].lastPoint.Y)

            line.length = row[0].length
            glines.append(line)

    polygon.gravityLine.lines = glines


    # 删除 poly.oid + "_dl_sp.shp"
    arcpy.Delete_management(outFeature)
    arcpy.Delete_management(glspFeature)


    """
        根据分割线段积分生成形状矢量
    """
    vector = [0 for i in range(N - 1)]  # 形状矢量
    dlList = polygon.dlList
    for i in range(len(dlList)):
        lines = dlList[i].lines  # type Line
        if len(lines) == 1:
            vector[i] = np.square(lines[0].length) / 2.0
        else:
            for k in range(len(lines)):
                for t in range(k + 1, len(lines)):
                    vector[i] += lines[k].length * lines[t].length
    polygon.vector = vector

    # 生成主方向的顺序描述量
    glines = polygon.gravityLine.lines
    if len(glines) == 1:
        polygon.mainVector = np.square(glines[0].length) / 2.0
    else:
        for k in range(len(glines)):
            for t in range(k + 1, len(glines)):
                polygon.mainVector += glines[k].length * glines[t].length

    # 将形状矢量平均
    if polygon.mainVector != 0:
        for i in range(len(vector)):
             polygon.vector[i] /= polygon.mainVector

print("executed sucessfully!")

et = time.time()
et = int(round(et * 1000))
dt = et - st
dt = dt / 1000.0

print("executed time:"),
print(bytes(dt))
