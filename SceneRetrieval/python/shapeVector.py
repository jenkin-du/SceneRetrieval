# -*- coding:utf-8 -*-

"""

    该程序获得面状要素的形状矢量
"""
import sys
import arcpy

from model.Polygon import *
from model.Polyline import *
import tool.util as util
import tool.mathUtil as mu

# 面状矢量的名字
shapeName = sys.argv[1]
# shapeName = "polygon.shp"
# 定义面状要素被分割的段数
N = 10


# 设置工作空间
arcpy.env.workspace = util.dataPath
arcpy.env.overwriteOutput = True

#多边形列表
polygons = []

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

        polygon.parts = parts
        polygon.oid = shapeName.split(".")[0] + "_" + bytes(row[0])
        polygon.gravity = Point(row[2][0], row[2][1])

        polygons.append(polygon)

# 将polygon旋转给定的角度
for poly in polygons:
    parts = poly.parts
    gravity = poly.gravity

    for part in parts:
        for point in part:
            # TODO 旋转主方向角度
            mu.rotateCoord(gravity, point, 30)

f = open(util.tempPath + "data.cp", 'w')

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
    widthSeg = (rt.x - lb.x) / N
    height = rt.y - lb.y

    dividingLines = []
    for i in range(N + 1):
        line = Line()

        line.startPoint = Point(lb.x + i * widthSeg, lb.y)
        line.endPoint = Point(lb.x + i * widthSeg, lb.y + height)

        pointList = [line.startPoint, line.endPoint]
        line.pointList = pointList

        pl = Polyline()
        lines = [line]
        pl.lines = lines

        pl.oid = poly.oid + "-" + bytes(i)

        dividingLines.append(pl)
    poly.dLines = dividingLines

    dividingLines = poly.dLines
    for pl in dividingLines:
        for line in pl.lines:
            for pnt in line.pointList:
                # TODO 旋转回主方向
                mu.rotateCoord(poly.gravity, pnt, 330)

    # 生成分割线要素
    outputFeatureClass = poly.oid + "_dl.shp"
    features = []

    polylines = poly.dLines
    for pl in polylines:
        for line in pl.lines:

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

    # 给每条线加上oid
    polyDLName = poly.oid + "_dl.shp"
    arcpy.AddField_management(polyDLName, "line_id", "TEXT", "", "", 50)
    with arcpy.da.UpdateCursor(polyDLName, "line_id") as cursor:
        i = 0
        for row in cursor:
            row[0] = polyDLName.split(".")[0] + "_" + bytes(i)
            i += 1
            cursor.updateRow(row)

    # 相交
    polyFeatureName = poly.oid.split("_")[0] + ".shp"

    inFeatures = [polyFeatureName, polyDLName]
    outFeature = polyDLName.split(".")[0] + "_in.shp"

    arcpy.Intersect_analysis(inFeatures, outFeature)

    # 删除 poly.oid + "_dl.shp"
    arcpy.Delete_management(polyDLName)

    # 分割生成的分割线
    inFeature = poly.oid + "_dl_in.shp"
    outFeature = poly.oid + "_dl_sp.shp"
    arcpy.SplitLine_management(inFeature, outFeature)

    # 删除 poly.oid + "_dl_in.shp"
    arcpy.Delete_management(inFeature)

    # 将分割线加入到polygon中
    lines = []  # type: List[Line]
    with arcpy.da.SearchCursor(outFeature, ["line_id", "SHAPE@"]) as cursor:
        for row in cursor:
            line = Line()

            line.oid = row[0]
            line.startPoint = Point(row[1].firstPoint.X, row[1].firstPoint.Y)
            line.endPoint = Point(row[1].lastPoint.X, row[1].lastPoint.Y)
            line.length = row[1].length
            lines.append(line)

    # # 删除 poly.oid + "_dl_sp.shp"
    # arcpy.Delete_management(outFeature)

    # 根据line_id将line放在对应的polyline中
    dLines = []  # type: List[Polyline]

    for i in range(1, N):
        pl = Polyline()
        pl.oid = poly.oid + "_" + bytes(i)
        ls = []  # type: List[Line]
        for line in lines:
            lineIndex = int(line.oid.split("_")[-1])
            if lineIndex == i:
                ls.append(line)
        pl.lines = ls
        dLines.append(pl)

    poly.dLines = dLines

    for dl in dLines:
        f.write(dl.oid + ":")
        f.write("\n")
        lines = dl.lines
        for line in lines:
            f.write("    " + line.oid + " ,")
            f.write("sp: ")
            f.write(line.startPoint.__str__())
            f.write("ep: "),
            f.write(line.endPoint.__str__())
            f.write("\n")

f.close()
    # TODO 根据分割线段积分生成形状矢量

print("executed sucessfully!")
