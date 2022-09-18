import os
import zipfile
import arcpy

starting_dir_name = r'C:\Users\slead\Downloads'
starting_zip_name = ''

def unzip_all(dir_name):
    os.chdir(dir_name) # change to directory with main zip file
    for item in os.listdir(dir_name):
        if item.endswith(".zip"): 
            starting_zip_name = os.path.abspath(item)
            # print("Processing {}".format(starting_zip_name))
            zip_ref = zipfile.ZipFile(starting_zip_name)
            zip_ref.extractall(dir_name)
            zip_ref.close()

def unzip(dir_name, file_name, cleanup):
    os.chdir(dir_name)
    file_name = os.path.abspath(file_name)
    # print("Processing {}".format(file_name))
    zip_ref = zipfile.ZipFile(file_name)
    zip_ref.extractall(dir_name)
    zip_ref.close()
    if cleanup:
        print("Deleting temporary file {}".format(file_name))
        os.remove(file_name)

def mosaic(images):
    arcpy.management.MosaicToNewRaster(r"'C:\Users\slead\Downloads\DEM\NSW Government - Spatial Services\DEM\1 Metre\Dubbo201407-LID1-AHD_6466426_55_0002_0002_1m.asc';'C:\Users\slead\Downloads\DEM\NSW Government - Spatial Services\DEM\1 Metre\Dubbo201407-LID1-AHD_6466428_55_0002_0002_1m.asc'", r"C:\Users\slead\Downloads\DEM\Dubbo_20220918.gdb", "Dubbo_small", None, "32_BIT_FLOAT", None, 1, "LAST", "FIRST")



if __name__ == "__main__":
    # Unzip the main zip file
    # unzip_all(starting_dir_name)

    # The result is a nested set of directories, ultimately containing
    # a series of zip files, so traverse the newly created directories
    working_dir = ''
    for root, dirs, files in os.walk(starting_dir_name):
        path = root.split(os.sep)
        for file in files:
            if file.endswith(".zip") and not file == starting_zip_name:
                # unzip(root, file, False)
                working_dir = root

    from arcpy import env
    env.workspace = working_dir
    files_to_process = []
    
    for item in os.listdir(working_dir):
        if item.endswith(".asc"):
            files_to_process.append(item)

    print("\nFiles to process: {}".format((";").join(files_to_process)))
    
    arcpy.MosaicToNewRaster_management(\
        (";").join(files_to_process), \
        r"C:\Users\slead\Flood\data\DEM\Dubbo\Dubbo.gdb", \
        "new_mosaic2", \
        'GEOGCS["GCS_GDA_1994",DATUM["D_GDA_1994",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]', \
        "32_BIT_FLOAT", \
        None, \
        1,\
        "LAST", \
        "FIRST"
    )
    
    # arcpy.management.MosaicToNewRaster(\
    #     r"C:\Users\slead\Flood\data\DEM\Dubbo\Dubbo201407-LID1-AHD_6466426_55_0002_0002_1m.asc;C:\Users\slead\Flood\data\DEM\Dubbo\Dubbo201407-LID1-AHD_6466428_55_0002_0002_1m.asc", \
    #     r"C:\Users\slead\Flood\data\DEM\Dubbo\Dubbo.gdb", \
    #     "new_mosaic", \
    #     'GEOGCS["GCS_GDA_1994",DATUM["D_GDA_1994",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]', \
    #     "32_BIT_FLOAT", \
    #     None, \
    #     1,\
    #     "LAST", \
    #     "FIRST")


print("finished")