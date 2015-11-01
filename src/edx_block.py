#!/usr/bin/python
"""
edX Block object used to parse, store, and setup specific data.
"""
import re

from edx_block_icons import icon_dict


class Block(object):

    def __init__(self, block, parent):
        self.id = block['block_id']
        self.name = block['block_name'] if block['block_name'] else block['block_id']
        self.type = block['block_type']
        self.icon = icon_dict[self.type]
        self.tooltip = ''
        self.parent = parent
        self.children = []

    def __str__(self):
        """Overload string function."""
        return '%s, %s' % (self.type, self.name)

    def to_dict(self):
        """Builds a dictionary of the important items for building the visualization."""
        dict = {}
        dict['name'] = self.name
        dict['parent'] = self.parent
        dict['type'] = self.type
        dict['icon'] = self.icon
        dict['tooltip'] = self.tooltip

        return dict

    def get_friendly_name(self, name, type):
        """Checking for UUID strings and replacing with more friendly names."""
        if type == 'openassessment' and self.is_id(name):
            return 'Open Assessment'
        elif type == 'discussion' and self.is_id(name):
            return 'Discussion'
        else:
            return name

    @staticmethod
    def is_id(string):
        """Check string to see if matches UUID syntax of alphanumeric, 32 chars long."""
        regex = re.compile('[0-9a-f]{32}\Z', re.I)
        if bool(regex.match(string)):
            return True

        return False
