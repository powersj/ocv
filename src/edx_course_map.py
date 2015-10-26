#!/usr/bin/python
"""
Script used to connect to the edX MongoDB or take in valid MongoDB database
dump and produce valid couse represented in JSON format.
"""
import argparse
import json


class Block(object):
    def __init__(self, id, name, type, children):
        self.id = id
        self.name = name if name else id
        self.type = type
        self.children = children

    def __str__(self):
        return '%s (%s)' % (self.name, self.type)


def read_blocks(course_dict):
    """Read in the course dictionary into Block objects."""
    blocks = {}
    for item in course_dict['blocks']:
        blocks[item['block_id']] = Block(item['block_id'], item['block_name'],
                                         item['block_type'], item['children'])

    for id, block in blocks.iteritems():
        list = []
        for child in block.children:
            list.append(blocks[child['child_id']])
        block.children = list

    return blocks


def main(filename):
    """Read in a file and print JSON of the course content."""
    with open(filename, 'r') as my_file:
        course_dict = json.load(my_file)

    blocks = read_blocks(course_dict)

    print '//',
    print '-' * 58
    print '// Course: %s (%s blocks)' % (course_dict['course_id'],
                                         len(course_dict['blocks']))
    print '//',
    print '-' * 58

    print '\n// printing nodes'
    for id, block in blocks.iteritems():
        print 'g.setNode("%s", { label: "%s" });' % (block.id, block.name)

    print '\n// printing edges'
    for id, block in blocks.iteritems():
        for child in block.children:
            print 'g.setEdge("%s", "%s");' % (block.id, child.id)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-f', '--filename', help='MongoDB data dumped to file')
    ARGS = PARSER.parse_args()

    main(ARGS.filename)
