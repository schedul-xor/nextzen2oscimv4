#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import TileData_v4_pb2
import vector_tile_pb2

in_target = sys.argv[1] # mvt file
tile_z = int(sys.argv[2])
tile_x = int(sys.argv[3])
tile_y = int(sys.argv[4])
out_target = sys.argv[5] # oscim file

SIZE = 256
SCALE_FACTOR = 20037508.342789244

paz = 20037508.342789244 / 256 / (2 ** tile_z)
tile_x = tile_x*SIZE
tile_y = tile_y*SIZE
center = (SIZE << tile_z) >> 1
min_lat3857 = ((center - (tile_y+SIZE+paz))/center)*SCALE_FACTOR
max_lat3857 = ((center - (tile_y-paz))/center)*SCALE_FACTOR
min_lon3857 = (((tile_x-paz)-center)/center)*SCALE_FACTOR
max_lon3857 = (((tile_x+SIZE+paz)-center)/center)*SCALE_FACTOR

def parse_to_raw_geometry(encoded):
    command_read_mode = True
    left_length = 0
    prev_b = 0
    idx = 0
    paths = []
    while idx < len(encoded):
        if command_read_mode:
            b = encoded[idx]
            command = b & 0x07
            left_length = b >> 3
            if command == 1:
                print 'Move to',left_length
                paths.append([])
            elif command == 2: print 'Line to',left_length
            elif command == 7: print 'Close path'
            command_read_mode = False
            idx = idx+1
        else:
            b = encoded[idx]
            x = prev_b-b
            idx = idx+1
            prev_b = b
            
            b = encoded[idx]
            y = b-prev_b
            idx = idx+1

            point = [x,y]
            paths[-1].append(point)
            left_length = left_length-1
            if left_length == 0:
                command_read_mode = True

        prev_b = b
    return paths
            
# parse_to_raw_geometry([9,6,12,18,10,12,24,44,15]) # Sample written in tile.proto file

oscim_tile = TileData_v4_pb2.Data()
with open(in_target,'rb') as fr:
    mvt_content = fr.read()
    mvt_tile = vector_tile_pb2.Tile()
    mvt_tile.ParseFromString(mvt_content)

    layers = mvt_tile.layers
    for layer in layers:
        print layer.name,'  Keys',len(layer.keys)
        keys = []
        for key in layer.keys: keys.append(key)
        print layer.name,'  Values',len(layer.values)
        values = []
        for value in layer.values: values.append(value)

        print layer.name,'  Features',len(layer.features)
        found_points = []
        found_polygons = []
        found_lines = []
        integral_tag_count = 0
        for feature in layer.features:
            print layer.name,'    Feature',feature.id,len(feature.geometry),len(feature.tags)
            for tag_idx in range(len(feature.tags)/2):
                tag_key_idx = feature.tags[tag_idx*2]
                tag_value_idx = feature.tags[tag_idx*2+1]
#                print layer.name,'      ',tag_key_idx,tag_value_idx,keys[tag_key_idx],values[tag_value_idx]

            geom_type = feature.type

            oscim_element = TileData_v4_pb2.Data.Element()
            appending_target = None
            if geom_type == vector_tile_pb2.Tile.GeomType.Value('POINT'):
                appending_target = found_points
            elif geom_type == vector_tile_pb2.Tile.GeomType.Value('POLYGON'):
                appending_target = found_polygons
            elif geom_type == vector_tile_pb2.Tile.GeomType.Value('LINESTRING'):
                appending_target = found_lines

            geometry = feature.geometry
            paths = parse_to_raw_geometry(geometry)
            print paths
            
            appending_target.append(oscim_element)

#        oscim_tile.num_tags = len(layer.tags)
        oscim_tile.num_keys = len(layer.keys)
        oscim_tile.num_vals = len(layer.values)
        
        if len(found_points) > 0: oscim_tile.points.extend(found_points)
        if len(found_polygons) > 0: oscim_tile.polygons.extend(found_polygons)
        if len(found_lines) > 0: oscim_tile.lines.extend(found_lines)

        
