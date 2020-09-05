#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
#import ijson
import json
import TileData_v4_pb2
from pyproj import Proj,transform

EPSG3857 = Proj(init='epsg:3857')
EPSG4326 = Proj(init='epsg:4326')

SIZE = 256
SCALE_FACTOR = 20037508.342789244

tile_z = int(sys.argv[1])
tile_x = int(sys.argv[2])
tile_y = int(sys.argv[3])
out_vtm_path = sys.argv[4]

paz = 20037508.342789244 / 256 / (2 ** tile_z)
tile_x = tile_x*SIZE
tile_y = tile_y*SIZE
center = (SIZE << tile_z) >> 1
min_lat3857 = ((center - (tile_y+SIZE+paz))/center)*SCALE_FACTOR
max_lat3857 = ((center - (tile_y-paz))/center)*SCALE_FACTOR
min_lon3857 = (((tile_x-paz)-center)/center)*SCALE_FACTOR
max_lon3857 = (((tile_x+SIZE+paz)-center)/center)*SCALE_FACTOR

min_lon4326,min_lat4326 = transform(EPSG3857,EPSG4326,min_lon3857,min_lat3857)
max_lon4326,max_lat4326 = transform(EPSG3857,EPSG4326,max_lon3857,max_lat3857)

oscim_tile = TileData_v4_pb2.Data()
oscim_tile.version = 4
found_points = []
found_polygons = []
found_lines = []
appending_target = None

tag2idx = {}
serialized_tags = []
oscim_keys = []
key2oscim_idx = {}
oscim_values = []
value2oscim_idx = {}

def ll2xy(lon,lat):
    lon3857,lat3857 = transform(EPSG4326,EPSG3857,lon,lat)
    rx = (lon3857-min_lon3857)/(max_lon3857-min_lon3857)
    ry = (lat3857-min_lat3857)/(max_lat3857-min_lat3857)
    ry = 1.0-ry
    x = int(rx*4096.0)
    y = int(ry*4096.0)
    return x,y

def lls2xy(lls):
    abs_xys = []
    for ll in lls:
        lon = ll[0]
        lat = ll[1]
        x,y = ll2xy(lon,lat)
        abs_xys.append([x,y])

    last_x = 0
    last_y = 0
    delta_xys = []
    for x,y in abs_xys:
        dx = x-last_x
        dy = y-last_y
        delta_xys.append([dx,dy])
        last_x = x
        last_y = y

    return delta_xys

def llss2xy(llss):
    abs_xyss = []
    for lls in llss:
        abs_xys = []
        for ll in lls:
            lon = ll[0]
            lat = ll[1]
            x,y = ll2xy(lon,lat)
            abs_xys.append([x,y])
        abs_xyss.append(abs_xys)
            
    last_x = 0
    last_y = 0
    delta_xyss = []
    for abs_xys in abs_xyss:
        delta_xys = []
        for x,y in abs_xys:
            dx = x-last_x
            dy = y-last_y
            delta_xys.append([dx,dy])
            last_x = x
            last_y = y
        delta_xyss.append(delta_xys)
    
    return delta_xyss
    
