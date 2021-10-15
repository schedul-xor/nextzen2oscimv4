#!/usr/bin/env sh

protoc -I=. --python_out=. TileData_v4.proto
