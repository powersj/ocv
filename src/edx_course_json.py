#!/usr/bin/python
"""
Script used to connect to the edX MongoDB produce a file with the course
content nicely printed to it.
"""
import argparse
import json
import os
import re


from pymongo import MongoClient


MONGODB_IP = None
MONGODB_PORT = 27017
MONGODB_DB = 'edxapp'


def connect_mongo():
    """Connect to MongoDB."""
    client = MongoClient('mongodb://%s:%s' % (MONGODB_IP, str(MONGODB_PORT)))
    database = client[MONGODB_DB]
    return database


def get_published_branch_id(database):
    """Return the IDs of the published-branch courses."""
    collection = 'modulestore.active_versions'
    projection = {'versions.published-branch': 1, '_id': 0}
    cursor = database[collection].find({}, projection)

    published_branch_ids = []
    for result in cursor:
        course_id = result['versions']['published-branch']
        published_branch_ids.append(course_id)

    return published_branch_ids


def get_course_content(database, branch_ids):
    """Get course content for each branch id."""
    content = {}

    for branch_id in branch_ids:
        collection = 'modulestore.structures'
        query = {"_id": branch_id}
        cursor = database[collection].find(query)

        for result in cursor:
            content[branch_id] = result

    return content


def is_id(string):
    """Check string to see if matches UUID syntax of alphanumeric, 32 chars long."""
    regex = re.compile('[0-9a-f]{32}\Z', re.I)
    if bool(regex.match(string)):
        return True

    return False


def customize_discussion(block, block_data):
    if not block_data['name']:
        block_data['name'] = 'Discussion'

    try:
        block_data['name'] = block['fields']['discussion_target']
    except KeyError:
        block_data['name'] = block['fields']['discussion_category']


def customize_html(block, block_data):
    if is_id(block_data['name']) or not block_data['name']:
        block_data['name'] = 'HTML Page'


def customize_openassessment(block, block_data):
    if is_id(block_data['name']):
        block_data['name'] = 'Open Assessment'


def customize_problem(block, block_data):
    if not block_data['name']:
        block_data['name'] = 'Problem'

    try:
        block_data['markdown'] = block['fields']['markdown']
    except:
        block_data['markdown'] = None


def customize_video(block, block_data):
    try:
        block_data['youtube_id'] = block['fields']['youtube_id_1_0']
    except KeyError:
        block_data['youtube_id'] = None
    try:
        block_data['start_time'] = block['fields']['start_time']
    except KeyError:
        block_data['start_time'] = None
    try:
        block_data['end_time'] = block['fields']['end_time']
    except KeyError:
        block_data['end_time'] = None


def customize_by_type(block, block_data):
    if block_data['type'] == 'discussion':
        customize_discussion(block, block_data)
    if block_data['type'] == 'html':
        customize_html(block, block_data)
    elif block_data['type'] == 'openassessment':
        customize_openassessment(block, block_data)
    elif block_data['type'] == 'problem':
        customize_problem(block, block_data)
    elif block_data['type'] == 'video':
        customize_video(block, block_data)


def add_children(block, block_data):
    block_children = []
    for child in block['fields']['children']:
        children_data = {}
        children_data['child_id'] = child[1]
        children_data['child_type'] = child[0]
        block_children.append(children_data)

    block_data['children'] = block_children


def build_course_map(course_id, course_content):
    """Parse out the data for each block."""
    course_dict = {}
    course_dict['course_id'] = course_id.__str__()
    course_blocks = []
    for block in course_content['blocks']:
        block_data = {}

        block_data['id'] = block['block_id']
        block_data['type'] = block['block_type']
        try:
            block_data['name'] = block['fields']['display_name']
        except KeyError:
            block_data['name'] = block_data['id']

        customize_by_type(block, block_data)
        add_children(block, block_data)

        course_blocks.append(block_data)

    course_dict['blocks'] = course_blocks

    return course_dict


def main(ip):
    """Print each published couse content to a file."""
    global MONGODB_IP
    MONGODB_IP = ip

    database = connect_mongo()
    branch_ids = get_published_branch_id(database)
    course_dump = get_course_content(database, branch_ids)

    for course_id, course_content in course_dump.iteritems():
        course_dict = build_course_map(course_id, course_content)
        filename = '%s.json' % str(course_id)
        filepath = os.path.join('./data/', filename)

        with open(filepath, 'w') as outfile:
            json.dump(course_dict, outfile, indent=4)

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('ip', help='IP Address for valid MongoDB')
    ARGS = PARSER.parse_args()

    main(ARGS.ip)
