#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import subprocess
from flask import Flask
#import nextzenjson2oscimv4 # In this directory
import mvtjson2oscimv4 # In this directory
import redis

TIPPECANOE_BIN_PATH = '/usr/local/bin/tippecanoe-decode'
#MVT_URL = 'https://tile.nextzen.org/tilezen/vector/v1/256/all/{0}/{1}/{2}.mvt?api_key=_lQbucvFRf6L7cPYIG1Fdg'
#MVT_URL = 'http://tile0.ogiqvo.com:22380/maps/osm/{0}/{1}/{2}.pbf'
MVT_URL = 'http://localhost:22380/maps/osm/{0}/{1}/{2}.pbf'

OSCIMV4_BUFFER_PIXELS = 156600.0

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

r = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB)

TMP_PATH = './tmp'
MVT_CACHE_DIR = os.path.join(TMP_PATH,'mvt')
GEOJSON_CACHE_DIR = os.path.join(TMP_PATH,'geojson')

required_commands = []
tmp_path_exists = os.path.exists(TMP_PATH)
mvt_cache_dir_exists = os.path.exists(MVT_CACHE_DIR)
geojson_cache_dir_exists = os.path.exists(GEOJSON_CACHE_DIR)

if not tmp_path_exists or not mvt_cache_dir_exists or not geojson_cache_dir_exists:
    print('ERROR: Required directories was not fully prepared. Exec the following command')
    if not tmp_path_exists: print('mkdir -p '+TMP_PATH)
    if not mvt_cache_dir_exists: print('mkdir -p '+MVT_CACHE_DIR)
    if not geojson_cache_dir_exists: print('mkdir -p '+GEOJSON_CACHE_DIR)
    quit(-1)

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
        cmd = ['wget','--no-check-certificate','-O',tmp_mvt_path,MVT_URL.format(tile_z,tile_x,tile_y)]
        subprocess.call(cmd)

    for retry_i in range(100):
        if os.path.getsize(tmp_mvt_path) == 23:
            os.unlink(tmp_mvt_path)
            r.delete('osm/'+str(z)+'/'+str(x)+'/'+str(y))
            cmd = ['wget','--no-check-certificate','-O',tmp_mvt_path,MVT_URL.format(tile_z,tile_x,tile_y)]
            subprocess.call(cmd)
        else: break

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
            # -f option means 'force', which outputs at least valid JSON string
            cmd = TIPPECANOE_BIN_PATH+' -f '+tmp_mvt_path+' '+str(tile_z)+' '+str(tile_x)+' '+str(tile_y)+' > '+tmp_geojson_path
            subprocess.call(cmd,shell=True)

    with open(tmp_geojson_path,encoding='UTF-8') as fr:
        oscimv4_buffer_pixels = float(OSCIMV4_BUFFER_PIXELS)/pow(2.0,float(tile_z))
#        oscimv4_binary = nextzenjson2oscimv4.convert(tile_z,tile_x,tile_y,oscimv4_buffer_pixels,fr.read())
        oscimv4_binary = mvtjson2oscimv4.convert(tile_z,tile_x,tile_y,oscimv4_buffer_pixels,fr.read())
        
    return oscimv4_binary

if __name__ == '__main__':
    app.run(port=32400)
