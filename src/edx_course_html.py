#!/usr/bin/python
"""
Print out self-contained HTML page with visualization. However, does require internet access to
download the d3.js script.
"""
import argparse
import re

from edx_course_map import get_course_data


def print_html_header():
    """Print the header and start of the body of the HTML document."""
    print """<!DOCTYPE html>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>OCV</title>
<meta name="description" content="Online Course Visualizer">

<style type="text/css">
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

    .node {
        cursor: pointer;
    }

    .overlay {
        background-color: #DDD;
    }

    .node circle {
        fill: #fff;
        stroke: steelblue;
        stroke-width: 1.5px;
    }

    .node text {
        font-size: 10px;
    }

    .link {
        fill: none;
        stroke: #ccc;
        stroke-width: 1.5px;
    }

    .templink {
        fill: none;
        stroke: red;
        stroke-width: 3px;
    }

    .ghostCircle.show {
        display: block;
    }

    .ghostCircle,
    .activeDrag .ghostCircle {
        display: none;
    }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0-alpha1/jquery.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.js"></script>
<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Cantarell" />
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">

<body>
<script type="text/javascript">
"""


def print_html_footer():
    """Finish off the HTML tags."""
    print """
</script>
</body>
</html>
"""


def print_javascript_function():
    """Print all the icky javascript."""
    print """
    var margin = {
            top: 20,
            right: 0,
            bottom: 40,
            left: 200
        },
        width = $(document).width(),
        height = $(document).height();

    var i = 0;
    var duration = 750;
    var root;

    var tree = d3.layout.tree()
        .size([height, width]);

    var tree = d3.layout.tree()
        .size([height, width]);

    var diagonal = d3.svg.diagonal()
        .projection(function (d) {
            return [d.y, d.x];
        });

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.right + margin.left)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + ")");

    d3.select(self.frameElement).style("height", "800px");

    var collapse = function (d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    };

    var zoom = function() {
        var scale = d3.event.scale,
            translation = d3.event.translate,
            tbound = -height * scale,
            bbound = height * scale,
            lbound = (-width + margin.right) * scale,
            rbound = (width - margin.left) * scale;
        // limit translation to thresholds
        translation = [
            Math.max(Math.min(translation[0], rbound), lbound),
            Math.max(Math.min(translation[1], bbound), tbound)
        ];
        svg.attr("transform", "translate(" + translation + ")" + " scale(" + scale + ")");
    };

    // Toggle children on click.
    var click = function(d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            d.children = d._children;
            d._children = null;
        }
        update(d);
    };

    var update = function(source) {
        // Compute the new tree layout.
        var nodes = tree.nodes(root).reverse(),
            links = tree.links(nodes);

        // Normalize for fixed-depth.
        nodes.forEach(function(d) {
            d.y = d.depth * 180;
        });

        // Update the nodes...
        var node = svg.selectAll("g.node")
            .data(nodes, function(d) {
                return d.id || (d.id = ++i);
            });

        // Enter any new nodes at the parent's previous position.
        var nodeEnter = node.enter().append("g")
            .attr("class", "node")
            .attr("transform", function(d) {
                return "translate(" + source.y0 + "," + source.x0 + ")";
            })
            .on("click", click);

        nodeEnter.append("circle")
            .attr("r", 1e-6)
            .style("fill", function(d) {
                return d._children ? "lightsteelblue" : "#fff";
            });

        nodeEnter.append("text")
            .attr("x", function(d) {
                return d.children || d._children ? -10 : 10;
            })
            .attr("dy", ".35em")
            .attr("text-anchor", function(d) {
                return d.children || d._children ? "end" : "start";
            })
            .text(function(d) {
                return d.icon + " " + d.name;
            })
            .style("fill-opacity", 1e-6);

        // Transition nodes to their new position.
        var nodeUpdate = node.transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + d.y + "," + d.x + ")";
            });

        nodeUpdate.select("circle")
            .attr("r", 8)
            .style("fill", function(d) {
                return d._children ? "lightsteelblue" : "#fff";
            });

        nodeUpdate.select("text")
            .style("fill-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + source.y + "," + source.x + ")";
            })
            .remove();

        nodeExit.select("circle")
            .attr("r", 1e-6);

        nodeExit.select("text")
            .style("fill-opacity", 1e-6);

        // Update the links...
        var link = svg.selectAll("path.link")
            .data(links, function(d) {
                return d.target.id;
            });

        // Enter any new links at the parent's previous position.
        link.enter().insert("path", "g")
            .attr("class", "link")
            .attr("d", function(d) {
                var o = {
                    x: source.x0,
                    y: source.y0
                };
                return diagonal({
                    source: o,
                    target: o
                });
            });

        // Transition links to their new position.
        link.transition()
            .duration(duration)
            .attr("d", diagonal);

        // Transition exiting nodes to the parent's new position.
        link.exit().transition()
            .duration(duration)
            .attr("d", function(d) {
                var o = {
                    x: source.x,
                    y: source.y
                };
                return diagonal({
                    source: o,
                    target: o
                });
            })
            .remove();

        // Stash the old positions for transition.
        nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });

        d3.select("svg").call(d3.behavior.zoom().scaleExtent([1, 8]).on("zoom", zoom));
    };


    var dataMap = data.reduce(function(map, node) {
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

    root = treeData[0];
    root.x0 = height / 2;
    root.y0 = 0;

    root.children.forEach(collapse);

    update(root);

"""


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
    course_data = get_course_data(filename)

    print_html_header()
    for data in course_data:
        print data.encode('utf-8')
    print_javascript_function()
    print_html_footer()

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('filename', help='MongoDB data dumped to file')
    ARGS = PARSER.parse_args()

    main(ARGS.filename)
