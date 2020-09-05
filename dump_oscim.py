#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import TileData_v4_pb2
from pyproj import Proj,transform
import json

EPSG3857 = Proj(init='epsg:3857')
EPSG4326 = Proj(init='epsg:4326')

SIZE = 256
SCALE_FACTOR = 20037508.342789244

in_vtm_path = sys.argv[1]
tile_z = int(sys.argv[2])
tile_x = int(sys.argv[3])
tile_y = int(sys.argv[4])
out_json_path = sys.argv[5]

paz = 20037508.342789244 / 256 / (2 ** tile_z)
tile_x = tile_x*SIZE
tile_y = tile_y*SIZE
center = (SIZE << tile_z) >> 1
min_lat3857 = ((center - (tile_y+SIZE+paz))/center)*SCALE_FACTOR
max_lat3857 = ((center - (tile_y-paz))/center)*SCALE_FACTOR
min_lon3857 = (((tile_x-paz)-center)/center)*SCALE_FACTOR
max_lon3857 = (((tile_x+SIZE+paz)-center)/center)*SCALE_FACTOR

min_lon4326,min_lat4326 = transform(EPSG3857,EPSG4326,min_lon3857,min_lat3857)
max_lon4326,max_lat4326 = transform(EPSG3857,EPSG4326,max_lon3857,max_lat3857)

def xy2ll(x,y):
    rx = float(x)/4096.0
    ry = float(y)/4096.0
    lon3857 = min_lon3857+(max_lon3857-min_lon3857)*rx
    lat3857 = min_lat3857+(max_lat3857-min_lat3857)*(1.0-ry)
    lon4326,lat4326 = transform(EPSG3857,EPSG4326,lon3857,lat3857)
    return [lon4326,lat4326]

TAG_PREDEFINED_KEYS = [
            "access",
            "addr:housename",
            "addr:housenumber",
            "addr:interpolation",
            "admin_level",
            "aerialway",
            "aeroway",
            "amenity",
            "area",
            "barrier",
            "bicycle",
            "brand",
            "bridge",
            "boundary",
            "building",
            "construction",
            "covered",
            "culvert",
            "cutting",
            "denomination",
            "disused",
            "embankment",
            "foot",
            "generator:source",
            "harbour",
            "highway",
            "historic",
            "horse",
            "intermittent",
            "junction",
            "landuse",
            "layer",
            "leisure",
            "lock",
            "man_made",
            "military",
            "motorcar",
            "name",
            "natural",
            "oneway",
            "operator",
            "population",
            "power",
            "power_source",
            "place",
            "railway",
            "ref",
            "religion",
            "route",
            "service",
            "shop",
            "sport",
            "surface",
            "toll",
            "tourism",
            "tower:type",
            "tracktype",
            "tunnel",
            "water",
            "waterway",
            "wetland",
            "width",
            "wood",

            "height",
            "min_height",
            "roof:shape",
            "roof:height",
            "rank"
]

