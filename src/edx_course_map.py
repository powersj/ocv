#!/usr/bin/python
"""
Script used to connect to the edX MongoDB or take in valid MongoDB database
dump and produce valid couse represented in JSON format.
"""
import argparse
import json


class Block(object):
    def __init__(self, id, name, type):
        self.id = id
        self.name = name if name else id
        self.type = type
        self.children = []

    def __str__(self):
        return '%s, %s' % (self.type, self.name)


def get_children(dict, block):
    """Recursive function to produce the nodes and edges for a particular block."""
    for child in block.children:
        print '    { "name": "%s", "parent": "%s", "type": "%s"},' % (child.name,
                                                                      block.name,
                                                                      child.type)
        get_children(dict, child)


def create_chapter_maps(block):
    """Given a single block, go build all the nodes and edges."""
    print '    { "name": "%s", "parent": "null", "type": "%s"},' % (block.name, block.type)
    get_children(dict, block)


def read_blocks(course_dict):
    """Read entire course dictionary into Block objects and set children."""
    blocks = {}
    for item in course_dict['blocks']:
        blocks[item['block_id']] = Block(item['block_id'], item['block_name'], item['block_type'])

    # now go through and add refrences to each parent to the children blocks
    for item in course_dict['blocks']:
        parent_id = item['block_id']
        for child in item['children']:
            blocks[parent_id].children.append(blocks[child['child_id']])

    return blocks.values()


def main(filename):
    """Read in a file and print each course by chapter."""
    with open(filename, 'r') as my_file:
        course_dict = json.load(my_file)

    blocks = read_blocks(course_dict)
    for block in blocks:
        if block.type == 'chapter':
            print 'var data = ['
            create_chapter_maps(block)
            print '];'
            print

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-f', '--filename', help='MongoDB data dumped to file')
    ARGS = PARSER.parse_args()

    main(ARGS.filename)
