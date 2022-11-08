import os
import json
import requests
import arcgis
from arcgis.gis import GIS
gis = GIS("https://sims.spatial.nsw.gov.au/rest/tokens", "stephen.lead@transport.nsw.gov.au", "FullExtent2022")


url = 'https://sims.spatial.nsw.gov.au/arcgis/rest/services/ESSIL_REMO_GDA94/MapServer/227/'

def download_data(oid):
    query = "?where=objectid>={}+and+objectid<{}".format(oid, oid + 1000)
    query += "&outFields=objectid&f=json"
    print(url + query)
    response = requests.get(url + query)
    print(response.json)
    if response.status_code == 200:
        #collect json from server
        url_json = response.json()
        
        # #define file path
        # file_path = os.path.join(timestamp_path,str(i)+".json")
        
        # #output file
        # out_file = open(file_path,"w")
        # json.dump(url_json, out_file, indent = 6)
        # out_file.close()
    oid+=1000
    # download_data(oid)

if __name__ == "__main__":
    oid = 1
    download_data(1)