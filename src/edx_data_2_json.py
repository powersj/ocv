#!/usr/bin/python
"""
Script used to connect to the edX MongoDB or take in valid MongoDB database
dump and produce valid couse represented in JSON format.
"""
import argparse

from pymongo import MongoClient

MONGODB_IP = None
MONGODB_PORT = 27017
MONGODB_DB = 'edxapp'


def query_db(collection, query, projection=None):
    """Given a query connect to the datbase and run it."""
    client = MongoClient('mongodb://' + MONGODB_IP + ':' + str(MONGODB_PORT))
    database = client[MONGODB_DB]
    if projection:
        return database[collection].find(query, projection)
    else:
        return database[collection].find(query)


def get_published_branch_id():
    """Return the IDs of the published-branch courses."""
    results = query_db('modulestore.active_versions',
                       {},
                       {'versions.published-branch': 1, '_id': 0})

    published_branch_ids = []
    for result in results:
        course_id = result['versions']['published-branch']
        published_branch_ids.append(course_id)

    return published_branch_ids


def get_course_content(branch_ids):
    """Get course content for each branch id."""
    content = {}

    for branch_id in branch_ids:
        results = query_db('modulestore.structures', {"_id": branch_id})

        for result in results:
            content[branch_id] = result

    return content


def build_course_map(course_id, course_content):
    """Parse out the data for each block."""
    print course_id
    for block in course_content['blocks']:
        content_id = block['block_id'].encode('utf-8')
        content_type = block['block_type'].encode('utf-8')
        children = block['fields']['children']

        try:
            name = block['fields']['display_name'].encode('utf-8')
        except KeyError:
            name = ''

        print '%s, %s, %s' % (content_id, content_type, name)
        for child in children:
            child_id = child[0].encode('utf-8')
            child_type = child[1].encode('utf-8')
            print child_id, child_type
        print


def main():
    """Main function to do stuff."""
    branch_ids = get_published_branch_id()
    content = get_course_content(branch_ids)
    print 'breaking down course:'
    print
    for course_id, course_content in content.iteritems():
        # if course_id.__str__() == '561c649756c02c484b1bb5ec':
        build_course_map(course_id, course_content)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('ip', help='IP Address for valid MongoDB')
    PARSER.add_argument('file', help='MongoDB data dumped to file')
    PARSER.add_argument('dir', help='Directory of MongoDB data')
    ARGS = PARSER.parse_args()

    MONGODB_IP = ARGS.ip

    main()
