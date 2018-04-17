# -*- coding:utf-8 -*-

import arcpy
from model.Polygon import *
import numpy as np
from model.Constant import *
from model.Programme import *

import simplejson as json

program = Programme()
program.start()

if __name__ == '__main__':
    poly = Polygon()
    poly.oid = "polygon_0"
    poly.area = 200
    poly.gravity = Point(100, 100)
    strs = json.dumps(poly,default=lambda o: o.__dict__, sort_keys=True, indent=4)
    print(strs)

    pass
