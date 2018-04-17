# -*- coding:utf-8 -*-

from model.Polygon import *
from model.RelationPair import *

'''
    场景类
'''


class Scene(object):
    # 场景里的多边形列表
    polygonList = []  # type:list[Polygon]

    # 多边形的关系列表
    _RelationPairList = []  # type:list[RelationPair]

    # 计算场景polygon之间的关系
    def makeRelationPair(self):

        if len(self._RelationPairList) == 0:
            for i in range(len(self.polygonList) - 1):
                for j in range(i + 1, len(self.polygonList)):
                    pa = self.polygonList[i]
                    pb = self.polygonList[j]

                    pr = RelationPair(pa, pb)
                    self._RelationPairList.append(pr)
        return self._RelationPairList
