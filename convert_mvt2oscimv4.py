#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import TileData_v4_pb2
import vector_tile_pb2

in_target = sys.argv[1] # mvt file
out_target = sys.argv[2] # oscim file

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
        for feature in layer.features:
            print layer.name,'    Feature',feature.id,len(feature.geometry),len(feature.tags)
            for tag_idx in range(len(feature.tags)/2):
                tag_key_idx = feature.tags[tag_idx*2]
                tag_value_idx = feature.tags[tag_idx*2+1]
                print layer.name,'      ',tag_key_idx,tag_value_idx,keys[tag_key_idx],values[tag_value_idx]
