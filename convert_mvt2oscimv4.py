#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import vector_tile_pb2

MVT_POINT_TYPE = vector_tile_pb2.Tile.GeomType.Value('POINT')
MVT_POLYGON_TYPE = vector_tile_pb2.Tile.GeomType.Value('POLYGON')
MVT_LINESTRING_TYPE = vector_tile_pb2.Tile.GeomType.Value('LINESTRING')

OSCIM_SIZE = float(4096)
SCALE_FACTOR = 20037508.342789244

in_target = sys.argv[1] # mvt file
tile_z = int(sys.argv[2])
tile_x = int(sys.argv[3])
tile_y = int(sys.argv[4])
tile_pixels = int(sys.argv[5])
out_target = sys.argv[6] # oscim file

def parse_to_raw_geometry(encoded):
    print 'ENCODED->',encoded
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
                print 'Move to'
                paths.append([])
            elif command == 2:
                print 'Line to'
            elif command == 7:
                print 'Close'
            command_read_mode = False
            idx = idx+1
        else:
            b = encoded[idx]
            x = b-prev_b
            x = (x << 1) ^ (x >> 31)
            idx = idx+1
            prev_b = b
            
            b = encoded[idx]
            y = b-prev_b
            y = (y << 1) ^ (y >> 31)
            idx = idx+1

            fixed_x = int(float(x)/tile_pixels*OSCIM_SIZE)
            fixed_y = int(float(y)/tile_pixels*OSCIM_SIZE)
            point = [fixed_x,fixed_y]
            print x,y,'->',fixed_x,fixed_y,'(',OSCIM_SIZE,tile_pixels
            paths[-1].append(point)
            
            left_length = left_length-1
            if left_length == 0:
                command_read_mode = True

        prev_b = b
    print paths
    return paths
            
parse_to_raw_geometry([9,6,12,18,10,12,24,44,15]) # Sample written in tile.proto file

oscim_tile = TileData_v4_pb2.Data()
oscim_tile.version = 4
with open(in_target,'rb') as fr:
    mvt_content = fr.read()
    mvt_tile = vector_tile_pb2.Tile()
    mvt_tile.ParseFromString(mvt_content)

    tag2idx = {}
    serialized_tags = []
    mvt_keys = []
    oscim_keys = []
    key2oscim_idx = {}
    mvt_values = []
    oscim_values = []
    value2oscim_idx = {}

    layers = mvt_tile.layers
    for layer in layers:
        for key in layer.keys:
            mvt_keys.append(key)
            if key in key2oscim_idx:
                key_idx = key2oscim_idx[key]
            else:
                key_idx = len(oscim_keys)
                key2oscim_idx[key] = key_idx
                oscim_keys.append(key)

        for value in layer.values:
            value = str(value)
            mvt_values.append(value)
            if value in value2oscim_idx:
                value_idx = value2oscim_idx[value]
            else:
                value_idx = len(oscim_values)
                value2oscim_idx[value] = value_idx
                oscim_values.append(value)

#        print layer.name,'  Features',len(layer.features)
        found_points = []
        found_polygons = []
        found_lines = []
        integral_tag_count = 0

        for feature in layer.features:
            oscim_element = TileData_v4_pb2.Data.Element()

#            print layer.name,'    Feature',feature.id,len(feature.geometry),len(feature.tags)
            tag_idxs = []
            for tag_idx in range(len(feature.tags)/2):
                tag_key_idx = feature.tags[tag_idx*2]
                tag_value_idx = feature.tags[tag_idx*2+1]

                tag = (tag_key_idx,tag_value_idx)
                if tag in tag2idx:
                    tag_idx = tag2idx[tag]
                else:
                    tag_idx = len(serialized_tags)
                    tag2idx[tag] = tag_idx
                    serialized_tags.append(tag_key_idx)
                    serialized_tags.append(tag_value_idx)
                    
                key = mvt_keys[tag_key_idx]
                value = mvt_values[tag_value_idx]
#                print layer.name,'      ',tag_key_idx,tag_value_idx,key,value
                tag_idxs.append(tag_idx)
                oscim_element.tags.extend([tag_idx])
            oscim_element.num_tags = len(tag_idxs)

            geom_type = feature.type
            geometry = feature.geometry
            paths = parse_to_raw_geometry(geometry)

            oscim_element.layer = 0

            appending_target = None
            if geom_type == MVT_POINT_TYPE:
                appending_target = found_points
                xy = paths[0][0]
                oscim_element.coordinates.extend(xy)
            elif geom_type == MVT_POLYGON_TYPE:
                appending_target = found_polygons
            elif geom_type == MVT_LINESTRING_TYPE:
                appending_target = found_lines
            
            appending_target.append(oscim_element)

        if len(found_points) > 0: oscim_tile.points.extend(found_points)
        if len(found_polygons) > 0: oscim_tile.polygons.extend(found_polygons)
        if len(found_lines) > 0: oscim_tile.lines.extend(found_lines)

    oscim_tile.num_tags = len(serialized_tags)/2
    oscim_tile.tags.extend(serialized_tags)
    oscim_tile.keys.extend(oscim_keys)
    oscim_tile.num_keys = len(oscim_keys)
    oscim_tile.values.extend(oscim_values)
    oscim_tile.num_vals = len(oscim_values)

with open(out_target,'wb') as fw:
    fw.write(b'0123')
    fw.write(oscim_tile.SerializeToString())
