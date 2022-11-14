# Convert DEM into smoothed polygon layers representing the areas
# below the specified elevation. Useful to simulate flood polygons
#
# Author:   Stephen Lead
# Date:     18th October, 2022

import arcpy
from arcpy import env
from arcpy.sa import *
import os
import numpy as np

dem = r"C:\Users\slead\Flood\Flood_20220919.gdb\ForbesEugowra" # input DEM
output_dir = r"C:\Users\slead\Flood\Flood_20220919.gdb" # output geodatabase
prefix = "ForbesEugowra"    # prefix to apply to the output polygons
min_elevation = 246 # starting elevation
max_elevation = 252 # end elevation
step = 0.2  # interval between contours, in metres

arcpy.CheckOutExtension("SPATIAL")
env.overwriteOutput = True
# env.workspace = working_dir
env.outputCoordinateSystem = arcpy.SpatialReference(3857)

for elev in np.arange(min_elevation, max_elevation + 1, step):
    elev = round(elev, 1)
    
    print("Processing {} at {}m".format(prefix, elev))
    
    # Create contours
    output_layer_temp = os.path.join(output_dir, "{}_LT{}_temp".format(prefix, str(elev).replace(".", "_")))
    arcpy.sa.Contour(dem, output_layer_temp, 999999999, elev, 1, "CONTOUR_POLYGON", None)
    
    # Multipart to single part
    output_layer_temp2 = os.path.join(output_dir, "{}_LT{}_temp2".format(prefix, str(elev).replace(".", "_")))
    arcpy.management.MultipartToSinglepart(output_layer_temp, output_layer_temp2)
    
    # Remove upper contours, and small polygons
    arcpy.management.MakeFeatureLayer(output_layer_temp2, "{}_Layer".format(prefix), '', None, None)
    arcpy.management.SelectLayerByAttribute("{}_Layer".format(prefix), "NEW_SELECTION", "ContourMax > {} or Shape_Area <= 10000".format(elev + 0.01), None)
    arcpy.management.DeleteRows("{}_Layer".format(prefix))

    # Remove small donuts
    output_layer = os.path.join(output_dir, "{}_LT{}".format(prefix, str(elev).replace(".", "_")))
    arcpy.management.EliminatePolygonPart(output_layer_temp2, output_layer, "AREA", "50000 SquareMeters", 0, "CONTAINED_ONLY")
    
    # # Clean up intermediate layers
    arcpy.Delete_management(output_layer_temp)
    arcpy.Delete_management(output_layer_temp2)

print("\nFinished")