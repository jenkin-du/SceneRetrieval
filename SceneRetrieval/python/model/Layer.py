# -*- coding:utf-8 -*-
from model.Polygon import *


class Layer(object):
    name = ""
    polygons = []  # type: List[Polygon]
