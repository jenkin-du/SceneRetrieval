# -*- coding:utf-8 -*-

import arcpy
from model.Polygon import *
import numpy as np

from model.Constant import *
from model.Programme import *

program = Programme()
program.start()
import sympy as sym

if __name__ == '__main__':
    arcpy.env.workspace = dataPath
    arcpy.env.overwriteOutput = True
    inFeature = "polygon.shp"
    outFeature = "rectangle.shp"

    arcpy.MinimumBoundingGeometry_management(inFeature, outFeature, "RECTANGLE_BY_AREA", mbg_fields_option=True)
    cursor = arcpy.da.SearchCursor(outFeature, ["ORIG_FID","MBG_Orient"])
    for row in cursor:
        print(str(row[0]) + ": orientation "),
        print(str(row[1]))

    del cursor
