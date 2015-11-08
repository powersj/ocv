#!/usr/bin/python
"""
edX Block object used to parse, store, and setup specific data.
"""
import re


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
        return ('{"id": "%s", "name": "%s", "parent": "%s",'
                ' "type": "%s", "icon": "%s", "tip": "%s"},') % (
               self.id.encode('utf-8'), self.name.encode('utf-8'),
               self.parent.encode('utf-8'), self.type.encode('utf-8'),
               self.icon, self.tip)

    def generate_video_tooltip(self, block):
        try:
            youtube_id = block['youtube_id']
        except KeyError:
            youtube_id = ''

        if youtube_id:
            duration = get_video_duration(youtube_id)
            if duration:
                self.tip = 'Video Length: %s' % (duration)

    @staticmethod
    def generate_feature_list(features):
        string = '<b>Problem Set Features:</b><ul>'
        for feature in features:
            item = '<li>%s</li>' % feature
            string = ''.join([string, item])

        string = ''.join([string, '</ul>'])

        # if we added something great, otherwise return empty string
        if string == '<b>Problem Set Features:</b><ul></ul>':
            return '<b>Problem Set includes no unique features</b>'
        else:
            return string

    def generate_problem_tooltip(self, block):
        try:
            markdown = block['markdown']
        except KeyError:
            markdown = ''

        if markdown:
            regex_dict = {
                'Hint - General':   r"""\|\|.*?\|\|""",
                'Hint - Incorrect': r"""not=.*?""",
                'Explanation':      r"""\[explanation\]""",
                'Feedback':         r"""{{.*?}}"""
            }

            features = []
            for type, regex in sorted(regex_dict.iteritems()):
                if re.compile(regex).findall(markdown):
                    features.append(type)

            self.tip = self.generate_feature_list(features)
