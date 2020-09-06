#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import subprocess
from flask import Flask
import json2oscimv4 # In this directory

NEXTZEN_API_KEY = '_lQbucvFRf6L7cPYIG1Fdg'
TIPPECANOE_BIN_PATH = '/usr/local/bin/tippecanoe-decode'

OSCIMV4_BUFFER_PIXELS = 5

TMP_PATH = './tmp'
MVT_CACHE_DIR = os.path.join(TMP_PATH,'mvt')
GEOJSON_CACHE_DIR = os.path.join(TMP_PATH,'geojson')

if not os.path.exists(TMP_PATH): os.mkdir(TMP_PATH)
if not os.path.exists(MVT_CACHE_DIR): os.mkdir(MVT_CACHE_DIR)
if not os.path.exists(GEOJSON_CACHE_DIR): os.mkdir(GEOJSON_CACHE_DIR)

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/vtm/<z>/<x>/<y>.vtm')
def vtm(z,x,y):
    tile_z = int(z)
    tile_x = int(x)
    tile_y = int(y)

    if tile_z < 17:
        mvt_filename = str(tile_z)+'_'+str(tile_x)+'_'+str(tile_y)+'.mvt'
        tmp_mvt_path = os.path.join(MVT_CACHE_DIR,mvt_filename)
        if not os.path.exists(tmp_mvt_path):
            cmd = ['wget','--no-check-certificate','-O',tmp_mvt_path,'https://tile.nextzen.org/tilezen/vector/v1/256/all/'+str(tile_z)+'/'+str(tile_x)+'/'+str(tile_y)+'.mvt?api_key='+NEXTZEN_API_KEY]
            subprocess.call(cmd)

        geojson_filename = str(tile_z)+'_'+str(tile_x)+'_'+str(tile_y)+'.json'
        tmp_geojson_path = os.path.join(GEOJSON_CACHE_DIR,geojson_filename)
        if not os.path.exists(tmp_geojson_path):
            cmd = TIPPECANOE_BIN_PATH+' '+tmp_mvt_path+' '+str(tile_z)+' '+str(tile_x)+' '+str(tile_y)+' > '+tmp_geojson_path
            subprocess.call(cmd,shell=True)

        with open(tmp_geojson_path) as fr:
            oscimv4_binary = json2oscimv4.convert(tile_z,tile_x,tile_y,OSCIM_BUFFER_PIXELS,fr.read())
    else:
        oscimv4_binary = b'0123'
        
    return oscimv4_binary

if __name__ == '__main__':
    app.run(port=32400)
