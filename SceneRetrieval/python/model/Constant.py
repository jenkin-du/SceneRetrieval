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

# 单个要素匹配的精度
polygon_precision = 0.7

# 场景要素匹配的精度
scene_precision = 0.7

# 宽高比差异度
whRatioDiff = 2

# 外包矩形匹配度
envelope_precision = 0.8
