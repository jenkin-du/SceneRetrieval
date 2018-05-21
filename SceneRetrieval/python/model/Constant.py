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

# 空间要素匹配的精度
polygon_precision = 0.7

# 空间关系匹配的精度
space_precision = 0.7

# 场景匹配精度
scene_precision = 0.75

# 宽高比差异度
whRatioDiff = 2

# 外包矩形匹配度
envelope_precision = 0.8
