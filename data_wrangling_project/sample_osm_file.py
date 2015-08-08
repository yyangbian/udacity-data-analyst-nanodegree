#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def main(osm_file, sample_file):
    with open(sample_file, 'wb') as output:
        output.write(bytes('<?xml version="1.0" encoding="UTF-8"?>\n', 'utf-8'))
        output.write(bytes('<osm>\n', 'utf-8'))

        # Write every 80th top level element
        for i, element in enumerate(get_element(osm_file)):
            if i % 80 == 0:
                output.write(ET.tostring(element, encoding='utf-8'))

        output.write(bytes('</osm>', 'utf-8'))

if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])
