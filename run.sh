#!/usr/bin/env sh

set -e

TARGETTYPE=mvt
TILESIZE=256

Z=$1
X=$2
Y=$3

MVT_BUFFER_PIXELS=5
OSCIMV4_BUFFER_PIXELS=5

MVT_URL=http://tile0.ogiqvo.com:22380/maps/osm/${Z}/${X}/${Y}.pbf
#MVT_URL=http://localhost:22380/maps/osm/${Z}/${X}/${Y}.pbf

mkdir -p tmp
mkdir -p tmp/${TARGETTYPE}
wget -nc --no-check-certificate -O tmp/${TARGETTYPE}/${Z}_${X}_${Y}_${MVT_BUFFER_PIXELS}.mvt ${MVT_URL}

# Use tippecanoe to decode mvt to GeoJSON
# https://github.com/mapbox/tippecanoe
# https://qiita.com/Kanahiro/items/a9ac8333191aaff27fcc
mkdir -p tmp/${TARGETTYPE}2geojson
tippecanoe-decode tmp/${TARGETTYPE}/${Z}_${X}_${Y}_${MVT_BUFFER_PIXELS}.mvt ${Z} ${X} ${Y}> tmp/${TARGETTYPE}2geojson/${Z}_${X}_${Y}_${MVT_BUFFER_PIXELS}.json
mkdir -p tmp/${TARGETTYPE}2geojson2oscimv4
#cat tmp/${TARGETTYPE}2geojson/${Z}_${X}_${Y}_${MVT_BUFFER_PIXELS}.json | python3 call_${TARGETTYPE}json2oscimv4.py ${Z} ${X} ${Y} ${OSCIMV4_BUFFER_PIXELS} tmp/${TARGETTYPE}2geojson2oscimv4/${Z}_${X}_${Y}_${OSCIMV4_BUFFER_PIXELS}.vtm
cat tmp/${TARGETTYPE}2geojson/${Z}_${X}_${Y}_${MVT_BUFFER_PIXELS}.json | python3 call_${TARGETTYPE}json2oscimv4.py ${Z} ${X} ${Y} ${OSCIMV4_BUFFER_PIXELS} tmp/${TARGETTYPE}2geojson2oscimv4/${Z}_${X}_${Y}_${OSCIMV4_BUFFER_PIXELS}.vtm
mkdir -p tmp/${TARGETTYPE}2geojson2oscimv42geojson
python3 dump_oscim.py tmp/${TARGETTYPE}2geojson2oscimv4/${Z}_${X}_${Y}_${OSCIMV4_BUFFER_PIXELS}.vtm ${Z} ${X} ${Y} ${OSCIMV4_BUFFER_PIXELS} tmp/${TARGETTYPE}2geojson2oscimv42geojson/${Z}_${X}_${Y}.json
