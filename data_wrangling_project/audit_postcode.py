"""
File: audit_postcode.py
Author: Yang Yang
Email: yyangbian@gmail.com
Github: yyangbian
Description: 
    Check postcode in the osm file
"""
import xml.etree.cElementTree as ET
import pprint

def has_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_postcode(osmfile):
    """Audit postcode in the specified osmfile.
    Visit tags with k="addr:postcode", collect all types not in list expected.

    :osmfile: osm file
    :returns: a set of different postcode from osm file
    """

    osm_file = open(osmfile, "r", encoding="utf-8")
    postcodes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if has_postcode(tag):
                    postcodes.add(tag.attrib['v'])

        elem.clear()

    return postcodes

def main(osmfile):
    audit_results = audit_postcode(osmfile)
    pprint.pprint(audit_results)

if __name__ == '__main__':
    import sys
    main(sys.argv[1])