TAG_PREDEFINED_VALUES = [
            "yes",
            "residential",
            "service",
            "unclassified",
            "stream",
            "track",
            "water",
            "footway",
            "tertiary",
            "private",
            "tree",
            "path",
            "forest",
            "secondary",
            "house",
            "no",
            "asphalt",
            "wood",
            "grass",
            "paved",
            "primary",
            "unpaved",
            "bus_stop",
            "parking",
            "parking_aisle",
            "rail",
            "driveway",
            "8",
            "administrative",
            "locality",
            "turning_circle",
            "crossing",
            "village",
            "fence",
            "grade2",
            "coastline",
            "grade3",
            "farmland",
            "hamlet",
            "hut",
            "meadow",
            "wetland",
            "cycleway",
            "river",
            "school",
            "trunk",
            "gravel",
            "place_of_worship",
            "farm",
            "grade1",
            "traffic_signals",
            "wall",
            "garage",
            "gate",
            "motorway",
            "living_street",
            "pitch",
            "grade4",
            "industrial",
            "road",
            "ground",
            "scrub",
            "motorway_link",
            "steps",
            "ditch",
            "swimming_pool",
            "grade5",
            "park",
            "apartments",
            "restaurant",
            "designated",
            "bench",
            "survey_point",
            "pedestrian",
            "hedge",
            "reservoir",
            "riverbank",
            "alley",
            "farmyard",
            "peak",
            "level_crossing",
            "roof",
            "dirt",
            "drain",
            "garages",
            "entrance",
            "street_lamp",
            "deciduous",
            "fuel",
            "trunk_link",
            "information",
            "playground",
            "supermarket",
            "primary_link",
            "concrete",
            "mixed",
            "permissive",
            "orchard",
            "grave_yard",
            "canal",
            "garden",
            "spur",
            "paving_stones",
            "rock",
            "bollard",
            "convenience",
            "cemetery",
            "post_box",
            "commercial",
            "pier",
            "bank",
            "hotel",
            "cliff",
            "retail",
            "construction",
            "-1",
            "fast_food",
            "coniferous",
            "cafe",
            "6",
            "kindergarten",
            "tower",
            "hospital",
            "yard",
            "sand",
            "public_building",
            "cobblestone",
            "destination",
            "island",
            "abandoned",
            "vineyard",
            "recycling",
            "agricultural",
            "isolated_dwelling",
            "pharmacy",
            "post_office",
            "motorway_junction",
            "pub",
            "allotments",
            "dam",
            "secondary_link",
            "lift_gate",
            "siding",
            "stop",
            "main",
            "farm_auxiliary",
            "quarry",
            "10",
            "station",
            "platform",
            "taxiway",
            "limited",
            "sports_centre",
            "cutline",
            "detached",
            "storage_tank",
            "basin",
            "bicycle_parking",
            "telephone",
            "terrace",
            "town",
            "suburb",
            "bus",
            "compacted",
            "toilets",
            "heath",
            "works",
            "tram",
            "beach",
            "culvert",
            "fire_station",
            "recreation_ground",
            "bakery",
            "police",
            "atm",
            "clothes",
            "tertiary_link",
            "waste_basket",
            "attraction",
            "viewpoint",
            "bicycle",
            "church",
            "shelter",
            "drinking_water",
            "marsh",
            "picnic_site",
            "hairdresser",
            "bridleway",
            "retaining_wall",
            "buffer_stop",
            "nature_reserve",
            "village_green",
            "university",
            "1",
            "bar",
            "townhall",
            "mini_roundabout",
            "camp_site",
            "aerodrome",
            "stile",
            "9",
            "car_repair",
            "parking_space",
            "library",
            "pipeline",
            "true",
            "cycle_barrier",
            "4",
            "museum",
            "spring",
            "hunting_stand",
            "disused",
            "car",
            "tram_stop",
            "land",
            "fountain",
            "hiking",
            "manufacture",
            "vending_machine",
            "kiosk",
            "swamp",
            "unknown",
            "7",
            "islet",
            "shed",
            "switch",
            "rapids",
            "office",
            "bay",
            "proposed",
            "common",
            "weir",
            "grassland",
            "customers",
            "social_facility",
            "hangar",
            "doctors",
            "stadium",
            "give_way",
            "greenhouse",
            "guest_house",
            "viaduct",
            "doityourself",
            "runway",
            "bus_station",
            "water_tower",
            "golf_course",
            "conservation",
            "block",
            "college",
            "wastewater_plant",
            "subway",
            "halt",
            "forestry",
            "florist",
            "butcher"
]

features = []
geojson = {
    'type':'FeatureCollection',
    'name':'demo',
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
    'features':features
}

