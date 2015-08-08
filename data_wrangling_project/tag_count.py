#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: tag_count.py
Author: Yang Yang
Email: yyangbian@gmail.com
Github: yyangbian
Description: Count different types of tags in the xml file
"""
import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):
    result = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag not in result:
            result[elem.tag] = 1
        else:
            result[elem.tag] += 1
        elem.clear()
    return result



if __name__ == "__main__":
    import sys
    tags = count_tags(sys.argv[1])
    pprint.pprint(tags)
