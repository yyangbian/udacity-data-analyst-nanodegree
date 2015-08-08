#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: position_range.py
Author: Yang Yang
Email: yyangbian@gmail.com
Github: yyangbian
Description: Get min and max of lattitude and longitude from the osm file
"""
import xml.etree.cElementTree as ET
import pprint

# min/max values is from bound tag in the osm file
MIN_LAT = 32.166
MAX_LAT = 33.431

MIN_LON = -97.789
MAX_LON = -96.113


def audit_position(osm_file):
    lon = []
    lat = []
    for event, elem in ET.iterparse(osm_file):
        if elem.tag == "node" or elem.tag == "way":
            if "lat" in elem.attrib:
                lat.append(float(elem.attrib["lat"]))
            if "lon" in elem.attrib:
                lon.append(float(elem.attrib["lon"]))

        elem.clear()

    return { "lat": [min(lat), max(lat)],
             "lon": [min(lon), max(lon)]
            }



if __name__ == "__main__":
    import sys
    result = audit_position(sys.argv[1])
    pprint.pprint(result)
