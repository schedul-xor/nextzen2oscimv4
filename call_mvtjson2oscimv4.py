#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import mvtjson2oscimv4 # In this directory

tile_z = int(sys.argv[1])
tile_x = int(sys.argv[2])
tile_y = int(sys.argv[3])
oscimv4_buffer_pixels = int(sys.argv[4])
out_vtm_path = sys.argv[5]

oscimv4_binary = mvtjson2oscimv4.convert(tile_z,tile_x,tile_y,oscimv4_buffer_pixels,sys.stdin.read())

with open(out_vtm_path,'wb') as fw:
    fw.write(oscimv4_binary)
