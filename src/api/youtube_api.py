#!/usr/bin/python
"""Used to determine YouTube video lengths."""
import os
import requests
import re
import sys


def load_api_key():
    """Read in YouTube API Key from local file."""
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        return open(os.path.join(__location__, 'youtube_api.key'), 'r').read().strip()
    except:
        print >> sys.stderr, ('Error: No YouTube API Key file found.')
        return None


def get_duration_time(video_json):
    """
    Blatenly stole from:
    https://github.com/s16h/py-must-watch/blob/master/add_youtube_durations.py
    """
    hours, minutes, seconds = 0, 0, 0

    duration = video_json['items'][0]['contentDetails']['duration']
    match = re.match(r'PT([0-5]?[\d])M([0-5]?[\d]?)S?', duration)

    if match:
        items = match.groups()
        minutes = items[0]
        seconds = items[1]
    else:
        match_with_hours = re.match(r'PT([\d]?[\d])H([0-5]?[\d]?)M?([0-5]?[\d]?)S?', duration)
        if match_with_hours:
            items = match_with_hours.groups()
            hours = items[0]
            minutes = items[1]
            seconds = items[2]

    return hours, minutes, seconds


def get_human_readable(duration):
    """
    Blatenly stole from:
    https://github.com/s16h/py-must-watch/blob/master/add_youtube_durations.py
    """
    hours = duration[0]
    minutes = duration[1]
    seconds = duration[2]

    output = ''
    if hours == '':
        output += '00'
    else:
        output += '0' + str(hours)

    output += ':'
    if minutes == '':
        output += '00'
    elif int(minutes) < 10:
        output += '0' + str(minutes)
    else:
        output += str(minutes)

    output += ':'
    if seconds == '':
        output += '00'
    elif int(seconds) < 10:
        output += '0' + str(seconds)
    else:
        output += str(seconds)

    return output


def get_video_duration(youtube_id):
    """Given a specific YouTube video id, go print the duration of the video."""
    api_key = load_api_key()
    if not api_key:
        return ''

    url = 'https://www.googleapis.com/youtube/v3/videos?'
    uri = 'part=contentDetails&id=%s&fields=items&key=%s' % (youtube_id, api_key)
    query = ''.join([url, uri])

    try:
        request = requests.get(query)
    except:
        print >> sys.stderr, 'Could not retrive video: %s' % (youtube_id)
        return ''

    http_code = request.status_code
    if http_code != 200:
        print >> sys.stderr, 'Could not retrive video: %s (HTTP Code: %s)' % (youtube_id, http_code)
        return ''

    duration = get_duration_time(request.json())
    return get_human_readable(duration)


if __name__ == '__main__':
    print get_video_duration('e8DFN3m8XGQ')
