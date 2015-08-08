#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: audit_street_name.py
Author: Yang Yang
Email: yyangbian@gmail.com
Github: yyangbian
Description:
Audit "v" value in "tag" with "k" value equal to "addr:street".
  - The last word inside the the "v" value is treated as street type. If it
    does not exist in the expected_type list, the street name is displayed
    under "type" category
  - If "v" value has direction such as N, W, East. The "v" value is displayed
    under "direction" category.
  - If "v" value has numbers in it. It is displayed under "digits" category.
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

#Street type is the non-white-space string at the end
street_type_re = re.compile(r'\b\S+\.?\s*$')

expected_type = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Circle",
            "Freeway", "Highway", "Plaza", "Tollway", "Turnpike"]


# (?<!'|\.|-) used to not match for names like Green's Court, Post-N-Paddock
street_dir_re = {
        "North"     : re.compile(r"(?<!'|\.|-)\b(?:N|North)\b\.?", re.IGNORECASE),
        "South"     : re.compile(r"(?<!'|\.|-)\b(?:S|South)\b\.?", re.IGNORECASE),
        "West"      : re.compile(r"(?<!'|\.|-)\b(?:W|West)\b\.?", re.IGNORECASE),
        "East"      : re.compile(r"(?<!'|\.|-)\b(?:E|East)\b\.?", re.IGNORECASE),
        "Northwest" : re.compile(r"(?<!'|\.|-)\b(?:NW|Northwest)\b\.?", re.IGNORECASE),
        "Northeast" : re.compile(r"(?<!'|\.|-)\b(?:NW|Northeast)\b\.?", re.IGNORECASE),
        "Southwest" : re.compile(r"(?<!'|\.|-)\b(?:NW|Southwest)\b\.?", re.IGNORECASE),
        "Southeast" : re.compile(r"(?<!'|\.|-)\b(?:NE|Southeast)\b\.?", re.IGNORECASE),
        }

digits_re = re.compile(r"\d+")

def audit_street_type(street_types, street_name):
    '''Find unexpected types from street_name using street_type_re
    and expected_type
    '''
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_type:
            street_types[street_type].add(street_name)

def audit_street_direction(street_directions, street_name):
    '''Find direction in street_name using street_direction_re
    '''
    for key, regex in street_dir_re.items():
        m = regex.search(street_name)
        if m:
            street_dir = m.group()
            street_dir = street_dir.capitalize()
            street_directions[street_dir].add(street_name)

# Many street names have digits in them, such as I30. For the same road, their
# names are not consistent. For example, I30 may be called Interstate 30, I 30,
# I-30. The goal is to use this method to find all such roads and make a 
# plan to make those names consistent when cleaning the data set
def audit_street_with_digits(street_with_digits, street_name):
    m = digits_re.search(street_name)
    if m:
        digits = m.group()
        street_with_digits[digits].add(street_name)

def is_street_name(elem):
    '''True if the elem attribute "k" value is "addr:street"
    '''
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """Audit street names in the specified osmfile.
    Visit tags with k="addr:street",
    check street type, direction, numbers appeared in street name

    :osmfile: osm file
    :returns: a dict of dict.
              The top level dict has 3 keys: type, direction and digits
              'type' is a dict with street types as key
              'direction' is a dict with direction as key
              'digits' is a dict with numbers shown in the street name as key
    """

    osm_file = open(osmfile, "r", encoding="utf-8")
    street_types = defaultdict(set)
    street_directions = defaultdict(set)
    street_with_digits = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                    audit_street_direction(street_directions, tag.attrib['v'])
                    audit_street_with_digits(
                            street_with_digits, tag.attrib['v'])

        elem.clear()

    return {
            "type"      : street_types,
            "direction" : street_directions,
            "digits"    : street_with_digits
            }

def main(osmfile):
    audit_results = audit(osmfile)
    pprint.pprint(audit_results);

if __name__ == '__main__':
    import sys
    main(sys.argv[1])
