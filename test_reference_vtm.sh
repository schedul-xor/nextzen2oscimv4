#!/usr/bin/env sh

# X=0
# Y=0
# Z=0

Z=14
X=14552
Y=6455
OSCIMV4_BUFFER_PIXELS=10

mkdir -p tmp
mkdir -p tmp/referencing_oscimv4
mkdir -p tmp/referencing_oscimv4_geojson
#wget -nc --no-check-certificate -O tmp/referencing_oscimv4/${Z}_${X}_${Y}.vtm http://tile0.ogiqvo.com/tiles/oscimv4/${Z}/${X}/${Y}.vtm
wget -nc --no-check-certificate -O tmp/referencing_oscimv4/${Z}_${X}_${Y}_${OSCIMV4_BUFFER_PIXELS}.vtm http://oscimproxy0.ogiqvo.com/tiles/vtm/${Z}/${X}/${Y}.vtm

#python dump_oscim.py tmp/oscimv4/${Z}_${X}_${Y}.vtm
python dump_oscim.py tmp/referencing_oscimv4/${Z}_${X}_${Y}_${OSCIMV4_BUFFER_PIXELS}.vtm ${Z} ${X} ${Y} ${OSCIMV4_BUFFER_PIXELS} tmp/referencing_oscimv4_geojson/${Z}_${X}_${Y}.json
