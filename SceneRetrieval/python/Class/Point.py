# -*- coding:utf-8 -*-

# 坐标类

class Point(object):
    # 成员变量
    x = 0
    y = 0

    # 构造函数
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def __str__(self):
        return "x:" + bytes(self.x) + ", y:" + bytes(self.y)
