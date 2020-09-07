#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import TileData_v4_pb2
from pyproj import Proj,transform

EPSG3857 = Proj(init='epsg:3857')
EPSG4326 = Proj(init='epsg:4326')

SIZE = 256

SCALE_FACTOR = 20037508.342789244

YES_VALUES = frozenset(['yes','1','true'])
NAME_KEYS = frozenset(['name','name:ja','name:en'])

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

predefined_key_idx = {}
predefined_value_idx = {}
for i in range(len(TAG_PREDEFINED_KEYS)):
    predefined_key = TAG_PREDEFINED_KEYS[i]
    predefined_key_idx[predefined_key] = i
for i in range(len(TAG_PREDEFINED_VALUES)):
    predefined_value = TAG_PREDEFINED_VALUES[i]
    predefined_value_idx[predefined_value] = i

def convert(tile_z,tile_x,tile_y,buffer_pixels,fr):
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

    oscim_tile = TileData_v4_pb2.Data()
    oscim_tile.version = 4
    found_points = []
    found_polygons = []
    found_lines = []
    appending_target = None

    tag2idx = {}
    serialized_tags = []
    oscim_keys = []
    key2oscim_idx = {}
    oscim_values = []
    value2oscim_idx = {}

    def ll2xy(lon,lat):
        lon3857,lat3857 = transform(EPSG4326,EPSG3857,lon,lat)
        rx = float(lon3857-min_lon3857)/float(max_lon3857-min_lon3857)
        ry = float(lat3857-min_lat3857)/float(max_lat3857-min_lat3857)

        rx = rx-0.5
        rx = rx*float(SIZE+buffer_pixels)/float(SIZE)
        rx = rx+0.5
        x = int(rx*4096.0)

        ry = ry-0.5
        ry = -ry*float(SIZE+buffer_pixels)/float(SIZE) # NEGATE!
        ry = ry+0.5
        y = int(ry*4096.0)
        
        return x,y

    def lls2xy(lls):
        abs_xys = []
        for ll in lls:
            lon = ll[0]
            lat = ll[1]
            x,y = ll2xy(lon,lat)
            abs_xys.append([x,y])

        last_x = 0
        last_y = 0
        delta_xys = []
        for x,y in abs_xys:
            dx = x-last_x
            dy = y-last_y
            delta_xys.append([dx,dy])
            last_x = x
            last_y = y

        return delta_xys

    def llss2xy(llss):
        abs_xyss = []
        for lls in llss:
            abs_xys = []
            for ll in lls:
                lon = ll[0]
                lat = ll[1]
                x,y = ll2xy(lon,lat)
                abs_xys.append([x,y])
            abs_xyss.append(abs_xys)

        last_x = 0
        last_y = 0
        delta_xyss = []
        for abs_xys in abs_xyss:
            delta_xys = []
            for x,y in abs_xys:
                dx = x-last_x
                dy = y-last_y
                delta_xys.append([dx,dy])
                last_x = x
                last_y = y
            delta_xyss.append(delta_xys)

        return delta_xyss

    j = json.loads(fr)
    layers = j['features']
    for layer in layers:
        features = layer['features']
        for feature in features:
            tag_idxs_in_feature = []
            properties = feature['properties']

            kv = {}
            for key in properties:
                if key in frozenset(['id','sort_rank','source','min_zoom','surface']): continue
                value = properties[key]
                value = unicode(value)
                kv[key] = value

            # for key in kv.keys():
            #     value = kv[key]

            #     if key == 'kind' and value in frozenset(['earth','cemetery','commercial','forest','grass','industrial']):
            #         key = 'landuse'
            #         value = 'urban'
                    
            #     elif key == 'kind' and value == 'locality':
            #         key = 'boundary'
            #         value = 'administrative'
                    
            #     elif key == 'kind' and value in frozenset(['water','riverbank','ocean']):
            #         key = 'natural'
            #         value = 'water'
            #     if key == 'kind' and value == 'river':
            #         key = 'waterway'
            #         value = 'river'
                    
            #     elif key == 'kind' and value == 'major_road':
            #         key = 'highway'
            #         value = 'trunk'
            #     elif key == 'kind' and value == 'minor_road':
            #         key = 'highway'
            #         value = 'residential'
            #     elif key == 'kind' and value == 'highway':
            #         key = 'highway'
            #         value = 'motorway'
            #     elif key == 'highway' and value == 'residential':
            #         key = 'highway'
            #         value = 'service'
            #     elif key == 'kind' and value in frozenset(['footway','bus_stop','unclassified']):
            #         key = 'highway'

            #     elif key == 'kind' and value in frozenset(['aerodrome','apron','helipad']):
            #         key = 'aeroway'
            #     elif key == 'kind_detail' and value in frozenset (['runway','taxiway']):
            #         key = 'aeroway'

            #     elif key == 'kind' and value in frozenset(['pitch','park','playground','common']):
            #         key = 'leisure'
                    
            #     elif key == 'kind' and value == 'building':
            #         key = 'building'
            #         value = 'yes'
                    
            #     elif key == 'kind_detail' and value == 'rail':
            #         key = 'railway'
            #     elif key == 'kind_detail' and value == 'subway':
            #         key = 'railway'
            #     elif key == 'kind' and value == 'station':
            #         key = 'railway'
                    
            #     elif key == 'kind' and value in frozenset(['viewpoint','information','park']):
            #         key = 'tourism'

            #     elif key == 'is_tunnel' and value == 'True':
            #         key = 'tunnel'
            #         value = 'yes'
                    
            #     elif key == 'is_bridge' and value == 'True':
            #         key = 'bridge'
            #         value = 'yes'

            #     elif key == 'kind' and value in frozenset([
            #             'bar',
            #             'bicycle',
            #             'books',
            #             'cafe',
            #             'clothes',
            #             'convenience',
            #             'dry_cleaning',
            #             'fast_food',
            #             'parking',
            #             'pharmacy',
            #             'place_of_worship',
            #             'police',
            #             'post_office',
            #             'pub',
            #             'restaurant',
            #             'school',
            #             'supermarket',
            #             'university',
            #     ]):
            #         key = 'amenity'

            names_kv = {}
            for key in kv.keys():
                value = kv[key]
                if key in NAME_KEYS:
                    names_kv[key] = value

            fixed_kv = {}
            
            if kv.has_key('oneway') and kv['oneway'].lower() in YES_VALUES:
                fixed_kv['oneway'] = 'yes'
            if kv.has_key('area') and kv['area'].lower() in YES_VALUES:
                fixed_kv['area'] = 'yes'
            elif kv.has_key('is_tunnel') and kv['is_tunnel'].lower() in YES_VALUES:
                fixed_kv['tunnel'] = 'yes'
            elif kv.has_key('is_bridge') and kv['is_bridge'].lower() in YES_VALUES:
                fixed_kv['bridge'] = 'yes'

            if kv.has_key('leisure'):
                leisure = kv['leisure']
                fixed_kv['leisure'] = leisure
                    
            if kv.has_key('natural'):
                natural = kv['natural']
                if natural in frozenset(['village_green','meadow']):
                    fixed_kv['landuse'] = natural
                elif natural == 'mountain_range': pass
                else:
                    fixed_kv['natural'] = natural
                    
            if kv.has_key('landuse'):
                landuse = kv['landuse']
                if landuse in frozenset(['park','natural_reserve']):
                    fixed_kv['leisure'] = landuse
                elif landuse == 'field':
                    fixed_kv['landuse'] = 'farmland'
                elif landuse in frozenset(['grassland','scrub']):
                    fixed_kv['natural'] = landuse
                else:
                    fixed_kv['landuse'] = landuse
                
            for explicit_kind in frozenset(['waterway']):
                if kv.has_key(explicit_kind): fixed_kv[explicit_kind] = kv[explicit_kind]

            if kv.has_key('kind'):
                kind_value = kv['kind']
                
                if kind_value == 'building':
                    fixed_kv['building'] = 'yes'
                    
                elif kind_value in frozenset(['earth']):
                    fixed_kv['landuse'] = 'urban'

                # REGION
                elif kind_value == 'locality':
                    fixed_kv['boundary'] = 'administrative'

                # WATER
                elif kind_value in frozenset(['water','riverbank','ocean']):
                    fixed_kv['natural'] = 'water'
                elif kind_value == 'lake;pond':
                    fixed_kv['water'] = 'pond'
                elif kind_value == 'river':
                    fixed_kv['waterway'] = 'river'

                # ROADS
                elif kind_value == 'major_road':
                    if kv.has_key('kind_detail'):
                        fixed_kv['highway'] = kv['kind_detail']
                    else:
                        fixed_kv['highway'] = 'trunk'
                elif kind_value == 'minor_road':
                    fixed_kv['highway'] = 'residential'
                elif kind_value == 'highway':
                    fixed_kv['highway'] = 'motorway'
                elif kind_value == 'residential':
                    fixed_kv['highway'] = 'service'
                elif kind_value in frozenset(['footway','bus_stop','unclassified']):
                    fixed_kv['highway'] = kind_value

                # RAILS
                elif kind_value in frozenset(['rail','subway','station']):
                    fixed_kv['railway'] = kind_value
                    
                # AIR
                elif kind_value in frozenset(['aerodrome','apron','helipad']):
                    fixed_kv['aeroway'] = kind_value

                # PATH
                elif kind_value == 'path':
                    if kv.has_key('kind_detail'):
                        kind_detail = kv['kind_detail']
                        if kind_detail == 'footway':
                            fixed_kv['highway'] = 'footway'
                        elif kind_detail == 'steps':
                            fixed_kv['highway'] = 'steps'
                        elif kind_detail == 'pedestrian':
                            fixed_kv['highway'] = 'footway'

                elif kind_value in frozenset(['pitch','park','playground','common','garden']):
                    fixed_kv['leisure'] = kind_value

                elif kind_value in frozenset(['viewpoint','information','park']):
                    fixed_kv['tourism'] = kind_value

                elif kind_value in frozenset([
                        'bar',
                        'bicycle',
                        'books',
                        'cafe',
                        'clothes',
                        'convenience',
                        'dry_cleaning',
                        'fast_food',
                        'grave_yard',
                        'parking',
                        'pharmacy',
                        'place_of_worship',
                        'police',
                        'post_office',
                        'pub',
                        'restaurant',
                        'school',
                        'supermarket',
                        'university',
                ]):
                    fixed_kv['amenity'] = kind_value
            
            merged_kv = {}
            for key in names_kv: merged_kv[key] = names_kv[key]
            for key in fixed_kv: merged_kv[key] = fixed_kv[key]
            
            for key in merged_kv.keys():
                value = merged_kv[key]
                
                if key in predefined_key_idx:
                    key_idx = predefined_key_idx[key]
                else:
                    if key in key2oscim_idx:
                        key_idx = key2oscim_idx[key]
                    else:
                        key_idx = len(oscim_keys)
                        key2oscim_idx[key] = key_idx
                        oscim_keys.append(key)
                    key_idx = key_idx+256

                if value in predefined_value_idx:
                    value_idx = predefined_value_idx[value]
                else:
                    if value in value2oscim_idx:
                        value_idx = value2oscim_idx[value]
                    else:
                        value_idx = len(oscim_values)
                        value2oscim_idx[value] = value_idx
                        oscim_values.append(value)
                    value_idx = value_idx+256

                tag = (key_idx,value_idx)
                if tag in tag2idx:
                    tag_idx = tag2idx[tag]
                else:
                    tag_idx = len(serialized_tags)/2
                    tag2idx[tag] = tag_idx
                    serialized_tags.append(key_idx)
                    serialized_tags.append(value_idx)
                tag_idxs_in_feature.append(tag_idx)

            geometry = feature['geometry']
            geometry_type = geometry['type']
            c = geometry['coordinates']

            if geometry_type == 'Point':
                oscim_element = TileData_v4_pb2.Data.Element()
                oscim_element.num_tags = len(tag_idxs_in_feature)
                oscim_element.tags.extend(tag_idxs_in_feature)

                x,y = ll2xy(c[0],c[1])
                oscim_element.coordinates.extend([x,y])
                found_points.append(oscim_element)

            elif geometry_type == 'MultiPoint':
                for cp in c:
                    oscim_element = TileData_v4_pb2.Data.Element()
                    oscim_element.num_tags = len(tag_idxs_in_feature)
                    oscim_element.tags.extend(tag_idxs_in_feature)

                    x,y = ll2xy(cp[0],cp[1])
                    oscim_element.coordinates.extend([x,y])
                    found_points.append(oscim_element)

            elif geometry_type == 'LineString':
                oscim_element = TileData_v4_pb2.Data.Element()
                oscim_element.num_tags = len(tag_idxs_in_feature)
                oscim_element.tags.extend(tag_idxs_in_feature)

                delta_xys = lls2xy(c)
                oscim_element.num_indices = 1
                oscim_element.indices.extend([len(delta_xys)])
                flat_xys = []
                for x,y in delta_xys:
                    flat_xys.append(x)
                    flat_xys.append(y)
                oscim_element.coordinates.extend(flat_xys)
                found_lines.append(oscim_element)

            elif geometry_type == 'MultiLineString':
                for cp in c:
                    oscim_element = TileData_v4_pb2.Data.Element()
                    oscim_element.num_tags = len(tag_idxs_in_feature)
                    oscim_element.tags.extend(tag_idxs_in_feature)

                    delta_xys = lls2xy(cp)
                    oscim_element.indices.extend([len(delta_xys)])
                    oscim_element.num_indices = 1
                    flat_xys = []
                    for x,y in delta_xys:
                        flat_xys.append(x)
                        flat_xys.append(y)
                    oscim_element.coordinates.extend(flat_xys)
                    found_lines.append(oscim_element)

            elif geometry_type == 'Polygon':
                oscim_element = TileData_v4_pb2.Data.Element()
                oscim_element.num_tags = len(tag_idxs_in_feature)
                oscim_element.tags.extend(tag_idxs_in_feature)

                delta_xyss = llss2xy(c)
                indices = []
                for delta_xys in delta_xyss:
                    indices.append(len(delta_xys))
                oscim_element.indices.extend(indices)
                oscim_element.num_indices = len(indices)
                flat_xys = []
                for delta_xys in delta_xyss:
                    for x,y in delta_xys:
                        flat_xys.append(x)
                        flat_xys.append(y)
                oscim_element.coordinates.extend(flat_xys)
                found_polygons.append(oscim_element)

            elif geometry_type == 'MultiPolygon':
                for cp in c:
                    oscim_element = TileData_v4_pb2.Data.Element()
                    oscim_element.num_tags = len(tag_idxs_in_feature)
                    oscim_element.tags.extend(tag_idxs_in_feature)

                    delta_xyss = llss2xy(cp)
                    indices = []
                    for delta_xys in delta_xyss:
                        indices.append(len(delta_xys))
                    oscim_element.indices.extend(indices)
                    oscim_element.num_indices = len(indices)
                    flat_xys = []
                    for delta_xys in delta_xyss:
                        for x,y in delta_xys:
                            flat_xys.append(x)
                            flat_xys.append(y)
                    oscim_element.coordinates.extend(flat_xys)
                    found_polygons.append(oscim_element)

    if len(found_points) > 0: oscim_tile.points.extend(found_points)
    if len(found_polygons) > 0: oscim_tile.polygons.extend(found_polygons)
    if len(found_lines) > 0: oscim_tile.lines.extend(found_lines)

    oscim_tile.num_tags = len(serialized_tags)/2
    oscim_tile.tags.extend(serialized_tags)
    oscim_tile.keys.extend(oscim_keys)
    oscim_tile.num_keys = len(oscim_keys)
    oscim_tile.values.extend(oscim_values)
    oscim_tile.num_vals = len(oscim_values)

    return b'0123'+oscim_tile.SerializeToString()
