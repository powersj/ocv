#!/usr/bin/python
"""
Script used to connect to the edX MongoDB or take in valid MongoDB database
dump and produce valid couse represented in JSON format.
"""
import argparse
import json
import re


class Block(object):

    def __init__(self, id, name, type):
        self.id = id
        self.name = name if name else id
        self.type = type
        self.children = []

    def __str__(self):
        return '%s, %s' % (self.type, self.name)


def get_awesome_icon(type):
    """Return unicode value of the icon for the particular type."""
    if type == 'chapter':
        return '\uf0c8'
    if type == 'course':
        return '\uf19c'
    elif type == 'discussion':
        return '\uf0c0'
    elif type == 'html':
        return '\uf02e'
    elif type == 'openassessment':
        return '\uf044'
    elif type == 'problem':
        return '\uf046'
    elif type == 'sequential':
        return '\uf02d'
    elif type == 'vertical':
        return '\uf0c9'
    elif type == 'video':
        return '\uf008'


def is_id(name):
    """Check names to see if they match UUID syntax of alphanumeric, 32 chars long."""
    regex = re.compile('[0-9a-f]{32}\Z', re.I)
    if bool(regex.match(name)):
        return True

    return False


def get_friendly_name(name, type):
    """Checking for UUID strings and replacing with more friendly names."""
    if type == 'openassessment' and is_id(name):
        return 'Open Assessment'
    elif type == 'discussion' and is_id(name):
        return 'Discussion'
    else:
        return name


def get_children(data, dict, block):
    """Recursive function to produce the nodes and edges for a particular block."""
    str = ''

    for child in block.children:
        icon = get_awesome_icon(child.type)
        name = get_friendly_name(child.name, child.type)
        # name = child.name
        str += '\n\t{ "name": "%s", "parent": "%s", "type": "%s", "icon": "%s"},' % (
            name, block.name, child.type, icon)

        str += get_children(data, dict, child)

    return str


def create_course_map(block):
    """Given a single block, go build all the nodes and edges."""
    icon = get_awesome_icon(block.type)
    data = '\n\t{ "name": "%s", "parent": "null", "type": "%s", "icon": "%s"},' % (
        block.name, block.type, icon)
    children = get_children(data, dict, block)

    return '%s%s%s%s' % ('var data = [', data, children, '\n\t];')


def read_blocks(course_dict):
    """Read entire course dictionary into Block objects and set children."""
    blocks = {}
    for item in course_dict['blocks']:
        blocks[item['block_id']] = Block(
            item['block_id'], item['block_name'], item['block_type'])

    # now go through and add refrences to each parent to the children blocks
    for item in course_dict['blocks']:
        parent_id = item['block_id']
        for child in item['children']:
            blocks[parent_id].children.append(blocks[child['child_id']])

    return blocks.values()


def get_course_data(filename):
    """Gets each chapter data."""
    with open(filename, 'r') as my_file:
        course_dict = json.load(my_file)

    blocks = read_blocks(course_dict)

    course = []
    for block in blocks:
        if block.type == 'course':
            course.append(create_course_map(block))

    return course


def main(filename):
    """Read in a file and print each course by chapter."""
    course_data = get_course_data(filename)
    for item in course_data:
        print item


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('filename', help='MongoDB data dumped to file')
    ARGS = PARSER.parse_args()

    main(ARGS.filename)
