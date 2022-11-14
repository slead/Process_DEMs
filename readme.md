# Generate estimated flood level polygons

This process generates polygons representing a particular elevation above sea level (AHD) to estimate the impacts of floods reaching that level. This is a simplistic model of water levels and doesn't take into account any detailed hydrologic behaviour.

(This is a rough first-pass at the process - it can definitely be streamlined!)

## 1. Download digital elevation model(s) for the area of interest

Head to https://portal.spatial.nsw.gov.au/portal/apps/webappviewer/index.html?id=437c0697e6524d8ebf10ad0d915bc219 and download the DEM(s) covering the area of interest.

## 2. Merge DEMs

If you downloaded multiple DEMs, use the script `processDems.py` to merge them into a single raster.

```
starting_dir_name = r'C:\Users\slead\Downloads\working' # directory containing the zip file
out_gdb_name = "working.gdb"  # output geodatabase to hold the new mosaicked raster
raster_name = "Forbes"         # the name of the new mosaicked raster
```

Place the zip files in `starting_dir_name`, set the `raster_name` to the desired output name and run the script.

(Delete the zip files once processing is complete).

## 3. Clip the raster to the area of interest

To speed up processing, reduce the size of the raster to cover only the required area, using Geoprocessing Tools or -> Data -> Export Raster with a clipping extent.

## 4. Estimate the min and max flood levels

Add the raster to ArcGIS Pro and use the Live River Level Height layer (https://geohub.transport.nsw.gov.au/portal/home/item.html?id=b21e407c9bf745319b99fec37ff20fcd) to estimate the min and max levels required for the flood model.

## 5. Generate the flood polygons

Edit the script `createFloodPolygons.py` to update the listed parameters:

```
dem = r"C:\Users\slead\Downloads\Deniliquin-DEM-AHD_55_5m\Mathoura-DEM-AHD_55_5m.asc" # input DEM
output_dir = r"C:\Users\slead\Flood\Flood_20220919.gdb" # output geodatabase
prefix = "ForbesEugowra"    # prefix to apply to the output polygons
min_elevation = 246 # starting elevation
max_elevation = 252 # end elevation
step = 0.2  # interval between contours, in metres
```

Run the script, which will generate one featureclass for each elevation contour.

## 6. Create layers in ArcGIS Pro

Run the script `createLayers.py` to add the layers to ArcGIS Pro (update the parameters as per #5).

Manually create a group layer from these individual layers, and publish to GeoHub. Share with the appropriate groups.