#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import subprocess
from flask import Flask
import nextzenjson2oscimv4 # In this directory

TIPPECANOE_BIN_PATH = '/usr/local/bin/tippecanoe-decode'

OSCIMV4_BUFFER_PIXELS = 156600.0

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

    is_not_original = False
    if tile_z >= 18:
        is_not_original = True
        new_x = tile_x
        new_y = tile_y
        new_z = tile_z
        while new_z >= 18:
            new_x = int(new_x/2)
            new_y = int(new_y/2)
            new_z = new_z-1
        mvt_filename = str(new_z)+'_'+str(new_x)+'_'+str(new_y)+'.mvt'
    else:
        mvt_filename = str(tile_z)+'_'+str(tile_x)+'_'+str(tile_y)+'.mvt'
        
    tmp_mvt_path = os.path.join(MVT_CACHE_DIR,mvt_filename)
    if os.path.exists(tmp_mvt_path) and os.stat(tmp_mvt_path).st_size == 0: os.unlink(tmp_mvt_path) # Remove zero-sized files
    if not os.path.exists(tmp_mvt_path):
        cmd = ['wget','--no-check-certificate','-O',tmp_mvt_path,'http://localhost:22380/maps/osm/'+str(tile_z)+'/'+str(tile_x)+'/'+str(tile_y)+'.pbf']
        subprocess.call(cmd)

    if is_not_original:
        geojson_filename = str(new_z)+'_'+str(new_x)+'_'+str(new_y)+'.json'
        tmp_geojson_path = os.path.join(GEOJSON_CACHE_DIR,geojson_filename)
        if os.path.exists(tmp_geojson_path) and os.stat(tmp_geojson_path).st_size == 0: os.unlink(tmp_geojson_path) # Remove zero-sized files
        if not os.path.exists(tmp_geojson_path):
            cmd = TIPPECANOE_BIN_PATH+' '+tmp_mvt_path+' '+str(new_z)+' '+str(new_x)+' '+str(new_y)+' > '+tmp_geojson_path
            subprocess.call(cmd,shell=True)
    else:
        geojson_filename = str(tile_z)+'_'+str(tile_x)+'_'+str(tile_y)+'.json'
        tmp_geojson_path = os.path.join(GEOJSON_CACHE_DIR,geojson_filename)
        if os.path.exists(tmp_geojson_path) and os.stat(tmp_geojson_path).st_size == 0: os.unlink(tmp_geojson_path) # Remove zero-sized files
        if not os.path.exists(tmp_geojson_path):
            cmd = TIPPECANOE_BIN_PATH+' '+tmp_mvt_path+' '+str(tile_z)+' '+str(tile_x)+' '+str(tile_y)+' > '+tmp_geojson_path
            subprocess.call(cmd,shell=True)

    with open(tmp_geojson_path,encoding='UTF-8') as fr:
        oscimv4_buffer_pixels = float(OSCIMV4_BUFFER_PIXELS)/pow(2.0,float(tile_z))
        oscimv4_binary = nextzenjson2oscimv4.convert(tile_z,tile_x,tile_y,oscimv4_buffer_pixels,fr.read())
        
    return oscimv4_binary

if __name__ == '__main__':
    app.run(port=32400)