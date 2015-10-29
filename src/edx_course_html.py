#!/usr/bin/python
"""
Print out self-contained HTML page with visualization. However, does require internet access to
download the d3.js script.
"""
import argparse
import re

from edx_course_map import get_chapter_data


def print_html_header():
    """Print the header and start of the body of the HTML document."""
    print """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>OCV</title>
    <meta name="description" content="Online Course Visualizer">

    <style>
        html {
            display: table;
            margin: auto;
        }

        body {
            display: table-cell;
            font-family: 'Cantarell';
            font-size: 100%;
            vertical-align: middle;
        }
        .link {
            fill: none;
            stroke: #ccc;
            stroke-width: 2px;
        }
    </style>

    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js">
    </script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
    <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Cantarell" />
</head>

<body>
<h1>Online Course Visualizations</h1>
<p>Below is a visualization for each chapter (printed alphabetically) found in the edX demo course.
This course was picked due to the size, scope,and variety of components it offers.</p>
"""


def print_html_footer():
    """Finish off the HTML tags."""
    print """
</body>
</html>"""


def print_javascript_function(div_id):
    """Print all the icky javascript."""
    print """var dataMap = data.reduce(function(map, node) {
            map[node.name] = node;
            return map;
        }, {});

        var treeData = [];
        data.forEach(function(node) {
            // add to parent
            var parent = dataMap[node.parent];
            if (parent) {
                // create child array if it doesn't exist
                (parent.children || (parent.children = []))
                // add node to child array
                .push(node);
            } else {
                // parent is null or missing
                treeData.push(node);
            }
        });
        // ************** Generate the tree diagram	 *****************
        var margin = {
                top: 20,
                right: 120,
                bottom: 20,
                left: 120
            },
            width = 960 - margin.right - margin.left,
            height = 500 - margin.top - margin.bottom;

        var i = 0;

        var tree = d3.layout.tree()
            .size([height, width]);

        var diagonal = d3.svg.diagonal()
            .projection(function(d) {
                return [d.y, d.x];
            });
"""

    print '        var svg = d3.select("#%s").append("svg")' % div_id

    print """.attr("width", width + margin.right + margin.left)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            root = treeData[0];

            update(root);

            function update(source) {

                // Compute the new tree layout.
                var nodes = tree.nodes(root).reverse(),
                    links = tree.links(nodes);

                // Normalize for fixed-depth.
                nodes.forEach(function(d) {
                    d.y = d.depth * 180;
                });

                // Declare the nodes!
                var node = svg.selectAll("g.node")
                    .data(nodes, function(d) {
                        return d.id || (d.id = ++i);
                    });

                // Enter the nodes.
                var nodeEnter = node.enter().append("g")
                    .attr("class", "node")
                    .attr("transform", function(d) {
                        return "translate(" + d.y + "," + d.x + ")";
                    });

                nodeEnter.append('text')
                        .attr('text-anchor', 'middle')
                        .attr('dominant-baseline', 'central')
                        .attr('font-family', 'FontAwesome')
                        .text(function(d) { return d.icon; });

                nodeEnter.append("text")
                    .attr("x", function(d) {
                        return d.children || d._children ? -13 : 13;
                    })
                    .attr("dy", ".35em")
                    .attr("text-anchor", function(d) {
                        return d.children || d._children ? "end" : "start";
                    })
                    .text(function(d) {
                        return d.name;
                    })
                    .style("fill-opacity", 1);

                // Declare the links!
                var link = svg.selectAll("path.link")
                    .data(links, function(d) {
                        return d.target.id;
                    });

                // Enter the links.
                link.enter().insert("path", "g")
                    .attr("class", "link")
                    .attr("d", diagonal);

            }
"""


def print_chapter_divs(chapters):
    """
    Print sections for each chapter in body.

    Example:
    <h3>Graph 1</h3>
    <div id="area1"></div>
    """
    for key in sorted(chapters.keys()):
        print '<h3>%s</h3>' % key
        div_id = create_div_id(key)
        print '<div id="%s"></div>' % div_id
        print ''


def print_chapter_javascript(chapters):
    """Print Javascript for each chapter."""
    for key in sorted(chapters.keys()):
        print '<script type="text/javascript">'
        print chapters[key].encode('utf-8')
        div_id = create_div_id(key)
        print_javascript_function(div_id)
        print '</script>'


def create_div_id(key):
    """
    One method to take course name and do the following:
    1) make lower case
    2) remove white space
    3) remove non-alphanumeric charachters
    """
    return re.sub(r'\W+', '', key.lower().replace(' ', ''))


def main(filename):
    """Print working single, self contained HTML page with only external dependency on d3.js."""
    chapters = get_chapter_data(filename)
    print_html_header()
    print_chapter_divs(chapters)
    print_chapter_javascript(chapters)
    print_html_footer()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('filename', help='MongoDB data dumped to file')
    ARGS = PARSER.parse_args()

    main(ARGS.filename)
