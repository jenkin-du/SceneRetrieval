# -*- coding:utf-8 -*-
"""

    检索场景要素
"""
import os
import arcpy

import ShapeVector as SV
from model.Constant import *
from model.Layer import *
from model.Programme import *

if __name__ == '__main__':

    pro = Programme()
    pro.start()
    # 搜索的场景图层
    sceneLayer = Layer
    sceneLayer.name = "scene.shp"
    sceneLayer.polygons = SV.getVector(dataPath + "scene\\", sceneLayer.name)

    # 待搜索的数据
    layerList = []
    # 匹配的结果列表
    matchedPolygonList = []  # type:list[list[Polygon]] #已匹配的矩形
    # 搜索数据目录下的矢量数据
    workPath = dataPath
    files = os.listdir(workPath)
    for f in files:
        fp = os.path.join(workPath, f)

        layer = Layer
        layer.name = f

        if os.path.isfile(fp) and len(f.split(".")) == 2 and f.split(".")[1] == "shp":
            desc = arcpy.Describe(fp)
            if desc.shapeType == 'Polygon':
                polygons = SV.getVector(workPath, f)  # type: list[Polygon]
                matchedPolygon = []
                for sp in sceneLayer.polygons:
                    matchedPolygon.append(sp)
                    for rp in polygons:
                        # if rp.diff > 0.1:
                        #     # 计算匹配度
                        #     md = mu.matchVector(sp.vector, rp.vector)
                        #     if md >= precision:
                        #         matchedPolygon.append(rp)
                        #         print("sp :" + sp.oid + " "),
                        #         print("rp :" + rp.oid + " "),
                        #         print("   md:" + str(md))
                        # elif rp.diff < 0.1 and sp.diff < 0.1:
                            md = mu.matchPolygon(sp, rp)
                        #     if md >= precision:
                        #     matchedPolygon.append(rp)
                            print("sp :" + sp.oid + " "),
                            print("rp :" + rp.oid + " "),
                            print("   md:" + str(md))

                matchedPolygonList.append(matchedPolygon)
    pro.stop()
