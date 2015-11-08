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
        blocks[item['id']] = Block(item)

    # now go through and add refrences to each parent to the children blocks
    for item in course_dict['blocks']:
        parent_id = item['id']
        for child in item['children']:
            blocks[parent_id].children.append(blocks[child['child_id']])

    return blocks.values()


def get_children(tree, block):
    """Finds all children and children's children recursively."""
    for child in block.children:
        child.parent = block.id
        tree.append(child)
        children = get_children(tree, child)
        if children:
            tree.append(children)


def build_course_tree(filename):
    """Get all course data from a specific file. Assumes only one course per file."""
    with open(filename, 'r') as my_file:
        course_dict = json.load(my_file)

    blocks = read_blocks(course_dict)

    tree = []
    for block in blocks:
        if block.type == 'course':
            block.parent = 'null'
            tree.append(block)
            children = get_children(tree, block)
            if children:
                tree.append(children)

    return tree


def main(filename):
    """Read in a file and print each course by chapter."""
    course = build_course_tree(filename)
    for block in course:
        print block


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('filename', help='MongoDB data dumped to file')
    ARGS = PARSER.parse_args()

    main(ARGS.filename)
