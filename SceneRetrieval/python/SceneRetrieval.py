# -*- coding:utf-8 -*-
"""

    检索场景要素
"""
import arcpy
import numpy as np
import json

from tool import ShapeUtil as su
from model.Constant import *
from model.Programme import *
from model.MatchedPolygon import *
from model.Scene import *
from model.SimilarScene import *

if __name__ == '__main__':

    pro = Programme()
    pro.start()
    # 搜索的场景图层
    scenePolygons = su.getPointList(dataPath + "scene\\", "scene.shp")

    originScene = Scene()
    originScene.polygonList = scenePolygons
    originRelationPairList = originScene.makeRelationPair()  # 原图形的关系列表

    # 匹配的结果列表
    mpList = []  # type:list[MatchedPolygon] #已匹配的矩形
    # 搜索数据目录下的矢量数据
    workPath = dataPath
    files = os.listdir(workPath)

    for sp in scenePolygons:
        mp = MatchedPolygon()
        mp.origin = sp

        matchingList = []
        matchingDegreeList = []
        scaleList = []

        for f in files:
            fp = os.path.join(workPath, f)
            if os.path.isfile(fp) and len(f.split(".")) == 2 and f.split(".")[1] == "shp":
                desc = arcpy.Describe(fp)
                if desc.shapeType == 'Polygon':

                    polygons = su.getPointList(workPath, f)  # type: list[Polygon]

                    for rp in polygons:

                        md, scale = su.matchPolygon(sp, rp)
                        if md > precision:
                            matchingList.append(rp)
                            scaleList.append(scale)
                            matchingDegreeList.append(md)

        mp.matchingList = matchingList
        mp.mdList = matchingDegreeList
        mp.scaleList = scaleList

        mpList.append(mp)

    # 关联对列表
    relationPairList = []  # type:list[RelationPair]
    # 从场景中的关联对中找出与之匹配度高的关联对
    for opr in originRelationPairList:

        indexA = su.indexOfMatched(mpList, opr.firstPolygon)
        indexB = su.indexOfMatched(mpList, opr.lastPolygon)
        ampList = mpList[indexA].matchingList
        bmpList = mpList[indexB].matchingList

        dmpListA = mpList[indexA].mdList
        dmpListB = mpList[indexB].mdList

        scaleListA = mpList[indexA].scaleList
        scaleListB = mpList[indexB].scaleList

        for i in range(len(ampList)):
            for j in range(len(bmpList)):

                fp = ampList[i]
                lp = bmpList[j]
                pr = RelationPair(fp, lp)

                # 方向角的差异度
                da = np.abs(opr.getAzimuth() - pr.getAzimuth()) / (opr.getAzimuth() + pr.getAzimuth())
                # 重心距离的差异
                # 考虑缩放相似性
                fs = scaleListA[i]
                ls = scaleListB[j]
                dsc = np.abs(fs - ls)
                av_sc = 1
                if dsc < 0.1:
                    av_sc = (fs + ls) / 2
                dg = np.abs(opr.getGravityDistance() * av_sc - pr.getGravityDistance()) / (
                        opr.getGravityDistance() * av_sc + pr.getGravityDistance())

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
                fms = dmpListA[i]
                lms = dmpListB[j]
                if lms != 1 and fms != 1:
                    ams = (1 / (1 - lms) * fms + 1 / (1 - fms) * lms) / (1 / (1 - lms) + 1 / (1 - fms))
                else:
                    ams = (lms + fms) / 2

                ds = 1 - ams
                dv = 1 - md
                if ds != 0 and dv != 0:
                    md = (1 / ds * (1 - dv) + 1 / dv * (1 - ds)) / (1 / dv + 1 / ds)

                if md > precision:
                    pr.md = md
                    # 将生成的关联对加入到中的列表里
                    relationPairList.append(pr)

    similarSceneList = []  # type:list[SimilarScene]
    for pr in relationPairList:
        fp = pr.firstPolygon
        lp = pr.lastPolygon

        scene = SimilarScene()
        plist = [fp.oid, lp.oid]  # type:list[str]

        scene.polygonList = plist
        scene.md = pr.md

        envelopeList = [fp.envelope, lp.envelope]
        scene.gravity, scene.envelope = mu.getEnvelopeGravity(envelopeList)

        similarSceneList.append(scene)
    # 序列化
    fp = open(tempPath + "data", 'w')
    json.dump(similarSceneList, fp, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    fp.close()
    pro.stop()
