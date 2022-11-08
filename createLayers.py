# Create layers in an ArcGIS Pro document, ready for publishing to Portal
#
# Author:   Stephen Lead
# Date:     8th Novemnber, 2022

import arcpy
from arcpy import env
import os
import numpy as np

output_dir = r"C:\Users\slead\Flood\Flood_20220919.gdb"
prefix = "Condobolin"
min_elevation = 188
max_elevation = 191
step = 0.2

aprx = arcpy.mp.ArcGISProject(r"C:\Users\slead\Flood\processing\processing.aprx")
m = aprx.listMaps("Map")[0]

for elev in np.arange(min_elevation, max_elevation + 1, step):
    elev = str(round(elev, 1)).replace(".", "_")
    print("Processing {}_LT{}".format(prefix, elev))