#!/usr/bin/python
"""
Script used to connect to the edX MongoDB produce a file with the course
content nicely printed to it.
"""
import argparse
import json
import os

from pymongo import MongoClient

MONGODB_IP = None
MONGODB_PORT = 27017
MONGODB_DB = 'edxapp'


def connect_mongo():
    """Connect to MongoDB."""
    client = MongoClient('mongodb://' + MONGODB_IP + ':' + str(MONGODB_PORT))
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


def build_course_map(course_id, course_content):
    """Parse out the data for each block."""
    course_dict = {}
    course_dict['course_id'] = course_id.__str__()
    course_blocks = []
    for block in course_content['blocks']:
        block_data = {}
        block_data['block_id'] = block['block_id'].encode('utf-8')
        block_data['block_type'] = block['block_type'].encode('utf-8')
        try:
            block_data['block_name'] = block['fields']['display_name'].encode('utf-8')
        except KeyError:
            block_data['block_name'] = None

        block_children = []
        for child in block['fields']['children']:
            children_data = {}
            children_data['child_id'] = child[1].encode('utf-8')
            children_data['child_type'] = child[0].encode('utf-8')
            block_children.append(children_data)

        block_data['children'] = block_children
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
        filename = course_id.__str__() + '.json'
        filepath = os.path.join('./data/', filename)

        with open(filepath, 'w') as outfile:
            json.dump(course_dict, outfile, indent=4)

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('ip', help='IP Address for valid MongoDB')
    ARGS = PARSER.parse_args()

    main(ARGS.ip)
