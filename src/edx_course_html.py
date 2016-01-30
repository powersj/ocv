#!/usr/bin/python
"""
Print out self-contained HTML page with visualization. However, does require internet access to
download the d3.js script.
"""
import argparse
import os
import re

from edx_course_map import build_course_tree


def print_html_header():
    """Print the header and start of the body of the HTML document."""
    return """<!DOCTYPE html>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>OCV</title>
<meta name="description" content="Online Course Visualizer">

<script type="text/javascript" src="js/jquery.js"></script>
<script type="text/javascript" src="js/d3.js"></script>
<script type="text/javascript" src="js/d3-tip.js"></script>

<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Cantarell" />
<link rel="stylesheet" type="text/css" href="css/font-awesome.css">
<link rel="stylesheet" type="text/css" href="css/style.css">

<body>
<script type="text/javascript">
var data = ["""


def print_html_footer():
    """Finish off the HTML tags."""
    return """];
</script>
<script type="text/javascript" src="js/tree.js"></script>
</body>
</html>"""


def create_div_id(key):
    """
    One method to take course name and do the following:
    1) make lower case
    2) remove white space
    3) remove non-alphanumeric charachters
    """
    return re.sub(r'\W+', '', key.lower().replace(' ', ''))


def main(filename, id_only):
    """Print working single, self contained HTML page with only external dependency on d3.js."""
    course_data = build_course_tree(filename, id_only)

    output_filename = os.path.splitext(os.path.basename(filename))[0] + '.html'
    output_file = open('../output/' + output_filename, 'w')
    print 'creating ../output/%s' % output_filename

    output_file.write(print_html_header())
    for data in course_data:
        output_file.write('\t%s' % (data))
    output_file.write(print_html_footer())

    output_file.close()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('filename', help='MongoDB data dumped to file')
    PARSER.add_argument('-i', '--id-only', action="store_true", help='Uses the id as the tooltip',
                        default=False)
    ARGS = PARSER.parse_args()

    main(ARGS.filename, ARGS.id_only)
