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
            self.generate_problem_tooltip(block)

        if self.type == 'video':
            self.generate_video_tooltip(block)

    def __str__(self):
        """Overload string function."""
        return '{"name": "%s", "parent": "%s", "type": "%s", "icon": "%s", "tip": "%s"},' % (
               self.name.encode('utf-8'), self.parent.encode('utf-8'), self.type.encode('utf-8'),
               self.icon, self.tip)

    def generate_problem_tooltip(self, block):
        try:
            if block['markdown']:
                self.tip = 'I HAVE MARKDOWN TO VIEW!!!'
        except KeyError:
            return 0

    def generate_video_tooltip(self, block):
        try:
            youtube_id = block['youtube_id']
        except KeyError:
            youtube_id = ''

        try:
            video_start = block['start_time']
        except KeyError:
            video_start = None

        try:
            video_end = block['end_time']
        except KeyError:
            video_end = None

        # if video_start and video_end:
        #     video_length = video_end - video_start
        # else:
        #     video_length = '' # query_youtube_api(youtube_id)

        self.tip = 'video tip: %s %s %s' % (youtube_id.encode('utf-8'), video_start, video_end)
