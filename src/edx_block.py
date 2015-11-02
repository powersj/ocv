#!/usr/bin/python
"""
edX Block object used to parse, store, and setup specific data.
"""


from edx_block_icons import icon_dict


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
            self.markdown = block['markdown']
        if self.type == 'video':
            self.video_start = block['start_time']
            self.video_end = block['end_time']
            self.youtube_id = block['youtube_id']

    def __str__(self):
        """Overload string function."""
        return '{"name": "%s", "parent": "%s", "type": "%s", "icon": "%s", "tip": "%s"},' % (
               self.name.encode('utf-8'), self.parent.encode('utf-8'), self.type.encode('utf-8'),
               self.icon.encode('utf-8'), self.tip.encode('utf-8'))
