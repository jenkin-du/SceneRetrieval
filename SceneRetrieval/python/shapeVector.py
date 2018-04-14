# -*- coding:utf-8 -*-

"""

    该程序获得面状要素的形状矢量
"""
import arcpy
import numpy as np

import tool.util as util
from model.Polygon import *
from model.Polyline import *
from model.Programme import *

pro = Programme()
pro.start()

# 面状矢量的名字
# shapeName = sys.argv[1]
shapeName = "polygon.shp"
# 定义面状要素被分割的段数
N = 10

# 设置工作空间
arcpy.env.workspace = util.dataPath
arcpy.env.overwriteOutput = True
# 设置没内存工作空间
memoryWorkspace = "in_memory\\"

# 多边形列表
polygonList = []  # type: List[Polygon]

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

    del cursor
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
    dlList = []
    for i in range(1, N):
        line = Line()

        line.startPoint = Point(lb.x + i * widthSeg, lb.y)
        line.endPoint = Point(lb.x + i * widthSeg, rt.y)

        pointList = [line.startPoint, line.endPoint]
        line.pointList = pointList
        line.oid = polygon.oid + "_dl_" + bytes(i - 1)

        pl = Polyline()
        pl.oid = line.oid
        lines = [line]
        pl.lines = lines

        dlList.append(pl)
    polygon.dlList = dlList

    #  生成重心分割线

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
    dlList = polygon.dlList
    for pl in dlList:
        for line in pl.lines:
            for pnt in line.pointList:
                # TODO 旋转回主方向
                mu.rotateCoord(gravity, pnt, 330)

"""
      生成分割线要素
"""
inFeatures = []
for polygon in polygonList:

    dlList = polygon.dlList
    for pl in dlList:
        for line in pl.lines:
            array = arcpy.Array()
            for pnt in line.pointList:
                point = arcpy.Point()
                point.X = pnt.x
                point.Y = pnt.y

                array.append(point)
            polyline = arcpy.Polyline(array)
            inFeatures.append(polyline)

# 创建要素
dlOutFeature = shapeName.split(".")[0] + "_dl"
spatial_ref = arcpy.Describe(shapeName).spatialReference
arcpy.CreateFeatureclass_management("in_memory", dlOutFeature, "POLYLINE", spatial_reference=spatial_ref)
# 生成要素类


"""
     给每条线加上oid,然后取分割线和原面状要素交集
"""
dlOutFeature = memoryWorkspace + dlOutFeature
arcpy.AddField_management(dlOutFeature, "line_id", "TEXT", "", "", 100)
with arcpy.da.InsertCursor(dlOutFeature, ["line_id", "SHAPE@"]) as cursor:
    for polygon in polygonList:
        dlList = polygon.dlList
        for pl in dlList:
            for line in pl.lines:
                value = [line.oid]
                array = arcpy.Array()
                for pnt in line.pointList:
                    point = arcpy.Point()
                    point.X = pnt.x
                    point.Y = pnt.y

                    array.append(point)
                polyline = arcpy.Polyline(array)
                value.append(polyline)

                cursor.insertRow(value)

        # 插入重心线
        value = [polygon.gravityLine.oid]

        array = arcpy.Array()
        sp = arcpy.Point()
        sp.X = polygon.gravityLine.lines[0].startPoint.x
        sp.Y = polygon.gravityLine.lines[0].startPoint.y
        array.append(sp)

        ep = arcpy.Point()
        ep.X = polygon.gravityLine.lines[0].endPoint.x
        ep.Y = polygon.gravityLine.lines[0].endPoint.y
        array.append(ep)

        glPolyline = arcpy.Polyline(array)
        value.append(glPolyline)

        cursor.insertRow(value)

    del cursor

'''
    相交
'''
inFeatures = [shapeName, dlOutFeature ]
inOutFeature = dlOutFeature + "_in"
arcpy.Intersect_analysis(inFeatures, inOutFeature)

'''
    分割
'''
inFeature = inOutFeature
spOutFeature = inOutFeature + "_sp"
arcpy.SplitLine_management(inFeature, spOutFeature)

'''
    合并
'''
lines = []  # type: List[Line]
with arcpy.da.SearchCursor(spOutFeature, ["line_id", "SHAPE@"]) as cursor:
    for row in cursor:
        line = Line()

        line.oid = row[0]
        line.startPoint = Point(row[1].firstPoint.X, row[1].firstPoint.Y)
        line.endPoint = Point(row[1].lastPoint.X, row[1].lastPoint.Y)
        line.length = row[1].length
        lines.append(line)

# 清空
for polygon in polygonList:
    dlList = polygon.dlList
    for polyline in dlList:
        polyline.lines = []
    polygon.gravityLine.lines = []
# 根据line_id将line放在对应的polyline中
for line in lines:
    oid = line.oid
    if oid.__contains__("_dl_"):
        k = int(oid.split("_")[-3])
        i = int(oid.split("_")[-1])
        polygonList[k].dlList[i].lines.append(line)
    elif oid.__contains__("_gl"):
        t = int(oid.split("_")[-2])
        polygonList[t].gravityLine.lines.append(line)

'''
    删除中间结果
'''
arcpy.Delete_management(dlOutFeature + ".shp")
arcpy.Delete_management(inOutFeature)
arcpy.Delete_management(spOutFeature)

"""
    根据分割线段积分生成形状矢量
"""
for polygon in polygonList:

    vector = [0 for m in range(N - 1)]  # 形状矢量
    dlList = polygon.dlList
    for i in range(len(dlList)):
        lines = dlList[i].lines  # type Line
        if len(lines) == 1:
            vector[i] = np.square(lines[0].length) / 2.0
        elif len(lines) > 1:
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

    print(polygon.mainVector)
    print("\n")
    for v in polygon.vector:
        print(v)
    print("\n")

pro.stop()
