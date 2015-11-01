#!/usr/bin/python
"""
Script used to connect to the edX MongoDB or take in valid MongoDB database
dump and produce valid couse represented in JSON format.
"""
import argparse
import json


from edx_block import Block


def read_blocks(course_dict):
    """Read entire course dictionary into Block objects and set children."""
    blocks = {}
    for item in course_dict['blocks']:
        blocks[item['block_id']] = Block(item)

    # now go through and add refrences to each parent to the children blocks
    for item in course_dict['blocks']:
        parent_id = item['block_id']
        for child in item['children']:
            blocks[parent_id].children.append(blocks[child['child_id']])

    return blocks.values()


def get_children(block):
    """Finds all children and children's children recursively."""
    tree = []
    for child in block.children:
        tree.append(child)
        tree.append(get_children(child))

    return tree


def build_course_tree(filename):
    """Get all course data from a specific file. Assumes only one course per file."""
    with open(filename, 'r') as my_file:
        course_dict = json.load(my_file)

    blocks = read_blocks(course_dict)

    tree = []
    for block in blocks:
        if block.type == 'course':
            tree.append(block)
            tree.append(get_children(block))

    return tree


def main(filename):
    """Read in a file and print each course by chapter."""
    course = build_course_tree(filename)
    print course


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('filename', help='MongoDB data dumped to file')
    ARGS = PARSER.parse_args()

    main(ARGS.filename)
