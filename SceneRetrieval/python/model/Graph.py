# -*- coding:utf-8 -*-

"""
    图
"""

from Node import *
import tool.MathUtil as mu
from model.Node import Node


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
            foid = incidentPair.firstNode.oid
            fdid = incidentPair.firstNode.did

            index = int(foid.split('_')[1])
            node = Node()
            node.id = fdid
            if not mu.contains(node, self.nodesList[index]):
                self.nodesList[index].append(node)

            #
            loid = incidentPair.lastNode.oid
            ldid = incidentPair.lastNode.did

            index = int(loid.split('_')[1])
            node = Node()
            node.id = ldid
            if not mu.contains(node, self.nodesList[index]):
                self.nodesList[index].append(node)

        # 声明边
        for incidentPair in incidentPairList:

            foid = incidentPair.firstNode.oid
            index_f = int(foid.split('_')[1])

            loid = incidentPair.lastNode.oid
            index_l = int(loid.split('_')[1])

            if index_f - index_l == -1:

                nodes = self.nodesList[index_f]  # type: list[Node]
                for node in nodes:
                    node.adges = [0 for x in range(len(self.nodesList[index_l]))]

        # 添加边
        for incidentPair in incidentPairList:

            foid = incidentPair.firstNode.oid
            fdid = incidentPair.firstNode.did
            index_fo = int(foid.split('_')[1])

            loid = incidentPair.lastNode.oid
            ldid = incidentPair.lastNode.did
            index_lo = int(loid.split('_')[1])

            if index_fo - index_lo == -1:
                firstNodes = self.nodesList[index_fo]
                lastNodes = self.nodesList[index_lo]

                index_fd = -1
                for i in range(len(firstNodes)):
                    if firstNodes[i].id == fdid:
                        index_fd = i

                index_ld = -1
                for i in range(len(lastNodes)):
                    if lastNodes[i].id == ldid:
                        index_ld = i

                self.nodesList[index_fo][index_fd].adges[index_ld] = incidentPair.correlation

        # for nodes in self.nodesList:
        #     for node in nodes:
        #         print("id:" + node.id),
        #     print("")
        #     for node in nodes:
        #         for edge in node.adges:
        #             print(edge),
        #     print("")
