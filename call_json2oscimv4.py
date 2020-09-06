#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import json2oscimv4 # In this directory

tile_z = int(sys.argv[1])
tile_x = int(sys.argv[2])
tile_y = int(sys.argv[3])
out_vtm_path = sys.argv[4]

oscimv4_binary = json2oscimv4.convert(tile_z,tile_x,tile_y,sys.stdin.read())

with open(out_vtm_path,'wb') as fw:
    fw.write(oscimv4_binary)
