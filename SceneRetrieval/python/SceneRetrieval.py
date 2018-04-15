# -*- coding:utf-8 -*-
"""

    检索场景要素
"""
import os
import arcpy

import ShapeVector as sv
import tool.MathUtil as mu
from model.Constant import *
from model.Layer import *
from model.Programme import *

if __name__ == '__main__':

    pro = Programme()
    pro.start()
    # 搜索的场景图层
    sceneLayer = Layer
    sceneLayer.name = "scene.shp"
    sceneLayer.polygons = sv.getVector(dataPath + "\\scene\\", sceneLayer.name)

    # 待搜索的数据
    layerList = []
    # 匹配的结果列表
    matchedLayerList = []
    # 搜索数据目录下的矢量数据
    files = os.listdir(dataPath)
    for f in files:
        fp = os.path.join(dataPath, f)

        layer = Layer
        layer.name = f
        matchedPolygons = []
        if os.path.isfile(fp) and len(f.split(".")) == 2 and f.split(".")[1] == "shp":
            desc = arcpy.Describe(fp)
            if desc.shapeType == 'Polygon':
                polygons = sv.getVector(dataPath, f)  # type: list[Polygon]

                for sp in sceneLayer.polygons:
                    for p in polygons:
                        # 计算匹配读
                        sv = sp.vectorList[0]
                        pvList = p.vectorList
                        for pv in pvList:
                            md = mu.matchVector(sv, pv)
                            print("sp :" + sp.oid + " "),
                            print("rp :" + p.oid + " "),
                            print("   md:" + str(md))

    pro.stop()
