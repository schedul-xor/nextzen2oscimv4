#!/usr/bin/env sh

NEXTZEN_API_KEY=_lQbucvFRf6L7cPYIG1Fdg
TILESIZE=256

# X=1
# Y=1
# Z=1

Z=15
X=29096
Y=12914

MVT_BUFFER_PIXELS=5
OSCIMV4_BUFFER_PIXELS=5

mkdir -p tmp
mkdir -p tmp/mvt
wget -nc --no-check-certificate -O tmp/mvt/${Z}_${X}_${Y}_${MVT_BUFFER_PIXELS}.mvt https://tile.nextzen.org/tilezen/vector/v1/256/all/${Z}/${X}/${Y}.mvt?api_key=${NEXTZEN_API_KEY}

# mkdir -p tmp/oscimv4
# mkdir -p tmp/oscimv4_geojson
# python convert_mvt2oscimv4.py tmp/mvt/${Z}_${X}_${Y}.mvt ${Z} ${X} ${Y} ${TILESIZE} tmp/oscimv4/${Z}_${X}_${Y}.vtm
# python dump_oscim.py tmp/oscimv4/${Z}_${X}_${Y}.vtm ${Z} ${X} ${Y} tmp/oscimv4_geojson/${Z}_${X}_${Y}.json

# Use tippecanoe to decode mvt to GeoJSON
# https://github.com/mapbox/tippecanoe
# https://qiita.com/Kanahiro/items/a9ac8333191aaff27fcc
mkdir -p tmp/mvt2geojson
tippecanoe-decode tmp/mvt/${Z}_${X}_${Y}_${MVT_BUFFER_PIXELS}.mvt ${Z} ${X} ${Y}> tmp/mvt2geojson/${Z}_${X}_${Y}_${MVT_BUFFER_PIXELS}.json
mkdir -p tmp/mvt2geojson2oscimv4
cat tmp/mvt2geojson/${Z}_${X}_${Y}_${MVT_BUFFER_PIXELS}.json | python call_json2oscimv4.py ${Z} ${X} ${Y} ${OSCIMV4_BUFFER_PIXELS} tmp/mvt2geojson2oscimv4/${Z}_${X}_${Y}_${OSCIMV4_BUFFER_PIXELS}.vtm
mkdir -p tmp/mvt2geojson2oscimv42geojson
python dump_oscim.py tmp/mvt2geojson2oscimv4/${Z}_${X}_${Y}_${OSCIMV4_BUFFER_PIXELS}.vtm ${Z} ${X} ${Y} ${OSCIMV4_BUFFER_PIXELS} tmp/mvt2geojson2oscimv42geojson/${Z}_${X}_${Y}.json
