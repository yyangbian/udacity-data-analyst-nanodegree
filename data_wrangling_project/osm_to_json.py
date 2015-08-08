#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: osm_to_json.py
Author: Yang Yang
Email: yyangbian@gmail.com
Github: yyangbian
Description:
Convert osm file to a json file with a list of dictionaries that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

The following things are done during conversion:
- 2 types of top level tags: "node" and "way", are processed
- all attributes of "node" and "way" are be turned into regular
  key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array
      are floating numbers instead of strings.
- Ignore second level tag if its "k" value contains problematic characters
- if second level tag "k" value starts with "addr:", it is added to
  a dictionary "address".
- if second level tag "k" value starts with "addr:" and there is a second ":",
  it is ignored
- if second level tag "k" value does not start with "addr:", but contains ":",
  process it the same as any other tag.
- for tags with other "k" value, treat it the same as other tags
- some tag "k" value is "type", to avoid overwriting element type (node or way),
  rename it to tag_type

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]

"""

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

# if true, name conversion will be printed to screen
__DEBUG__ = True

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]

TAGS_TO_PROCESS = ['node', 'way']

def get_created(element):
    """Get "created" dictionary from top level element.
    {
      "version"   :  "2",
      "changeset" :  "17206049",
      "timestamp" :  "2013-08-03T16:43:42Z",
      "user"      :  "linuxUser16",
      "uid"       :  "1219059"
    }

    :element: xml.etree.ElementTree.Element object
    :returns: a dictionary with info related to "created" (or empty dictionary)

    """
    created = {}
    for attr in element.attrib:
        if attr in CREATED:
            created[attr] = element.attrib[attr]

    return created

def get_pos(element):
    """Get position information [lattitude, longitude] related to element
        [41.9757030, -87.6921867]

    :element: xml.etree.ElementTree.Element object
    :returns: a 2-element list [lattitude, longitude];
              if either lon or lat does not exist, None is returned
    """
    lat, lon = None, None
    for attr in element.attrib:
        if attr == "lat":
            lat = float(element.attrib[attr])
        elif attr == "lon":
            lon = float(element.attrib[attr])
    return None if lat is None or lon is None else [lat, lon]

def get_address(element):
    """Get "address" dictionary
        {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        }
        from second level tags with "k" value starting with "addr:"
        Ignore the tag if there is a second ":" in its "k" value

    :element: xml.etree.ElementTree.Element object
    :returns: a dictionary with address or empty dictionary

    """
    address = {}
    for tag in element.iter("tag"):
        key, value = tag.attrib["k"], tag.attrib["v"]
        if problemchars.search(key):
            continue
        elif key.startswith("addr:"):
            key_list = key.split(":")
            if len(key_list) == 2:
                address[key_list[1]] = value

    return address

def get_nd_refs(element):
    """Get nd_ref list for "way" element

    <nd ref="305896090"/>
    <nd ref="1719825889"/>

    should be turned into
    "node_refs": ["305896090", "1719825889"]

    :element: xml.etree.ElementTree.Element object
    :returns: a list of reference node for tag "way"
              or an empty list if not existing

    """
    node_refs = []
    for nd in element.iter("nd"):
        node_refs.append(nd.attrib["ref"])
    return node_refs

def shape_element(element):
    """Convert top level tags "node" and "way" to proper dictionary.
    The element is cleard after processing to save memory.

    :element: xml.etree.ElementTree.Element object
    :returns: a dictionary for "node" or "way";
              an empty dictionary for other top level tags

    """
    node = {}

    node["type"] = "node" if element.tag == "node" else "way"

    created = get_created(element)
    if created:
        node["created"] = created

    pos = get_pos(element)
    if pos is not None:
        node["pos"] = pos

    address = get_address(element)
    if address:
        node["address"] = address

    if element.tag == "way":
        nd_refs = get_nd_refs(element)
        if nd_refs:
            node["node_refs"] = nd_refs


    #check if there are other attributes in "node" and "way" tag
    for attr in element.attrib:
        if attr not in CREATED and attr != "lat" and attr != "lon":
            node[attr] = element.attrib[attr]

    #process second level tags
    #ignore if it is address or has problematic characters in "k" value
    #some tag "k" value is "type", to avoid overwriting element type,
    #rename it to tag_type
    for tag in element.iter("tag"):
        key, value = tag.attrib["k"], tag.attrib["v"]
        if problemchars.search(key):
            continue
        if key.startswith("addr:"):
            continue
        if key == "type":
            key = "tag_type"
        node[key] = value

    return node

def process_map(osm_file, json_file, pretty=True):
    """Convert "node" and "way" tags in osm_file to json stored in json_file.

    :osm_file: original osm data
    :json_file: file to store json data
    :pretty": write json data to file in a human readable format if True

    """
    with open(json_file, "w", encoding="utf-8") as fo:

        context = ET.iterparse(osm_file, events=('start', 'end'))

        _, root = next(context)

        #for _, element in ET.iterparse(osm_file):
        for event, element in context:
            if event == 'end' and element.tag in TAGS_TO_PROCESS:
                el = shape_element(element)
                if el:
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")
                root.clear()

if __name__ == "__main__":
    import sys
    osm_file, json_file= sys.argv[1:]
    process_map(osm_file, json_file)