j = json.loads(sys.stdin.read())
layers = j['features']
for layer in layers:
    features = layer['features']
    for feature in features:
        tag_idxs_in_feature = []
        properties = feature['properties']
        for key in properties:
            if key in frozenset(['id','area','sort_rank','source','min_zoom','surface']): continue
            
            value = properties[key]
            value = unicode(value)
            
            if key in key2oscim_idx:
                key_idx = key2oscim_idx[key]
            else:
                key_idx = len(oscim_keys)
                key2oscim_idx[key] = key_idx
                oscim_keys.append(key)
                
            if value in value2oscim_idx:
                value_idx = value2oscim_idx[value]
            else:
                value_idx = len(oscim_values)
                value2oscim_idx[value] = value_idx
                oscim_values.append(value)
        
            tag = (key_idx,value_idx)
            if tag in tag2idx:
                tag_idx = tag2idx[tag]
            else:
                tag_idx = len(serialized_tags)/2
                tag2idx[tag] = tag_idx
                serialized_tags.append(key_idx)
                serialized_tags.append(value_idx)
            tag_idxs_in_feature.append(tag_idx)

        geometry = feature['geometry']
        geometry_type = geometry['type']
        c = geometry['coordinates']

        if geometry_type == 'Point':
            oscim_element = TileData_v4_pb2.Data.Element()
            oscim_element.num_tags = len(tag_idxs_in_feature)
            oscim_element.tags.extend(tag_idxs_in_feature)
            
            x,y = ll2xy(c[0],c[1])
            oscim_element.coordinates.extend([x,y])
            found_points.append(oscim_element)

        elif geometry_type == 'MultiPoint':
            for cp in c:
                oscim_element = TileData_v4_pb2.Data.Element()
                oscim_element.num_tags = len(tag_idxs_in_feature)
                oscim_element.tags.extend(tag_idxs_in_feature)

                x,y = ll2xy(cp[0],cp[1])
                oscim_element.coordinates.extend([x,y])
                found_points.append(oscim_element)

        elif geometry_type == 'LineString':
            oscim_element = TileData_v4_pb2.Data.Element()
            oscim_element.num_tags = len(tag_idxs_in_feature)
            oscim_element.tags.extend(tag_idxs_in_feature)

            delta_xys = lls2xy(c)
            oscim_element.num_indices = 1
            oscim_element.indices.extend([len(delta_xys)])
            flat_xys = []
            for x,y in delta_xys:
                flat_xys.append(x)
                flat_xys.append(y)
            oscim_element.coordinates.extend(flat_xys)
            found_lines.append(oscim_element)

        elif geometry_type == 'MultiLineString':
            for cp in c:
                oscim_element = TileData_v4_pb2.Data.Element()
                oscim_element.num_tags = len(tag_idxs_in_feature)
                oscim_element.tags.extend(tag_idxs_in_feature)

                delta_xys = lls2xy(cp)
                oscim_element.indices.extend([len(delta_xys)])
                oscim_element.num_indices = 1
                flat_xys = []
                for x,y in delta_xys:
                    flat_xys.append(x)
                    flat_xys.append(y)
                oscim_element.coordinates.extend(flat_xys)
                found_lines.append(oscim_element)

        elif geometry_type == 'Polygon':
            oscim_element = TileData_v4_pb2.Data.Element()
            oscim_element.num_tags = len(tag_idxs_in_feature)
            oscim_element.tags.extend(tag_idxs_in_feature)

            delta_xyss = llss2xy(c)
            indices = []
            for delta_xys in delta_xyss:
                indices.append(len(delta_xys))
            oscim_element.indices.extend(indices)
            oscim_element.num_indices = len(indices)
            flat_xys = []
            for delta_xys in delta_xyss:
                for x,y in delta_xys:
                    flat_xys.append(x)
                    flat_xys.append(y)
            oscim_element.coordinates.extend(flat_xys)
            found_polygons.append(oscim_element)

        elif geometry_type == 'MultiPolygon':
            for cp in c:
                oscim_element = TileData_v4_pb2.Data.Element()
                oscim_element.num_tags = len(tag_idxs_in_feature)
                oscim_element.tags.extend(tag_idxs_in_feature)

                delta_xyss = llss2xy(cp)
                indices = []
                for delta_xys in delta_xyss:
                    indices.append(len(delta_xys))
                oscim_element.indices.extend(indices)
                oscim_element.num_indices = len(indices)
                flat_xys = []
                for delta_xys in delta_xyss:
                    for x,y in delta_xys:
                        flat_xys.append(x)
                        flat_xys.append(y)
                oscim_element.coordinates.extend(flat_xys)
                found_polygons.append(oscim_element)
            
# for call in ijson.parse(sys.stdin):
#     str_path,key,value = call
#     path = str_path.split('.')
#     if path[0] == 'features':
#         if len(path) == 1:
#             pass
#         else:
#             if path[1] == 'item':
#                 if len(path) == 2:
#                     pass
#                 else:
#                     if path[2] == 'features':
#                         if len(path) == 3:
#                             pass
#                         else:
#                             if path[3] == 'item':
#                                 if len(path) == 4:
#                                     if key == 'start_map':
#                                         oscim_element = TileData_v4_pb2.Data.Element()
#                                         appending_target = None
#                                     elif key == 'end_map':
#                                         appending_target.append(oscim_element)
#                                 else:
#                                     if path[4] == 'geometry':
#                                         if len(path) == 5:
#                                             pass
#                                         else:
#                                             if path[5] == 'type':
#                                                 if value == 'LineString':
#                                                     appending_target = found_lines
#                                                 elif value == 'MultiLineString':
#                                                     appending_target = found_lines
#                                                 elif value == 'Polygon':
#                                                     appending_target = found_polygons
#                                                 elif value == 'MultiPolygon':
#                                                     appending_target = found_polygons
#                                                 elif value == 'Point':
#                                                     appending_target = found_points
#                                                 else:
#                                                     print 'Wrong geometry type',value
            
if len(found_points) > 0: oscim_tile.points.extend(found_points)
if len(found_polygons) > 0: oscim_tile.polygons.extend(found_polygons)
if len(found_lines) > 0: oscim_tile.lines.extend(found_lines)

oscim_tile.num_tags = len(serialized_tags)/2
oscim_tile.tags.extend(serialized_tags)
oscim_tile.keys.extend(oscim_keys)
oscim_tile.num_keys = len(oscim_keys)
oscim_tile.values.extend(oscim_values)
oscim_tile.num_vals = len(oscim_values)
        
with open(out_vtm_path,'wb') as fw:
    fw.write(b'0123')
    fw.write(oscim_tile.SerializeToString())
