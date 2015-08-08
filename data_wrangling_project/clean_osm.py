#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: clean_osm.py
Author: Yang Yang
Email: yyangbian@gmail.com
Github: yyangbian
Description:
Clean original osm data and generate a new osm file:
- 2 types of top level tags: "node" and "way", are processed
- Fix some "special issues in address related field.
    * Street names without correct type
    * Street name v field is not a name, but rather phone or house number
    * Street name v field contains the house number or other information
    * If street names contain other information, for example,
        house number, a separate tag is created for this information.
    * Postcode field does not contain any postcode or out of dallas region.
- Fix general issues in street name and postcode:
    * Street name is over-abbreviated in street type, direction. Cleaning
      makes the name show in a consistent way
        - "Rd." => "Road".
        - "Ste" or "#" is converted to "Suite"
        - "N" => "North", "NW" => "Northwest" ...
    * Multilple street names with number in them are converted
    to make the name consistent:
        - Interstate highway names: "Interstate Hwy 30" => "I30" ...
        - County Road names are converted: "CR 120" => "County Road 120"
        - Farm-to-market road names are converted: "F.M. 150" => "FM 150"
        - State Highway 121 are all renamed to "TX 121"

    * Postcode field contains special character or information other than
      postcode. Special characters and additinal information are removed
        <tag k="addr:postcode" v="Grand Prairie, TX 75052-8514"/> =>
        <tag k="addr:postcode" v="75226"/>
"""
import xml.etree.cElementTree as ET

LEVEL_ONE_TAGS = ["node", "way", "relation", "bounds"]

import clean_utils

def process_element(element):
    """Make changes to this element.

    :element: a level-one element to be processed

    """
    if element.tag not in clean_utils.TAGS_TO_PROCESS:
        return

    clean_utils.process_special_cases(element)

    clean_utils.process_address(element)


def clean_osm(osm_file, new_osm_file):
    """Parse osm_file and create a new_osm_file with data cleaned.

    :osm_file: original osm data file
    :new_osm_file: new osm data file

    """
    with open(new_osm_file, 'wb') as output:
        output.write(bytes('<?xml version="1.0" encoding="UTF-8"?>\n', 'utf-8'))
        output.write(bytes('<osm>\n', 'utf-8'))

        context = ET.iterparse(osm_file, events=('start', 'end'))

        _, root = next(context)

        # process level-one tags one by one, clean it up after done
        for event, element in context:
            if event == 'end' and element.tag in LEVEL_ONE_TAGS:
                process_element(element)

                output.write(ET.tostring(element, encoding='utf-8'))
                root.clear()

        output.write(bytes('</osm>', 'utf-8'))

if __name__ == '__main__':
    import sys
    clean_osm(sys.argv[1], sys.argv[2])
