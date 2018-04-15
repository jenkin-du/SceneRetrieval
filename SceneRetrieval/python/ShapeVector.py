# -*- coding:utf-8 -*-

"""

    该程序获得面状要素的形状矢量
"""
import arcpy
import numpy as np

from model.Polygon import *
from model.Polyline import *
from model.Constant import *

'''
    计算面状要素的形状特征矢量
'''

# 定义面状要素被分割的段数
N = segment


def getVector(workspace, shapeName):
    """

    :rtype: List[Polygon]
    """
    # 多边形列表

    # 设置工作空间
    arcpy.env.workspace = workspace
    arcpy.env.overwriteOutput = True
    # 设置没内存工作空间
    memoryWorkspace = "in_memory\\"

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
                part.pop()
                parts.append(part)

            polygon.partList = parts
            polygon.oid = shapeName.split(".")[0] + "_" + bytes(row[0])
            polygon.gravity = Point(row[2][0], row[2][1])

            polygonList.append(polygon)

        del cursor

    '''
        计算polygon的形状矢量
    '''
    for polygon in polygonList:

        """
            计算polygon的主方向角度，并旋转
        """
        parts = polygon.partList
        gravity = polygon.gravity

        polygon.vectorList = []
        # 计算polygon的主方向
        radList = mu.getMainDirection(polygon)
        for rad in radList:
            # todo
            for part in parts:
                for point in part:
                    mu.rotateCoord(gravity, point, rad)

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

            #  生成重心分割线

            gl = Line()
            gl.startPoint = Point(gravity.x, lb.y)
            gl.endPoint = Point(gravity.x, rt.y)

            mu.rotateCoord(gravity, gl.startPoint, 2 * np.pi - rad)
            mu.rotateCoord(gravity, gl.endPoint, 2 * np.pi - rad)

            gravityLine = Polyline()
            glines = [gl]
            gravityLine.lines = glines
            gravityLine.oid = polygon.oid + "_gl"

            """
                 旋转回主方向
            """
            for pl in dlList:
                for line in pl.lines:
                    for pnt in line.pointList:
                        mu.rotateCoord(gravity, pnt, 2 * np.pi - rad)

            """
                      生成分割线要素
                """
            inFeatures = []
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
                value = [gravityLine.oid]

                array = arcpy.Array()
                sp = arcpy.Point()
                sp.X = gravityLine.lines[0].startPoint.x
                sp.Y = gravityLine.lines[0].startPoint.y
                array.append(sp)

                ep = arcpy.Point()
                ep.X = gravityLine.lines[0].endPoint.x
                ep.Y = gravityLine.lines[0].endPoint.y
                array.append(ep)

                glPolyline = arcpy.Polyline(array)
                value.append(glPolyline)

                cursor.insertRow(value)

                del cursor

            '''
                相交
            '''
            inFeatures = [shapeName, dlOutFeature]
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
            for polyline in dlList:
                polyline.lines = []
            gravityLine.lines = []

            # 根据line_id将line放在对应的polyline中
            for line in lines:
                oid = line.oid
                if oid.__contains__("_dl_"):
                    i = int(oid.split("_")[-1])
                    dlList[i].lines.append(line)
                elif oid.__contains__("_gl"):
                    gravityLine.lines.append(line)

            '''
                删除中间结果
            '''
            arcpy.Delete_management(dlOutFeature + ".shp")
            arcpy.Delete_management(inOutFeature)
            arcpy.Delete_management(spOutFeature)

            """
                根据分割线段积分生成形状矢量
            """

            vector = [0 for m in range(N - 1)]  # 形状矢量
            for i in range(len(dlList)):
                lines = dlList[i].lines  # type Line
                if len(lines) == 1:
                    vector[i] = np.square(lines[0].length) / 2.0
                elif len(lines) > 1:
                    for k in range(len(lines)):
                        for t in range(k + 1, len(lines)):
                            vector[i] += lines[k].length * lines[t].length

            # 生成主方向的顺序描述量
            mainVector = 0
            glines = gravityLine.lines
            if len(glines) == 1:
                mainVector = np.square(glines[0].length) / 2.0
            else:
                for k in range(len(glines)):
                    for t in range(k + 1, len(glines)):
                        mainVector += glines[k].length * glines[t].length

            # 将形状矢量平均
            if mainVector != 0:
                for i in range(len(vector)):
                    vector[i] /= mainVector

            polygon.vectorList.append(vector)

    return polygonList
