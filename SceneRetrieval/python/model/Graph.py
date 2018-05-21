# -*- coding:utf-8 -*-

"""
    图
"""

import tool.MathUtil as mu
from model.Constant import scene_precision
from model.Node import Node
from model.SimilarScene import *


class Graph(object):
    # id
    id = ""

    # 节点集合
    nodesList = []  # type: list[list[Node]]

    def __init__(self, incidentPairList, num):
        #
        for i in range(num):
            nodes = []
            self.nodesList.append(nodes)

        # 添加节点
        for incidentPair in incidentPairList:
            #
            fo_id = incidentPair.firstNode.oid
            fd_id = incidentPair.firstNode.did

            index = int(fo_id.split('_')[1])
            node = Node()
            node.id = fd_id
            if not mu.contains(node, self.nodesList[index]):
                self.nodesList[index].append(node)

            #
            lo_id = incidentPair.lastNode.oid
            ld_id = incidentPair.lastNode.did

            index = int(lo_id.split('_')[1])
            node = Node()
            node.id = ld_id
            if not mu.contains(node, self.nodesList[index]):
                self.nodesList[index].append(node)

        # 声明边
        for incidentPair in incidentPairList:

            fo_id = incidentPair.firstNode.oid
            index_f = int(fo_id.split('_')[1])

            lo_id = incidentPair.lastNode.oid
            index_l = int(lo_id.split('_')[1])

            if index_f - index_l == -1:

                nodes = self.nodesList[index_f]  # type: list[Node]
                for node in nodes:
                    node.edges = [0 for x in range(len(self.nodesList[index_l]))]

        # 添加边
        for incidentPair in incidentPairList:

            fo_id = incidentPair.firstNode.oid
            fd_id = incidentPair.firstNode.did
            index_fo = int(fo_id.split('_')[1])

            lo_id = incidentPair.lastNode.oid
            ld_id = incidentPair.lastNode.did
            index_lo = int(lo_id.split('_')[1])

            if index_fo - index_lo == -1:
                firstNodes = self.nodesList[index_fo]
                lastNodes = self.nodesList[index_lo]

                index_fd = -1
                for i in range(len(firstNodes)):
                    if firstNodes[i].id == fd_id:
                        index_fd = i

                index_ld = -1
                for i in range(len(lastNodes)):
                    if lastNodes[i].id == ld_id:
                        index_ld = i

                self.nodesList[index_fo][index_fd].edges[index_ld] = incidentPair.correlation

        for nodes in self.nodesList:
            for node in nodes:
                print("id:" + node.id),
            print("")
            for node in nodes:
                for edge in node.edges:
                    print(edge),
            print("")

    '''
        寻找相似场景
    '''

    @property
    def findScene(self):

        similarSceneList = []  # type:list[SimilarScene]

        firstNodes = self.nodesList[0]
        for node in firstNodes:

            polygonList = [node.id]
            mdList = []

            k = 1
            while k < len(self.nodesList):

                md = node.edges[0]
                index = 0
                for i in range(len(node.edges)):
                    if node.edges[i] > md:
                        index = i
                        md = node.edges[i]

                nextNode = self.nodesList[k][index]
                polygonList.append(nextNode.id)
                mdList.append(md)

                node = nextNode
                k += 1

            similarScene = SimilarScene()
            similarScene.polygonList = polygonList
            for md in mdList:  # type: list[float]
                similarScene.md += md / len(mdList)

            if similarScene.md > scene_precision:
                similarSceneList.append(similarScene)

        return similarSceneList
