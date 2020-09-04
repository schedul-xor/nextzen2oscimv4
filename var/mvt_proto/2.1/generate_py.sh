#!/usr/bin/env sh

protoc -I=. --python_out=. vector_tile.proto
mv -f vector_tile_pb2.py ../../..
