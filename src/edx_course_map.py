#!/usr/bin/python
"""
Script used to connect to the edX MongoDB or take in valid MongoDB database
dump and produce valid couse represented in JSON format.
"""
import argparse
import json

from pdb import set_trace


def main(filename):
    """Read in a file and print JSON of the course content."""
    with open(filename, 'r') as my_file:
        course_dict = json.load(my_file)

    print course_dict['course_id']
    print len(course_dict['blocks'])

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-f', '--filename', help='MongoDB data dumped to file')
    ARGS = PARSER.parse_args()

    main(ARGS.filename)
