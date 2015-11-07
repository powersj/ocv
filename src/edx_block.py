#!/usr/bin/python
"""
edX Block object used to parse, store, and setup specific data.
"""


from edx_block_icons import icon_dict
from api.youtube_api import get_video_duration


class Block(object):

    def __init__(self, block):
        self.id = block['id']
        self.type = block['type']
        self.name = block['name']
        self.children = []
        self.parent = ''

        self.tip = ''

        try:
            self.icon = icon_dict[self.type]
        except KeyError:
            self.icon = '\uf111'

        if self.type == 'problem':
            self.generate_problem_tooltip(block)

        if self.type == 'video':
            self.generate_video_tooltip(block)

    def __str__(self):
        """Overload string function."""
        return '{"name": "%s", "parent": "%s", "type": "%s", "icon": "%s", "tip": "%s"},' % (
               self.name.encode('utf-8'), self.parent.encode('utf-8'), self.type.encode('utf-8'),
               self.icon, self.tip)

    def generate_video_tooltip(self, block):
        try:
            youtube_id = block['youtube_id']
        except KeyError:
            youtube_id = ''

        if youtube_id:
            self.tip = 'Video Length: %s' % (get_video_duration(youtube_id))

    def generate_problem_tooltip(self, block):
        try:
            if block['markdown']:
                self.tip = 'I HAVE MARKDOWN TO VIEW!!!'
        except KeyError:
            return 0
