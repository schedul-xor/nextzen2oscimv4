#!/usr/bin/env sh

NEXTZEN_API_KEY=_lQbucvFRf6L7cPYIG1Fdg
X=0
Y=0
Z=0

mkdir -p tmp
mkdir -p tmp/mvt
#wget -o tmp/mvt/${Z}_${X}_${Y}.mvt https://tile.neztzen.com/tilezen/vector/v1/{tilesize}/{layers}/${Z}/${X}/${Y}.mvt?api_key=${NEXTZEN_API_KEY}

mkdir -p tmp/oscimv4
python convert_mvt2oscimv4.py tmp/mvt/${Z}_${X}_${Y}.mvt
