# Create layers in an ArcGIS Pro document, ready for publishing to Portal
#
# Author:   Stephen Lead
# Date:     8th Novemnber, 2022

import arcpy
from arcpy import env
import os
import numpy as np

output_dir = r"C:\Users\slead\Flood\Flood_20220919.gdb"
prefix = "Deniliquin"
min_elevation = 91
max_elevation = 95
step = 0.2

aprx = arcpy.mp.ArcGISProject(r"C:\Users\slead\Flood\Flood.aprx")
m = aprx.listMaps("Map")[0]

for elev in np.arange(min_elevation, max_elevation + 1, step):
    elev = str(round(elev, 1)).replace(".", "_")
    
    input_features = os.path.join(output_dir, "{}_LT{}".format(prefix, str(elev).replace(".", "_")))
    output_layer = "{}_LT{}_Layer".format(prefix, elev);
    print("Processing {}".format(input_features))
    if arcpy.Exists(output_layer):
        arcpy.Delete_management(output_layer)
    lyr = arcpy.management.MakeFeatureLayer(input_features, output_layer, '', None, None).getOutput(0)
    m.addLayer(lyr, "BOTTOM")
    
aprx.save()
del(aprx)
print ("finished")