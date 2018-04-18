# -*- coding:utf-8 -*-
from model.Envelope import Envelope, Point


class SimilarScene(object):
    # 找到的相似场景中的polygon的id
    polygonList = []  # type:list[str]

    # 相似度
    md = 0

    # 外包矩形
    envelope = Envelope()

    # 重心坐标
    gravity = Point()
