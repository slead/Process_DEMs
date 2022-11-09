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

working_dir = r"C:\Users\slead\Downloads\working\working.gdb"
output_dir = r"C:\Users\slead\Flood\Flood_20220919.gdb"
prefix = "Walgett"
min_elevation = 120
max_elevation = 126
step = 0.2

arcpy.CheckOutExtension("SPATIAL")
env.overwriteOutput = True
env.workspace = working_dir
env.outputCoordinateSystem = arcpy.SpatialReference(3857)
dem = arcpy.Raster(os.path.join(working_dir,prefix))

for elev in np.arange(min_elevation, max_elevation + 1, step):
    elev = round(elev, 1)

    # Create a binary raster for this elevation    
    print("Processing {} at {}m".format(prefix, elev))
    elev_raster = Con(dem < elev, 1)

    # Convert to polygons
    output_layer_temp = os.path.join(output_dir, "{}_LT{}_temp".format(prefix, str(elev).replace(".", "_")))
    arcpy.conversion.RasterToPolygon(elev_raster, output_layer_temp, "SIMPLIFY", "Value", "SINGLE_OUTER_PART", None)

    # Buffer slightly to create a layer with which to union - this removes the holes
    # arcpy.analysis.PairwiseBuffer(output_layer, "{}LT_{}_buffer".format(prefix, elev), "10 Meters", "NONE", None, "PLANAR", "0 Meters")
    # arcpy.analysis.Union([output_layer, "{}LT_{}_buffer".format(prefix, elev)], "{}_LT{}_union".format(prefix, elev), "ALL", None, "NO_GAPS")
    
    # # Dissolve the unioned layer to remove internal filled holes
    # arcpy.management.Dissolve("{}_LT{}_union".format(prefix, elev), output_layer, None, None, "SINGLE_PART", "DISSOLVE_LINES", '')
    
    # Remove the donuts
    output_layer_temp2 = os.path.join(output_dir, "{}_LT{}_temp2".format(prefix, str(elev).replace(".", "_")))
    arcpy.management.EliminatePolygonPart(output_layer_temp, output_layer_temp2, "AREA", "50000 SquareMeters", 0, "CONTAINED_ONLY")

    # Simplify
    output_layer = os.path.join(output_dir, "{}_LT{}".format(prefix, str(elev).replace(".", "_")))
    arcpy.cartography.SimplifyPolygon(output_layer_temp2, output_layer, "POINT_REMOVE", "10 Meters", "0 SquareMeters", "RESOLVE_ERRORS", "NO_KEEP", None)
    
    # Remove small polygons
    arcpy.management.MakeFeatureLayer(output_layer, "{}_Layer".format(prefix), '', None, None)
    arcpy.management.SelectLayerByAttribute("{}_Layer".format(prefix), "NEW_SELECTION", "Shape_Area <= 10000", None)
    arcpy.management.DeleteRows("{}_Layer".format(prefix))
    
    # Remove extraneous vertices
    arcpy.edit.Generalize(output_layer, "10 Meters")

    # Add an elevation field
    arcpy.management.AddField(output_layer, "elevation", 'SHORT')
    arcpy.management.CalculateField(output_layer, "elevation", elev)

    # Clean up intermediate layers
    # arcpy.Delete_management("{}LT_{}_buffer".format(prefix, elev))
    # arcpy.Delete_management("{}_LT{}_union".format(prefix, elev))
    arcpy.Delete_management(output_layer_temp)
    arcpy.Delete_management(output_layer_temp2)

del dem
print("\nFinished")