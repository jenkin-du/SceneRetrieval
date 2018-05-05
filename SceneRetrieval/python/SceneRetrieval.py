# -*- coding:utf-8 -*-
"""

    检索场景要素
"""

from model.Time import *

t = Time("analysis")
t.start()
import numpy as np
import json

from tool import ShapeUtil as su
from model.Constant import *
from model.Programme import *
from model.MatchedPolygon import *
from model.Scene import *
from model.SimilarScene import *
from model.IncidentPair import IncidentPair, IncidentNode

t.stop()

if __name__ == '__main__':

    pro = Programme()
    pro.start()
    # 搜索的场景图层
    scenePolygons = su.getPolygonList(dataPath + "scene\\", "scene.shp")

    # 获得归一化的坐标和外包矩形
    for op in scenePolygons:
        op.uniformedPartList = mu.polygonUniformization(op)
        op.uniformedEnvelope = mu.uniformedEnvelope(op.uniformedPartList)

    originScene = Scene()
    originScene.polygonList = scenePolygons
    originRelationPairList = originScene.makeRelationPair()  # 原图形的关系列表

    for pair in originRelationPairList:
        print(pair)

    # 匹配的结果列表
    mpList = []  # type:list[MatchedPolygon] #已匹配的矩形
    # 搜索数据目录下的矢量数据
    workPath = dataPath
    files = os.listdir(workPath)

    for op in scenePolygons:
        mp = MatchedPolygon()
        mp.origin = op

        matchingList = []
        matchingDegreeList = []
        scaleList = []

        for f in files:
            fp = os.path.join(workPath, f)
            if os.path.isfile(fp) and len(f.split(".")) == 2 and f.split(".")[1] == "shp":
                desc = arcpy.Describe(fp)
                if desc.shapeType == 'Polygon':

                    polygons = su.getPolygonList(workPath, f)  # type: list[Polygon]

                    for dp in polygons:

                        md, scale = su.matchPolygon(op, dp)
                        if md > polygon_precision:
                            matchingList.append(dp)
                            scaleList.append(scale)
                            matchingDegreeList.append(md)

        mp.matchingList = matchingList
        mp.mdList = matchingDegreeList
        mp.scaleList = scaleList

        mpList.append(mp)


    # 关联对列表
    incidentPairList = []  # type:list[IncidentPair]
    for opr in originRelationPairList:

        indexF = su.indexOfMatched(mpList, opr.firstPolygon)
        indexL = su.indexOfMatched(mpList, opr.lastPolygon)
        fmpList = mpList[indexF].matchingList
        lmpList = mpList[indexL].matchingList

        dmpListF = mpList[indexF].mdList
        dmpListL = mpList[indexL].mdList

        scaleListF = mpList[indexF].scaleList
        scaleListL = mpList[indexL].scaleList



        for i in range(len(fmpList)):
            for j in range(len(lmpList)):

                fp = fmpList[i]
                lp = lmpList[j]
                pr = RelationPair(fp, lp)


                # 方向角的差异度
                da = np.abs(opr.getAzimuth() - pr.getAzimuth()) / (opr.getAzimuth() + pr.getAzimuth())
                # 重心距离的差异
                # 考虑缩放相似性
                fs = scaleListF[i]
                ls = scaleListL[j]
                dsc = np.abs(fs - ls)
                av_sc = 1
                if dsc < 0.7:
                    av_sc = (fs + ls) / 2
                dg = np.abs(opr.getGravityDistance() - pr.getGravityDistance() * av_sc) / (
                        opr.getGravityDistance() + pr.getGravityDistance() * av_sc)

                # 总体差异度
                md = 0
                if da != 0 and dg != 0:
                    md = (1 / dg * (1 - da) + 1 / da * (1 - dg)) / (1 / da + 1 / dg)
                if da == 0 and dg == 0:
                    md = 1
                if da == 0:
                    md = 1 - dg
                if dg == 0:
                    md = 1 - da

                # 将形状差异度也加权到最终的结果中
                fms = dmpListF[i]
                lms = dmpListL[j]



                if lms != 1 and fms != 1:
                    ams = (1 / (1 - lms) * fms + 1 / (1 - fms) * lms) / (1 / (1 - lms) + 1 / (1 - fms))
                else:
                    ams = (lms + fms) / 2

                ds = 1 - ams
                dv = 1 - md
                if ds != 0 and dv != 0:
                    md = (1 / ds * (1 - dv) + 1 / dv * (1 - ds)) / (1 / dv + 1 / ds)

                if md > scene_precision:

                    pr.md = md

                    incidentPair = IncidentPair()

                    firstNode = IncidentNode()
                    lastNode = IncidentNode()
                    firstNode.oid = opr.firstPolygon.oid
                    lastNode.oid = opr.lastPolygon.oid

                    firstNode.did = fp.oid
                    lastNode.did = lp.oid

                    firstNode.md = fms
                    lastNode.md = lms

                    incidentPair.firstNode = firstNode
                    incidentPair.lastNode = lastNode

                    incidentPair.correlation = md
                    incidentPairList.append(incidentPair)

    # 序列化
    fp = open(tempPath + "data", 'w')
    json.dump(incidentPairList, fp, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    fp.close()
    pro.stop()
