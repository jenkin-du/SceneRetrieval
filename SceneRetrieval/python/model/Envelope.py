# -*- coding:utf-8 -*-

import arcpy

'''
    多边形的外包矩形
'''


class Envelope(object):
    xMin = 0
    xMax = 0

    yMin = 0
    yMax = 0

    def __init__(self, xMin=0, yMin=0, xMax=0, yMax=0):
        self.xMin = xMin
        self.xMax = xMax

        self.yMin = yMin
        self.yMax = yMax
