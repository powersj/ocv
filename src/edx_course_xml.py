#!/usr/bin/python
"""
Script used to connect read in an edX course exported to XML files
and to produce a json formatted data file.
"""
import argparse
import glob
import json
import os
import re

from lxml import etree


def is_id(string):
    """Check string to see if matches UUID syntax of alphanumeric, 32 chars long."""
    regex = re.compile('[0-9a-f]{32}\Z', re.I)
    if bool(regex.match(string)):
        return True

    return False


def customize_discussion(root, block_data):
    try:
        block_data['name'] = root.attrib['discussion_target']
    except KeyError:
        try:
            block_data['name'] = root.attrib['discussion_category']
        except KeyError:
            if not block_data['name']:
                block_data['name'] = 'Discussion'


def customize_html(root, block_data):
    if is_id(block_data['name']) or not block_data['name']:
        block_data['name'] = 'HTML Page'


def customize_openassessment(block, block_data):
    if is_id(block_data['name']):
        block_data['name'] = 'Open Assessment'


def customize_problem(root, block_data):
    if not block_data['name']:
        block_data['name'] = 'Problem'

    try:
        block_data['markdown'] = root.attrib['markdown']
    except:
        block_data['markdown'] = None


def customize_video(root, block_data):
    try:
        block_data['youtube_id'] = root.attrib['youtube_id_1_0']
    except KeyError:
        block_data['youtube_id'] = None
    try:
        block_data['start_time'] = root.attrib['start_time']
    except KeyError:
        block_data['start_time'] = None
    try:
        block_data['end_time'] = root.attrib['end_time']
    except KeyError:
        block_data['end_time'] = None


def customize_by_type(root, block_data):
    """TODO"""
    if block_data['type'] == 'discussion':
        customize_discussion(root, block_data)
    if block_data['type'] == 'html':
        customize_html(root, block_data)
    elif block_data['type'] == 'openassessment':
        customize_openassessment(root, block_data)
    elif block_data['type'] == 'problem':
        customize_problem(root, block_data)
    elif block_data['type'] == 'video':
        customize_video(root, block_data)


def add_children(root, block_data):
    """TODO"""
    block_children = []
    for child in root.getchildren():
        child_data = {}
        child_data['child_type'] = child.tag
        try:
            child_data['child_id'] = child.attrib['url_name']
        except KeyError:
            continue
        block_children.append(child_data)

    block_data['children'] = block_children


def build_course_map(xml_file):
    """TODO"""
    tree = etree.parse(xml_file)
    root = tree.getroot()

    block_data = {}
    block_data['type'] = root.tag
    block_data['id'] = os.path.splitext(os.path.basename(xml_file))[0]

    try:
        block_data['name'] = root.attrib['display_name']
    except KeyError:
        block_data['name'] = block_data['id']

    customize_by_type(root, block_data)
    add_children(root, block_data)

    return block_data


def main(folder):
    """Print each published couse content to a file."""

    xml_files = [y for x in os.walk(folder) for y in glob.glob(os.path.join(x[0], '*.xml'))]

    course_dict = {}
    course_dict['course_id'] = str(os.path.split(folder.strip('/'))[-1])
    course_blocks = []

    for xml_file in xml_files:
        if '/course/' not in xml_file and not is_id(os.path.splitext(os.path.basename(xml_file))[0]):
            print 'skipping: %s' % xml_file
            continue
        course_blocks.append(build_course_map(xml_file))

    course_dict['blocks'] = course_blocks

    filename = '%s.json' % course_dict['course_id']
    filepath = os.path.join('./data/', filename)

    with open(filepath, 'w') as outfile:
        json.dump(course_dict, outfile, indent=4)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('folder', help='Folder with XML export.')
    ARGS = PARSER.parse_args()

    main(ARGS.folder)
