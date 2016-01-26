var margin = {
        top: 0,
        right: 0,
        bottom: 40,
        left: 40
    },
    width = $(document).width(),
    height = $(document).height();

var i = 0;
var duration = 1000;
var root;

var tree = d3.layout.tree()
    .size([height, width]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) {
        return [d.y, d.x];
    });

var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
        return "<span>" + d.tip + "</span>";
    });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + ")");

svg.call(tip);


var collapse = function(d) {
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
        d.y = d.depth * 300;
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

    nodeEnter.append("text")
        .attr("x", function(d) {
            return d.children || d._children ? -10 : 10;
        })
        .attr("dy", ".35em")
        .attr('font-family', 'FontAwesome')
        .text(function(d) {
            return d.icon + ' ' + d.name;
        })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function(d) {
            return "translate(" + d.y + "," + d.x + ")";
        });

    nodeUpdate.select("text")
        .style("fill", function(d) {
            return d._children ? "#e72528" : "#FF9933";
        });

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function(d) {
            return "translate(" + source.y + "," + source.x + ")";
        })
        .remove();

    nodeExit.select('text')
        .attr('font-family', 'FontAwesome')
        .text(function(d) {
            return d.icon + ' ' + d.name;
        });

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
    map[node.id] = node;
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
