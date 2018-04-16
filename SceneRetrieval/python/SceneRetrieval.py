# -*- coding:utf-8 -*-
"""

    检索场景要素
"""
import arcpy

from tool import ShapeUtil as su
from model.Constant import *
from model.Programme import *
from model.MatchedPolygon import *

if __name__ == '__main__':

    pro = Programme()
    pro.start()
    # 搜索的场景图层
    scenePolygons = su.getPointList(dataPath + "scene\\", "scene.shp")

    # 匹配的结果列表
    mpList = []  # type:list[mp] #已匹配的矩形
    # 搜索数据目录下的矢量数据
    workPath = dataPath
    files = os.listdir(workPath)
    for f in files:
        fp = os.path.join(workPath, f)

        if os.path.isfile(fp) and len(f.split(".")) == 2 and f.split(".")[1] == "shp":

            desc = arcpy.Describe(fp)
            if desc.shapeType == 'Polygon':

                polygons = su.getPointList(workPath, f)  # type: list[Polygon]
                for sp in scenePolygons:
                    for rp in polygons:

                        md, scale = su.matchPolygon(sp, rp)
                        if md > precision:
                            mp = MatchedPolygon()
                            mp.sourcePolygon = sp
                            mp.retrievalPolygon = rp
                            mp.scale = scale
                            mp.matchingDegree = md
                            mpList.append(mp)

    for mp in mpList:
        print(" sp:"),
        print(mp.sourcePolygon.oid),
        print(" rp:"),
        print(mp.retrievalPolygon.oid),
        print(" md:"),
        print(mp.matchingDegree),
        print(" scale:"),
        print(mp.scale)
    pro.stop()
