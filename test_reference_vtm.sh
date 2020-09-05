#!/usr/bin/env sh

X=0
Y=0
Z=0

# Z=16
# X=58210
# Y=25812

mkdir -p tmp
mkdir -p tmp/referencing_oscimv4
#wget --no-check-certificate -O tmp/referencing_oscimv4/${Z}_${X}_${Y}.vtm http://tile0.ogiqvo.com/tiles/oscimv4/${Z}/${X}/${Y}.vtm
#wget --no-check-certificate -O tmp/referencing_oscimv4/${Z}_${X}_${Y}.vtm http://oscimproxy0.ogiqvo.com/tiles/vtm/${Z}/${X}/${Y}.vtm

#python dump_oscim.py tmp/oscimv4/${Z}_${X}_${Y}.vtm
python dump_oscim.py tmp/referencing_oscimv4/${Z}_${X}_${Y}.vtm
