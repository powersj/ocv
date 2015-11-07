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
            try:
                self.markdown = block['markdown']
            except KeyError:
                self.markdown = ''
        if self.type == 'video':
            try:
                self.youtube_id = block['youtube_id']
            except KeyError:
                self.youtube_id = ''
                
            try:
                self.video_start = block['start_time']
            except KeyError:
                self.video_start = ''

            try:
                self.video_end = block['end_time']
            except KeyError:
                self.video_end = ''

        self.generate_tooltip()

    def __str__(self):
        """Overload string function."""
        return '{"name": "%s", "parent": "%s", "type": "%s", "icon": "%s", "tip": "%s"},' % (
               self.name.encode('utf-8'), self.parent.encode('utf-8'), self.type.encode('utf-8'),
               self.icon, self.tip)

    def generate_tooltip(self):
        if self.type == 'video':
            self.tip = 'video tip: %s %s %s' % (self.youtube_id.encode('utf-8'),
                                                self.video_start,
                                                self.video_end)
        elif self.type == 'problem' and self.markdown:
            self.tip = 'I HAVE MARKDOWN TO VIEW!!!'
