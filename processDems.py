''''
processDEMS.py

This script is designed to automate the process of creating a DEM from
a zip file downloaded from Geoscience Australia at https://elevation.fsdf.org.au/

The downloaded zip file contains a series of zipped ascii raster files, which must
be mosaicked into a single seamless raster before processing can occur.

Author: Stephen Lead (Stephen.Lead@transport.nsw.gov.au, 0410 638 348)
Date: 18 September, 2022

'''
import os
import zipfile
import arcpy
from arcpy import env

starting_dir_name = r'C:\Users\slead\Downloads\working' # directory containing the zip file
out_gdb_name = "working.gdb"  # output geodatabase to hold the new mosaicked raster
raster_name = "Walgett"         # the name of the new mosaicked raster

def unzip_all(dir_name):
    os.chdir(dir_name) # change to directory with main zip file
    for item in os.listdir(dir_name):
        if item.endswith(".zip"): 
            zip_file_name = os.path.abspath(item)
            zip_ref = zipfile.ZipFile(zip_file_name)
            zip_ref.extractall(dir_name)
            zip_ref.close()

def unzip(dir_name, file_name):
    os.chdir(dir_name)
    file_name = os.path.abspath(file_name)
    # print("Unzipping {}".format(file_name))
    zip_ref = zipfile.ZipFile(file_name)
    zip_ref.extractall(dir_name)
    zip_ref.close()

if __name__ == "__main__":
    # Unzip the main zip file
    unzip_all(starting_dir_name)

    # The result is a nested set of directories, ultimately containing
    # a series of zip files, so traverse the newly created directories.
    # working_dir is the name of the deepest nested directory, containing
    # the ascii rasters to process
    for root, dirs, files in os.walk(starting_dir_name):
        path = root.split(os.sep)
        for file in files:
            if file.endswith(".zip"):
                unzip(root, file)
                working_dir = root

    # Find all the *.asc files and mosaic them into a new raster
    env.workspace = working_dir
    env.overwriteOutput = True
    os.chdir(working_dir)

    files_to_process = []
    for item in os.listdir(working_dir):
        if item.endswith(".asc") or item.endswith(".tif"):
            files_to_process.append(item)
    print("\nInput raster files to process:\n\t{}".format(("\n\t").join(files_to_process)))
    
    # Check that the output geodatabase exists; create it if not
    if not arcpy.Exists(os.path.join(starting_dir_name, out_gdb_name)):
        print("Creating output geodatabase {}".format(out_gdb_name))
        arcpy.management.CreateFileGDB(starting_dir_name, out_gdb_name)

    print ("Creating new mosaic raster {}\{}\{}".format(starting_dir_name, out_gdb_name, raster_name))
    arcpy.MosaicToNewRaster_management(\
        (";").join(files_to_process), \
        os.path.join(starting_dir_name, out_gdb_name), \
        raster_name, \
        'GEOGCS["GCS_GDA_1994",DATUM["D_GDA_1994",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]', \
        "32_BIT_FLOAT", \
        None, \
        1,\
        "LAST", \
        "MATCH"
    )

print("\nFinished")