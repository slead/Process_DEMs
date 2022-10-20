# Convert DEM into smoothed polygon layers representing the areas
# below the specified elevation. Useful to simulate flood polygons
#
# Author:   Stephen Lead
# Date:     18th October, 2022

import arcpy
from arcpy import env
from arcpy.sa import *
import os

working_dir = r"C:\Users\slead\Downloads\working\working.gdb"
output_dir = r"C:\Users\slead\Flood\Flood_20220919.gdb"
prefix = "Echuca"
min_elevation = 90
max_elevation = 95
step = 1

arcpy.CheckOutExtension("SPATIAL")
env.overwriteOutput = True
env.workspace = working_dir
dem = arcpy.Raster(os.path.join(working_dir,prefix))

for elevation in range(min_elevation, max_elevation + 1, step):

    # Create a binary raster for this elevation    
    print("Processing {} at {}m".format(prefix, elevation))
    elev = int(elevation)
    elev_raster = Con(dem < elev, 1)

    # Convert to polygons
    output_layer = os.path.join(output_dir, "{}_LT{}".format(prefix, elev))
    arcpy.conversion.RasterToPolygon(elev_raster, output_layer, "SIMPLIFY", "Value", "SINGLE_OUTER_PART", None)

    # Remove extraneous vertices
    arcpy.edit.Generalize(output_layer, "10 Meters")

    # Buffer slightly to create a layer with which to union - this removes the holes
    arcpy.analysis.PairwiseBuffer(output_layer, "{}LT_{}_buffer".format(prefix, elev), "10 Meters", "NONE", None, "PLANAR", "0 Meters")
    arcpy.analysis.Union([output_layer, "{}LT_{}_buffer".format(prefix, elev)], "{}_LT{}_union".format(prefix, elev), "ALL", None, "NO_GAPS")
    
    # Dissolve the unioned layer to remove internal filled holes
    arcpy.management.Dissolve("{}_LT{}_union".format(prefix, elev), output_layer, None, None, "SINGLE_PART", "DISSOLVE_LINES", '')

    # Remove small polygons
    arcpy.management.MakeFeatureLayer(output_layer, "{}_Layer".format(prefix), '', None, None)
    arcpy.management.SelectLayerByAttribute("{}_Layer".format(prefix), "NEW_SELECTION", "Shape_Area <= 0.000003", None)
    arcpy.management.DeleteRows("{}_Layer".format(prefix))

    # Generalise again to remove any extra vertices which were added
    arcpy.edit.Generalize(output_layer, "10 Meters")

    # Add an elevation field
    arcpy.management.AddField(output_layer, "elevation", 'SHORT')
    arcpy.management.CalculateField(output_layer, "elevation", elev)

    # Clean up intermediate layers
    arcpy.Delete_management("{}LT_{}_buffer".format(prefix, elev))
    arcpy.Delete_management("{}_LT{}_union".format(prefix, elev))

del dem
print("\nFinished")