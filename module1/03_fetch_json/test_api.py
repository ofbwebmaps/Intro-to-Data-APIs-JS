# CS50 - Final Project - Export par API KoboTollBox de donnees terrain collectees pour génération de carte
# ln0358 - https://github.com/ln0358

import requests
import os
import time
import shutil


# Choisir le bon formulaire !!!!
# url = "https://kc.kobotoolbox.org/api/v1/data/539494" # TEST
url = "https://kc.kobotoolbox.org/api/v1/data/550661"  # PROD

# gestion de fichiers output
basedir = "./"
# IL FAUT CREER LE REPERTOIRE ARCHIVES A L'INSTALLATION !!!
newdir = "./archives/"
archive_filename = "output_" + time.strftime("%Y%m%d-%H%M%S") + ".geojson"
filename = f'output.geojson'

payload = {}
files = {}
headers = {
    'Authorization': 'Token 8bcb99b155b024cbca9c8c9e20c0fc549cb27b64'
}

response = requests.request("GET", url, headers=headers, data=payload, files=files)

collect = response.json()

if os.path.isfile(basedir + filename):
    shutil.move(basedir + filename, newdir + archive_filename)

# partie statique 1
print('{\n"type": "FeatureCollection",\n"name": "onepf_web",\n"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },\n"features": [', file=open(filename, "w"))
# Itération sur les résultats - 1
for i in range(0, len(collect)-1):
    print('{ "type": "Feature", "properties": { "meta/instanceID": "' + collect[i]["meta/instanceID"] + '", "obs_org/station_dept": ' + str(collect[i]["obs_org/station_dept"]) + ',"obs_org_001/stat_code": "' + collect[i]["obs_org_001/stat_code"] + '", "obs_org_001/stat_choice": "' + collect[i]["obs_org_001/stat_choice"] + '" }, "geometry": { "type": "Point", "coordinates": [ ' + str(collect[i]["_geolocation"][1]) + ', ' + str(collect[i]["_geolocation"][0]) + ' ] } },', file=open(filename, "a"))
# ajout derniere ligne sans virgule
print('{ "type": "Feature", "properties": { "meta/instanceID": "' + collect[len(collect)-1]["meta/instanceID"] + '", "obs_org/station_dept": ' + str(collect[len(collect)-1]["obs_org/station_dept"]) + ',"obs_org_001/stat_code": "' + collect[len(collect)-1]["obs_org_001/stat_code"] + '", "obs_org_001/stat_choice": "' + collect[len(collect)-1]["obs_org_001/stat_choice"] + '" }, "geometry": { "type": "Point", "coordinates": [ ' + str(collect[len(collect)-1]["_geolocation"][1]) + ', ' + str(collect[len(collect)-1]["_geolocation"][0]) + ' ] } }', file=open(filename, "a"))
# partie statique 2 et fin
print(']\n}', file=open(filename, "a"))
