#!/usr/bin/env sh

NEXTZEN_API_KEY=_lQbucvFRf6L7cPYIG1Fdg
# X=1
# Y=1
# Z=1

Z=16
X=58210
Y=25812

mkdir -p tmp
mkdir -p tmp/mvt
#wget --no-check-certificate -O tmp/mvt/${Z}_${X}_${Y}.mvt https://tile.nextzen.org/tilezen/vector/v1/256/all/${Z}/${X}/${Y}.mvt?api_key=${NEXTZEN_API_KEY}

mkdir -p tmp/oscimv4
python convert_mvt2oscimv4.py tmp/mvt/${Z}_${X}_${Y}.mvt ${Z} ${X} ${Y} tmp/oscimv4/${Z}_${X}_${Y}.vtm
