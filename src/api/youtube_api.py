#!/usr/bin/python
"""Used to determine YouTube video lengths."""
import requests
import re


def load_api_key():
    """Read in YouTube API Key from local file."""
    try:
        return open('youtube_api.key', 'r').read().strip()
    except:
        SystemExit('Error: No YouTube API Key file found.')


def get_duration(json_video):
    """
    Blatenly stole from:
    https://github.com/s16h/py-must-watch/blob/master/add_youtube_durations.py
    """
    hours, minutes, seconds = 0, 0, 0
    duration = json_video['items'][0]['contentDetails']['duration']
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


def get_human_duration(duration):
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
        output += '0' + minutes
    else:
        output += minutes

    output += ':'
    if seconds == '':
        output += '00'
    elif int(seconds) < 10:
        output += '0' + seconds
    else:
        output += seconds

    return output


def main(youtube_id):
    """Given a specific YouTube video id, go print the duration of the video."""
    api_key = load_api_key()

    url = 'https://www.googleapis.com/youtube/v3/videos?'
    uri = 'part=contentDetails&id=%s&fields=items&key=%s' % (youtube_id, api_key)
    query = ''.join([url, uri])

    try:
        request = requests.get(query)
    except:
        print 'ERROR: Cannot get YouTube API data for: %s' % youtube_id

    duration = get_duration(request.json())
    return get_human_duration(duration)


if __name__ == '__main__':
    print main('e8DFN3m8XGQ')
