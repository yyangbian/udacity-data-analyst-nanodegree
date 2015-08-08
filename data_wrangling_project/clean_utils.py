#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: clean_utils.py
Author: Yang Yang
Email: yyangbian@gmail.com
Github: yyangbian
Description:
Define methods/regular expressions used to clean osm data
"""


import xml.etree.cElementTree as ET
import re

# level-one tags need to be processed
TAGS_TO_PROCESS = ["node", "way"]

# defines how to clean the "tag" data for some special cases
# key -- ("k" value, "v" value) of a "tag" element in original osm file
# value -- a list of ("k" value, "v" value) to be added as "tag" element
special_case_mapping = {
        ("addr:street", "5223 alpha road dallas tx 75240", None) : [
            ("addr:street", "Alpha Road"),
            ("addr:housenumber", "5223"),
            ("addr:city", "Dallas"),
            ("addr:state", "TX"),
            ("addr:postcode", "75240")],
        ("addr:street", "5229 alpha road dallas tx 75240", None) : [
            ("addr:street", "Alpha Road"),
            ("addr:housenumber", "5229"),
            ("addr:city", "Dallas"),
            ("addr:state", "TX"),
            ("addr:postcode", "75240")],
        ("addr:street", "5705", None) : [("addr:street", "Ledgestone Drive"),
                                   ("addr:city", "Fort Worth")],
        ("addr:street", "7817 kermit ave fort worth tx", None) : [
            ("addr:street", "Kermit Avenue"),
            ("addr:housenumber", "7817"),
            ("addr:city", "Fort Worth"),
            ("addr:state", "TX")],
        ("addr:street", "1001 Jones Street", None) : [
            ("addr:street", "Jones Street"), ("addr:housenumber", "1001")],
        ("addr:street", "221 W. Lancaster Ave", None) : [
            ("addr:street", "West Lancaster Ave"), ("addr:housenumber", "221")],
        ("addr:street", "500 Crescent Court", None) : [
            ("addr:street", "Crescent Court"), ("addr:housenumber", "500")],
        ("addr:street", "400 W. McDermott Drive", None) : [
            ("addr:street", "West McDermott Drive"), ("addr:housenumber", "400")],
        ("addr:street", "3909 Swiss Ave.", None) : [
            ("addr:street", "Swiss Avenue"), ("addr:housenumber", "3909")],
        ("addr:street", "923 Pennsylvania Avenue", None) : [
            ("addr:street", "Pennsylvania Avenue"), ("addr:housenumber", "923")],
        ("addr:street", "4201", None)                   :  [("addr:street", "Vintage Boulevard")],
        ("addr:housenumber", "Vintage", None)           :  [("addr:housenumber", "4201")],
        ("addr:housenumber", "972-788-2591", None)      :  [("addr:phone", "972-788-2591")],
        ("addr:street", "75062", None)                  :  [("addr:street", "West Northgate Drive")],
        ("addr:street", "Arapaho", None)                :  [("addr:street", "Arapaho Road")],
        ("addr:street", "Arbor Creek", None)            :  [("addr:street", "Arbor Creek Road")],
        ("addr:street", "Arctic", None)                 :  [("addr:street", "Arctic Lane")],
        ("addr:street", "Cantrell Sansom", None)        :  [("addr:street", "Cantrell Sansom Road")],
        ("addr:street", "Cedar Sage", None)             :  [("addr:street", "Cedar Sage Drive")],
        ("addr:street", "Country Club", None)           :  [("addr:street", "Country Club Road")],
        ("addr:street", "E Kearney", None)              :  [("addr:street", "East Kearney Street")],
        ("addr:street", "Everest", None)                :  [("addr:street", "Everest Drive")],
        ("addr:street", "Fawn", None)                   :  [("addr:street", "Fawn Drive")],
        ("addr:street", "Featherston", None)            :  [("addr:street", "Featherston Street")],
        ("addr:street", "Goldmark", None)               :  [("addr:street", "Goldmark Drive")],
        ("addr:street", "Highgrove", None)              :  [("addr:street", "Highgrove Drive")],
        ("addr:street", "Huddleston", None)             :  [("addr:street", "Huddleston Street")],
        ("addr:street", "I 30 Frontage", None)          :  [("addr:street", "I-30 Frontage Road")],
        ("addr:street", "Kroger Gas", None)             :  [("addr:street", "North Beach Street")],
        ("addr:housename", "North Beach Street", None)  :  [("addr:housename", "Kroger Gas")],
        ("addr:street", "McDermott", None)              :  [("addr:street", "McDermott Road")],
        ("addr:street", "Millmar", None)                :  [("addr:street", "Millmar Drive")],
        ("addr:street", "N. Beckley", None)             :  [("addr:street", "North Beckley Avenue")],
        ("addr:street", "North Collins", None)          :  [("addr:street", "North Collins Street")],
        ("addr:street", "Spanish Oaks", None)           :  [("addr:street", "Spanish Oaks Drive")],
        ("addr:street", "Valley View", None)            :  [("addr:street", "Valley View Drive")],
        ("addr:street", "W Park Row", None)             :  [("addr:street", "West Park Row Drive")],
        ("addr:street", "West Henderson", None)         :  [("addr:street", "West Henderson Street")],
        ("addr:street", "West Park Row", None)          :  [("addr:street", "West Park Row Drive")],
        ("addr:street", "Western Center", None)         :  [("addr:street", "Western Center Boulevard")],
        ("addr:street", "Wildfowl", None)               :  [("addr:street", "Wildfowl Drive")],
        ("addr:street", "South Ridgeway", None)         :  [("addr:street", "South Ridgeway Drive")],
        ("addr:street", "Webb Chapel Road 200", None)   :  [("addr:street", "Webb Chapel Road Suite 200")],
        ("addr:street", "County Road 234;CR 234", None) :  [("addr:street", "County Road 234")],
        ("addr:street", "Blvd 26 North", None)          :  [("addr:street", "Grapevine Highway")],
        ("addr:street", "Hwy N 287", None)              :  [("addr:street", "Highway 287 North")],
        ("addr:postcode", "Denton, TX", None)           :  [("addr:postcode", "76210")],
        ("addr:postcode", "74137", None)                :  [("addr:postcode", "75137")],
        ("addr:postcode", "TX", "2387624602")           :  [("addr:postcode", "75226")],
        ("addr:postcode", "TX", "2387624602")           :  [("addr:postcode", "75044")],
        ("addr:postcode", "TX", "230238099")            :  [("addr:postcode", "75226")],
        ("addr:postcode", "TX", "273516914")            :  [("addr:postcode", "75034")],
        ("addr:postcode", "Texas", "270679006")         :  [("addr:postcode", "76109")],
    }

# street types appear in street name and needs to be fixed
TYPE_RE = re.compile(r'''
        \b(?:                               # using a non-matching group
            st   | av     | ave  |
            blvd | dr     | ct   |
            pl   | square | ln   |
            rd   | trl    | pwky |
            cir  | fwy    | hwy  |
            plz
        )                                   # end of non-matching group
        \b\.?                               # end of type, may followed by a dot, for example: Rd.
        ''',
        re.VERBOSE | re.IGNORECASE)

# Based on audit result, dict key is the abbreviated street types exist
# They will be converted to the corresponding value
TYPE_MAPPING = {
                "st"    : "Street",
                "st."   : "Street",
                "av"    : "Avenue",
                "ave"   : "Avenue",
                "ave."  : "Avenue",
                "blvd"  : "Boulevard",
                "blvd." : "Boulevard",
                "dr"    : "Drive",
                "dr."   : "Drive",
                "ct"    : "Court",
                "ct."   : "Court",
                "pl"    : "Place",
                "pl."   : "Place",
                "rd"    : "Road",
                "rd."   : "Road",
                "trl"   : "Trail",
                "pkwy"  : "Parkway",
                "ln"    : "Lane",
                "ln."   : "Lane",
                "cir"   : "Circle",
                "fwy"   : "Freeway",
                "hwy"   : "Highway",
                "plz"   : "Plaza"
            }

# direction, such as N, E, NE, etc. appears in street name are converted to
# full words North, East, Northeast, etc.
# (?<!'|\.|-) used to not match for names like Green's Court, Post-N-Paddock
DIRECTION_RE = {
            "North"     : re.compile(r"(?<!'|\.|-)\b(?:N|North)\b\.?", re.IGNORECASE),
            "South"     : re.compile(r"(?<!'|\.|-)\b(?:S|South)\b\.?", re.IGNORECASE),
            "West"      : re.compile(r"(?<!'|\.|-)\b(?:W|West)\b\.?", re.IGNORECASE),
            "East"      : re.compile(r"(?<!'|\.|-)\b(?:E|East)\b\.?", re.IGNORECASE),
            "Northwest" : re.compile(r"(?<!'|\.|-)\b(?:NW|Northwest)\b\.?", re.IGNORECASE),
            "Northeast" : re.compile(r"(?<!'|\.|-)\b(?:NE|Northeast)\b\.?", re.IGNORECASE),
            "Southwest" : re.compile(r"(?<!'|\.|-)\b(?:SW|Southwest)\b\.?", re.IGNORECASE),
            "Southeast" : re.compile(r"(?<!'|\.|-)\b(?:SE|Southeast)\b\.?", re.IGNORECASE),
        }

# make suite shows consistently in the street name
# #, suite, ste will be converted to Suite
# leading spaces and "," will be replaced by a single space
SUITE_RE = re.compile(r",?\s+\b(?:#|suite|ste)\b", re.IGNORECASE)

#make these street names more consistent
#CR is replaced by "Country Road"
#Farm-to-Market or Farm to Market of F.M. or fm will all be replaced by FM
#State Hwy 121, Highway 121, SH 121 will be replaced by TX 121
#Interstate highway will be replaced by I followed by a number, no space: I30
NUMBERED_ROAD_RE = {
        "County Road": re.compile(r"\bCR\b", re.IGNORECASE),
        "FM": re.compile(r"\b(?:Farm[- ]to[- ]Market(?:\s+Road|\s+Rd\.?)?|F\.M\.|FM)", re.IGNORECASE),
        "TX 121": re.compile(r"(?:State Hwy|Highway|SH) 121", re.IGNORECASE),
        "I": re.compile(r"\b((?:I|Interstate|Interstate Highway)[- ])(\d+)"),
        }

# defines a valid postcode
POSTCODE_RE = re.compile(r"\d{5}(?:-\d{4})?")


def process_special_cases(element):
    """Clean children "tag" of the specified element.
    Assuming tags have only attributes "k" and "v". After cleaning, other
    attributes defined in the original tag will be lost, if there is any.

    :element: xml.etree.ElementTree.Element object for level-one tags

    """
    subelems = []
    for tag in element.iter("tag"):
        key = (tag.attrib["k"], tag.attrib["v"], None)
        # some cases depend on element id
        if key not in special_case_mapping:
            key = (tag.attrib["k"], tag.attrib["v"], element.attrib["id"])
            if key not in special_case_mapping:
                continue

        element.remove(tag)

        for k, v in special_case_mapping[key]:
            subelems.append(ET.Element("tag", {"k" : k, "v" : v}))
            display_tag_change(element, key, (k, v))

    element.extend(subelems)

def process_address(element):
    """Clean address info stored in the children of the specified element.

    :element: xml.etree.ElementTree.Element object for level-one tags

    """
    for tag in element.iter("tag"):
        key, value = tag.attrib["k"], tag.attrib["v"]
        old_value = value
        if key == "addr:street":
            value = update_type(value, TYPE_RE, TYPE_MAPPING)
            value = update_direction(value, DIRECTION_RE)
            value = update_suite(value, SUITE_RE)
            value = update_street_name_with_number(value,
                    NUMBERED_ROAD_RE)
        elif key == "addr:postcode":
            value = update_postcode(value, POSTCODE_RE)

        if value != old_value:
            tag.attrib["v"] = value
            display_tag_change(element, (key, old_value), (key, value))


def display_tag_change(element, old, new):
    """Print tag before and after change to screen.

    :old: (k, v) pair for old element
    :new: (k, v) pair for new element

    """
    msg = '{}-{}:\n<tag k="{}" v="{}"/>\n=>\n<tag k="{}" v="{}"/>\n{}'
    msg = msg.format(element.tag, element.attrib["id"],
            old[0], old[1], new[0], new[1], "="*60)
    print(msg)


def update_type(name, type_re, type_mapping):
    """Covert the abbreviated street type (in type_mapping key) to the
    coresponding type_mapping value

    :name: street name
    :type_re: regex object used to find street type, assuming the last match
              found is the type
    :type_mapping: a dict with key as abbreviated street type,
                   and value as the full word
    :returns: converted street name
    """
    m = type_re.findall(name)
    if m:
        street_type = m[-1]
        street_type_key = street_type.lower()
        if street_type_key in type_mapping:
           name = re.sub(r"\b{}(?=\s|$)".format(street_type),
                    type_mapping[street_type_key], name)

    return name

def update_direction(name, direction_re):
    """Make direction in street name shows consistently:
    N/N. ==> North, S/S. ==> South, etc
    Special case:
        Avenue N
        John W. Elliott
        John W Carpenter
    :name: street name
    :direction_re: a direciton of regex used to convert direction.
                   key is the full word, value is a regex object to find
                   direction in the street name
    :returns: name after conversion

    """
    for key, regex in direction_re.items():
        if ( "Avenue N" not in name and
                "John W. Elliott" not in name and
                "John W Carpenter" not in name):
            name = regex.sub(key, name)
    return name

#make suite consistent in the street name
# #40 ==> Suite 40; Ste 40 ==> Suite 40
# , (comma) in the street name before suite is also matched and will be removed
def update_suite(name, suite_re):
    """Make "suite" consistent in the street name:
    #40 => Suite40; Ste 40 => Suite 40

    :name: street name
    :suite_re: regex object to find "suite" in street name. The match includes
               the space (and "," if existing) before the "suite" pattern
    :returns: street name after conversion

    """
    name = suite_re.sub(" Suite", name)
    return name

#make the street names with numbers to be more consistent
def update_street_name_with_number(name, numbered_road_re):
    """Stree names may contain number: I30, TX 121, etc, this method uses
    regex object in numbered_road_re to make these names consistent:
    Interstate 30 => I30; State Hwy 121 => TX 121

    :name: street name
    :numbered_road_re: a dict with key as the correty way to show the street;
                       its value is used to identiified the street name that
                       needs conversion
    :returns: TODO

    """
    for key, regex in numbered_road_re.items():
        if key == "I":
            m = regex.search(name)
            if m:
                prefix, number = m.groups()
                name = name.replace(prefix, "I")
        else:
            name = regex.sub(key, name)
    return name

def update_postcode(postcode, postcode_re):
    """Replace postcode by the substring that matches postcode_re
    If postcode does not match postcode_re, an message is printed to screen
    and the original postcode is returned

    :postcode: postcode
    :postcode_re: regex object to find real postcode
    :returns: converted postcode or the original postcode if there is no match

    """
    m = postcode_re.search(postcode)
    if m:
        postdoce = m.group()
    else:
        print("Postcode {} is not correct.".format(postcode))
    return postcode