with open(in_vtm_path,'rb') as fr:
    content = fr.read()[4:]
    tile = TileData_v4_pb2.Data()
    tile.ParseFromString(content)

    print 'Version',tile.version

    print 'Tag count',tile.num_tags
    assert(tile.num_tags == len(tile.tags)/2)
    print 'Key count',tile.num_keys
    assert(tile.num_keys == len(tile.keys))
    print 'Value count',tile.num_vals
    assert(tile.num_vals == len(tile.values))

    keys = tile.keys
    values = tile.values
#    print 'Keys',len(keys),keys
#    print 'Values',len(values),values
    
    raw_tags = tile.tags
#    print 'raw tags',len(raw_tags),raw_tags
    tags = []
    for idx in range(len(raw_tags)/2):
        key_idx = raw_tags[idx*2]
        if key_idx < 256:
            key = TAG_PREDEFINED_KEYS[key_idx]
        else:
            key_idx = key_idx-256
            key = keys[key_idx]
            
        value_idx = raw_tags[idx*2+1]
        if value_idx < 256:
            value = TAG_PREDEFINED_VALUES[value_idx]
        else:
            value_idx = value_idx-256
            value = values[value_idx]
            
        tags.append((key,value))

    for geoobjs,geotype in [
            (tile.polygons,'POLYGON'),
            (tile.points,'POINT'),
            (tile.lines,'LINE')
    ]:
        for geoobj in geoobjs:
            layer = geoobj.layer

#            assert(geoobj.num_indices == len(geoobj.indices))
            assert(geoobj.num_tags == len(geoobj.tags))

            geojson_tags = {}
            for tag_idx in geoobj.tags:
                key,value = tags[tag_idx]
                geojson_tags[key] = value

            c = geoobj.coordinates
            if geotype == 'LINE':
                last_x = 0
                last_y = 0
                index_offset = 0
                for index in geoobj.indices:
                    new_geoms = []
                    for i in range(index):
                        dx = c[(index_offset+i)*2]
                        dy = c[(index_offset+i)*2+1]
                        x = last_x+dx
                        y = last_y+dy
                        last_x = x
                        last_y = y
                        ll = xy2ll(x,y)
                        new_geoms.append(ll)
                    features.append({
                        'type':'Feature',
                        'properties':geojson_tags,
                        'geometry':{
                            'type':'LineString',
                            'coordinates':new_geoms
                        }
                    })
                    index_offset = index_offset+index
                    
            elif geotype == 'POLYGON':
                last_x = 0
                last_y = 0
                index_offset = 0
                found_polygons = []
                is_first_polygon = True
                for index in geoobj.indices:
                    if is_first_polygon:
                        # It's first polygon
                        found_polygons.append([[]])
                        is_first_polygon = False

                    elif index == 0:
                        # It's a new polygon
                        is_first_polygon = True
                        continue
                        
                    else:
                        # It's a hole
                        found_polygons[-1].append([])

                    first_ll = None
                    for i in range(index):
                        dx = c[(index_offset+i)*2]
                        dy = c[(index_offset+i)*2+1]
                        x = last_x+dx
                        y = last_y+dy
                        last_x = x
                        last_y = y
                        ll = xy2ll(x,y)
                        if first_ll == None:
                            first_ll = ll
                        found_polygons[-1][-1].append(ll)
                    found_polygons[-1][-1].append(first_ll)
                    index_offset = index_offset+index

                for found_polygon in found_polygons:
                    features.append({
                        'type':'Feature',
                        'properties':geojson_tags,
                        'geometry':{
                            'type':'Polygon',
                            'coordinates':found_polygon
                        }
                    })

            elif geotype == 'POINT':
                assert(len(geoobj.indices) == 0)
                dx = c[0]
                dy = c[1]
                ll = xy2ll(dx,dy)
                features.append({
                    'type':'Feature',
                    'properties':geojson_tags,
                    'geometry':{
                        'type':'Point',
                        'coordinates':ll
                    }
                })

with open(out_json_path,'w') as fw:
    fw.write(json.dumps(geojson))
