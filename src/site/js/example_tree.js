var data = [{
    "name": "Example Week 2: Get Interactive",
    "parent": "null",
    "type": "chapter"
}, {
    "name": "Lesson 2 - Let's Get Interactive!",
    "parent": "Example Week 2: Get Interactive",
    "type": "chapter"
}, {
    "name": "Lesson 2 - Let's Get Interactive! ",
    "parent": "Lesson 2 - Let's Get Interactive!",
    "type": "sequential"
}, {
    "name": "Lesson 2: Let's Get Interactive!",
    "parent": "Lesson 2 - Let's Get Interactive! ",
    "type": "vertical"
}, {
    "name": "An Interactive Reference Table",
    "parent": "Lesson 2 - Let's Get Interactive!",
    "type": "sequential"
}, {
    "name": "An Interactive Reference Table",
    "parent": "An Interactive Reference Table",
    "type": "vertical"
}, {
    "name": "6f7a6670f87147149caeff6afa07a526",
    "parent": "An Interactive Reference Table",
    "type": "vertical"
}, {
    "name": "Zooming Diagrams",
    "parent": "Lesson 2 - Let's Get Interactive!",
    "type": "sequential"
}, {
    "name": "Zooming Diagrams",
    "parent": "Zooming Diagrams",
    "type": "vertical"
}, {
    "name": "e0d7423118ab432582d03e8e8dad8e36",
    "parent": "Zooming Diagrams",
    "type": "vertical"
}, {
    "name": "Electronic Sound Experiment",
    "parent": "Lesson 2 - Let's Get Interactive!",
    "type": "sequential"
}, {
    "name": "Electronic Sound Experiment",
    "parent": "Electronic Sound Experiment",
    "type": "vertical"
}, {
    "name": "03f051f9a8814881a3783d2511613aa6",
    "parent": "Electronic Sound Experiment",
    "type": "vertical"
}, {
    "name": "Homework - Labs and Demos",
    "parent": "Example Week 2: Get Interactive",
    "type": "chapter"
}, {
    "name": "Labs and Demos",
    "parent": "Homework - Labs and Demos",
    "type": "sequential"
}, {
    "name": "Labs and Demos",
    "parent": "Labs and Demos",
    "type": "vertical"
}, {
    "name": "Molecule Editor",
    "parent": "Homework - Labs and Demos",
    "type": "sequential"
}, {
    "name": "2b94658d2eee4d85ae13f83bc24cfca9",
    "parent": "Molecule Editor",
    "type": "vertical"
}, {
    "name": "Molecule Editor",
    "parent": "Molecule Editor",
    "type": "vertical"
}, {
    "name": "0aa7a3bdbe18427795b0c1a1d7c3cb9a",
    "parent": "Molecule Editor",
    "type": "vertical"
}, {
    "name": "Code Grader",
    "parent": "Homework - Labs and Demos",
    "type": "sequential"
}, {
    "name": "Code Grader",
    "parent": "Code Grader",
    "type": "vertical"
}, {
    "name": "python_grader",
    "parent": "Code Grader",
    "type": "vertical"
}, {
    "name": "c6cd4bea43454aaea60ad01beb0cf213",
    "parent": "Code Grader",
    "type": "vertical"
}, {
    "name": "Electric Circuit Simulator",
    "parent": "Homework - Labs and Demos",
    "type": "sequential"
}, {
    "name": "Electronic Circuit Simulator",
    "parent": "Electric Circuit Simulator",
    "type": "vertical"
}, {
    "name": "free_form_simulation",
    "parent": "Electric Circuit Simulator",
    "type": "vertical"
}, {
    "name": "logic_gate_problem",
    "parent": "Electric Circuit Simulator",
    "type": "vertical"
}, {
    "name": "4f06b358a96f4d1dae57d6d81acd06f2",
    "parent": "Electric Circuit Simulator",
    "type": "vertical"
}, {
    "name": "Protein Creator",
    "parent": "Homework - Labs and Demos",
    "type": "sequential"
}, {
    "name": "Protein Builder",
    "parent": "Protein Creator",
    "type": "vertical"
}, {
    "name": "Designing Proteins in Two Dimensions",
    "parent": "Protein Creator",
    "type": "vertical"
}, {
    "name": "ed01bcd164e64038a78964a16eac3edc",
    "parent": "Protein Creator",
    "type": "vertical"
}, {
    "name": "Homework - Essays",
    "parent": "Example Week 2: Get Interactive",
    "type": "chapter"
}, {
    "name": "Peer Assessed Essays",
    "parent": "Homework - Essays",
    "type": "sequential"
}, {
    "name": "b24c33ea35954c7889e1d2944d3fe397",
    "parent": "Peer Assessed Essays",
    "type": "vertical"
}, {
    "name": "Peer Grading",
    "parent": "Peer Assessed Essays",
    "type": "vertical"
}, ];




var dataMap = data.reduce(function (map, node) {
    map[node.name] = node;
    return map;
}, {});

var treeData = [];
data.forEach(function (node) {
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
    .projection(function (d) {
    return [d.y, d.x];
});

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.right + margin.left)
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
    nodes.forEach(function (d) {
        d.y = d.depth * 180;
    });

    // Declare the nodesâ€¦
    var node = svg.selectAll("g.node")
        .data(nodes, function (d) {
        return d.id || (d.id = ++i);
    });

    // Enter the nodes.
    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function (d) {
        return "translate(" + d.y + "," + d.x + ")";
    });

    nodeEnter.append("circle")
        .attr("r", 10)
        .style("fill", "#fff");

    nodeEnter.append("text")
        .attr("x", function (d) {
        return d.children || d._children ? -13 : 13;
    })
        .attr("dy", ".35em")
        .attr("text-anchor", function (d) {
        return d.children || d._children ? "end" : "start";
    })
        .text(function (d) {
        return d.name;
    })
        .style("fill-opacity", 1);

    // Declare the linksâ€¦
    var link = svg.selectAll("path.link")
        .data(links, function (d) {
        return d.target.id;
    });

    // Enter the links.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", diagonal);

}
