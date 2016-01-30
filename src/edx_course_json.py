#!/usr/bin/python
"""
Script used to connect to the edX MongoDB produce a file with the course
content nicely printed to it.
"""
import argparse
import json
import os
import re


def is_id(string):
    """Check string to see if matches UUID syntax of alphanumeric, 32 chars long."""
    regex = re.compile('[0-9a-f]{32}\Z', re.I)
    if bool(regex.match(string)):
        return True

    return False


def parse_id(string):
    """Returns the UUID part of a string only."""
    return string.split('/')[-1]


def customize_discussion(course_data, block_data):
    """Sets the block name for Discussions if emtpy."""
    try:
        block_data['name'] = course_data['metadata']['discussion_target']
    except KeyError:
        try:
            block_data['name'] = course_data['metadata']['discussion_category']
        except KeyError:
            if not block_data['name']:
                block_data['name'] = 'Discussion'


def customize_html(course_data, block_data):
    """Sets the block name for HTML pages if emtpy."""
    if is_id(block_data['name']) or not block_data['name']:
        block_data['name'] = 'HTML Page'


def customize_openassessment(course_data, block_data):
    """Sets the block name for Open Assessments if emtpy."""
    if is_id(block_data['name']):
        block_data['name'] = 'Open Assessment'


def customize_problem(course_data, block_data):
    """Sets the block name for Problems if empty."""
    if not block_data['name']:
        block_data['name'] = 'Problem'

    try:
        block_data['markdown'] = course_data['metadata']['markdown']
    except:
        block_data['markdown'] = None


def customize_video(course_data, block_data):
    """Sets block data for Videos."""
    try:
        block_data['youtube_id'] = course_data['metadata']['youtube_id_1_0']
    except KeyError:
        block_data['youtube_id'] = None
    try:
        block_data['start_time'] = course_data['metadata']['start_time']
    except KeyError:
        block_data['start_time'] = None
    try:
        block_data['end_time'] = course_data['metadata']['end_time']
    except KeyError:
        block_data['end_time'] = None


def customize_by_type(course_data, block_data):
    """Master customizer function."""
    if block_data['type'] == 'discussion':
        customize_discussion(course_data, block_data)
    if block_data['type'] == 'html':
        customize_html(course_data, block_data)
    elif block_data['type'] == 'openassessment':
        customize_openassessment(course_data, block_data)
    elif block_data['type'] == 'problem':
        customize_problem(course_data, block_data)
    elif block_data['type'] == 'video':
        customize_video(course_data, block_data)


def add_children(course_data, block_data):
    """Adds the children to each block."""
    block_children = []
    for child in course_data['children']:
        children_data = {}
        children_data['child_id'] = parse_id(child)
        children_data['child_type'] = None
        block_children.append(children_data)

    block_data['children'] = block_children


def build_course_map(course_content):
    """Parse out the data for each block."""
    course_blocks = []

    for key, course_data in course_content.items():
        block_data = {}
        block_data['id'] = parse_id(key)
        block_data['type'] = course_data['category']

        try:
            block_data['name'] = course_data['metadata']['display_name']
        except KeyError:
            block_data['name'] = block_data['id']

        customize_by_type(course_data, block_data)
        add_children(course_data, block_data)

        course_blocks.append(block_data)

    return course_blocks


def main(filename):
    """Print each published couse content to a file."""
    with open(filename) as json_file:
        data = json.load(json_file)

    course_dict = {}
    course_dict['course_id'] = str(os.path.split(filename.strip('/'))[-1])
    course_dict['blocks'] = build_course_map(data)

    filename = '%s' % course_dict['course_id']
    filepath = os.path.join('../input/', filename)

    with open(filepath, 'w') as outfile:
        json.dump(course_dict, outfile, indent=4)

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('filename', help='JSON file to parse.')
    ARGS = PARSER.parse_args()

    main(ARGS.filename)
