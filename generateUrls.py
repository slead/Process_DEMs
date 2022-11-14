# Generate URLs
#
# quickly generate the list of URLs

import numpy as np
import json
import yaml

config = yaml.safe_load(open("./config.yml"))
min_elevation = config['min_elevation']
max_elevation = config['max_elevation']
step = config['step']

prefix = "Buronga_flood_polygons"
base = "https://geohub.transport.nsw.gov.au/server/rest/services/Hosted/"

idx = 0
config = []
for elev in np.arange(min_elevation, max_elevation + 1, step):
    elev = str(round(elev, 1))
    idx += 1
    data = {}
    data['title'] = "{}m contour".format(elev)
    data['url'] = "{}{}/FeatureServer/{}".format(base, prefix, idx)
    json_data = json.dumps(data)
    config.append(json_data)
    
print(",".join(config))