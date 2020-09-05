#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import TileData_v4_pb2
import vector_tile_pb2

in_target = sys.argv[1] # mvt file
out_target = sys.argv[2] # oscim file

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
            appending_target.append(oscim_element)

#        oscim_tile.num_tags = len(layer.tags)
        oscim_tile.num_keys = len(layer.keys)
        oscim_tile.num_vals = len(layer.values)
        
        if len(found_points) > 0: oscim_tile.points.extend(found_points)
        if len(found_polygons) > 0: oscim_tile.polygons.extend(found_polygons)
        if len(found_lines) > 0: oscim_tile.lines.extend(found_lines)
