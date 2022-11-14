# Create layers in an ArcGIS Pro document, ready for publishing to Portal
#
# Author:   Stephen Lead
# Date:     8th Novemnber, 2022

import arcpy
from arcpy import env
import os
import numpy as np
import yaml

config = yaml.safe_load(open("./config.yml"))
output_dir = config['output_dir']
prefix = config['prefix']
min_elevation = config['min_elevation']
max_elevation = config['max_elevation']
step = config['step']
project = config['project']

aprx = arcpy.mp.ArcGISProject(project)
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