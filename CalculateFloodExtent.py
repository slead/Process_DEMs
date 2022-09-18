import arcpy
in_raster = r"C:\Users\slead\Flood\data\DEM\dem_sydney"
output_raster = arcpy.sa.RasterCalculator("Con({}<= 18, 1)").format(in_raster);
output_raster.save(r"C:\Users\slead\Flood\data\DEM\surfaces.gdb\FloodLE18")
