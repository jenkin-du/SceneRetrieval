# -*- coding:utf-8 -*-

import arcpy
from model.Polygon import *

from model.Programme import *

program = Programme()
program.start()
import sympy as sym

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
from tool import util

arcpy.env.overwriteOutput = True
# 指定输出数据的路径
# outputFeatureClass = r"D:\毕设\工程\data\box.shp"
#
#


if __name__ == '__main__':
    # coordList = [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]], [[4, 4], [4, 6], [6, 6], [6, 4], [4, 4]]]
    #

    # 设置工作空间
    arcpy.env.workspace = util.dataPath
    arcpy.env.overwriteOutput = True

    # outputFeatureClass = "in_memory/box"
    # # # outputFeatureClass=arcpy.CreateScratchName(outputFeatureClass,data_type="Shapefile",workspace="in_memory")
    # coordList = [[[0, 0], [0, 100], [100, 100], [100, 0], [0, 0]], [[40, 40], [40, 60], [60, 60], [60, 40], [40, 40]]]
    # features = []
    # # 读取坐标串
    # for part in coordList:
    #     array = arcpy.Array()
    #     for coordPair in part:
    #         point = arcpy.Point()
    #         point.X = coordPair[0]
    #         point.Y = coordPair[1]
    #         array.add(point)
    #     line = arcpy.Polygon(array)
    #     features.append(line)
    # # 生成要素类
    # arcpy.CopyFeatures_management(features, outputFeatureClass)
    #
    # # 复制
    # arcpy.Copy_management(r"polygon.shp","in_memory/polygon")
    # # 相交
    # inFeatures = [outputFeatureClass, "in_memory/polygon"]
    # arcpy.Intersect_analysis(inFeatures, "in_memory/bp")
    # arcpy.Buffer_analysis("in_memory/bp", "outFeatures", 10)
    #
    # program.stop()
    array = arcpy.Array([arcpy.Point(459111.668136828221, 5010433.128536828221), arcpy.Point(472516.381836828221, 5001431.080836828221),
                         arcpy.Point(477710.818536828221, 4986587.106336828221)])
    # Create a polyline geometry
    # array = arcpy.Array([arcpy.Point(459111.6681, 5010433.1285), arcpy.Point(472516.3818, 5001431.0808),
    #                      arcpy.Point(477710.8185, 4986587.1063)])
    polyline = arcpy.Polyline(array)
    # Open an InsertCursor and insert the new geometry
    cursor = arcpy.da.InsertCursor('polyline.shp', ['NAME', 'SHAPE@'])
    value=["Anderson"]
    value.append(polyline)
    cursor.insertRow(value)
# Delete cursor object del cursor