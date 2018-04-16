# -*- coding:utf-8 -*-

import os
import time

'''
    定义一些常量
'''

# 文档的相对路径
dataPath = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))) + "\\data\\"

tempPath = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))) + "\\temp\\"

# 面状要素的分割数目
segment = 10

# 单个要素匹配的精度
precision = 0.75
