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


def get_children(data, dict, block):
    """Recursive function to produce the nodes and edges for a particular block."""
    str = ''
    for child in block.children:
        str += '\n\t{ "name": "%s", "parent": "%s", "type": "%s"},' % (child.name,
                                                                       block.name,
                                                                       child.type)

        str += get_children(data, dict, child)

    return str


def create_chapter_maps(block):
    """Given a single block, go build all the nodes and edges."""
    data = 'var data = ['
    data += '\n\t{ "name": "%s", "parent": "null", "type": "%s"},' % (block.name, block.type)
    data += get_children(data, dict, block)
    data += '\n\t];'

    return data


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


def get_chapter_data(filename):
    """Gets each chapter data."""
    with open(filename, 'r') as my_file:
        course_dict = json.load(my_file)

    blocks = read_blocks(course_dict)

    chapters = {}
    for block in blocks:
        if block.type == 'chapter':
            chapters[block.name] = create_chapter_maps(block)

    return chapters


def main(filename):
    """Read in a file and print each course by chapter."""
    chapters = get_chapter_data(filename)
    for k, v in chapters.iteritems():
        print k
        print v


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('filename', help='MongoDB data dumped to file')
    ARGS = PARSER.parse_args()

    main(ARGS.filename)
