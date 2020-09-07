#!/usr/bin/env sh

# X=0
# Y=0
# Z=0

Z=$1
X=$2
Y=$3
OSCIMV4_BUFFER_PIXELS=0 # UNUSED

mkdir -p tmp
mkdir -p tmp/generated_oscimv4
mkdir -p tmp/generated_oscimv4_geojson
#wget -nc --no-check-certificate -O tmp/generated_oscimv4/${Z}_${X}_${Y}.vtm http://tile0.ogiqvo.com/tiles/oscimv4/${Z}/${X}/${Y}.vtm
rm -fr tmp/generated_oscimv4/${Z}_${X}_${Y}_${OSCIMV4_BUFFER_PIXELS}.vtm
wget --no-check-certificate -O tmp/generated_oscimv4/${Z}_${X}_${Y}_${OSCIMV4_BUFFER_PIXELS}.vtm http://tile0.ogiqvo.com/tiles/oscimv4/${Z}/${X}/${Y}.vtm

#python dump_oscim.py tmp/oscimv4/${Z}_${X}_${Y}.vtm
python dump_oscim.py tmp/generated_oscimv4/${Z}_${X}_${Y}_${OSCIMV4_BUFFER_PIXELS}.vtm ${Z} ${X} ${Y} ${OSCIMV4_BUFFER_PIXELS} tmp/generated_oscimv4_geojson/${Z}_${X}_${Y}.json
