"""Construct a maximum matching on a graph using the blossom algorithm.

Usage:
------

    $ blossalg infile.csv [outfile.txt]

Description of infile:

    The infile contains information on the number of nodes and the neighbours
    of each node. This information is stored using a series of comma-delimited
    binary-valued strings. Node N is identified by both the (N+1)th row and
    column and a value of 1 indicates a node neighbour. By convention a node
    cannot be a neighbour with itself.

    For example, the infile of a three node graph where both node 0 and node 2
    are neighbours of node 1 would look as follows:

    0,1,0
    1,0,1
    0,1,0

Description of program output:

    The program will compute the maximum matching of a user-supplied graph
    using the blossom algorithm. The total number of matched nodes will be
    output to screen. If an outfile is supplied (optional) the matched pairs
    from this maximal matching will be saved to the file.

Description of outfile (optional):

    In a user-supplied outfile, each node and its matched node will be stored
    as 'node_number: matched_node_number'. The node number will correspond to
    the node number from the infile (e.g. row 1 in the infile will represent
    node 0 in the outfile). Each matched pair in the outfile will be separated
    by a newline. By convention, unmatched nodes are not included in the
    outfile.

Available options are:

    -h, --help         Show this help

Contact:
--------

- https://github.com/nenb

Version:
--------

- blossalg v1.0.0
"""
from __future__ import print_function
from __future__ import unicode_literals

# Standard library imports
from builtins import range
import re
import sys
import csv

from .blossom import Node, Graph

USAGE = "Usage: {} 'infile.csv' ['outfile.txt']".format(sys.argv[0])

args_pattern = re.compile(
    r"""
    ^
    (
    (?P<HELP>-h|--help)|
    ((?P<ARG1>\w+\.csv))
    (\s(?P<ARG2>\w+\.txt$))?
    )
    $
""",
    re.VERBOSE,
)


def parse(arg_line):
    args = {}
    match_object = args_pattern.match(arg_line)
    if match_object:
        args = {
            k: v
            for k, v in list(match_object.groupdict().items())
            if v is not None
        }
    return args


def read_infile(infile):
    node_array = []
    with open(infile) as csvfile:
        for row in csv.reader(csvfile, delimiter=str(",")):
            neighbours = [idx for idx, row in enumerate(row) if row == "1"]
            node_array.append(neighbours)
    if len(node_array) == 0:
        raise SystemExit("Empty graph. Please supply a valid graph.")
    return node_array


def compute_max_matching(node_array):
    # Create node instances, fill node neighbours
    nodelist = [Node() for _ in range(len(node_array))]
    for idx, node in enumerate(node_array):
        nodelist[idx].neighbors = [nodelist[node] for node in node]

    # Create graph instance, construct graph
    graph = Graph()
    graph.nodes = {node.name: node for node in nodelist}
    graph.compute_edges()

    # Compute maximum matching
    graph.find_max_matching()

    return graph


def save_matched_pairs(matched_dict, outfile):
    with open(outfile, "w") as textfile:
        for pair in list(matched_dict.items()):
            string = "{}:{}\n".format(pair[0], pair[1])
            textfile.write(string)


def main():
    args = parse(" ".join(sys.argv[1:]))
    if not args:
        raise SystemExit(USAGE)
    if args.get("HELP"):
        print(USAGE)
        return

    node_array = read_infile(args["ARG1"])
    matched_graph = compute_max_matching(node_array)

    # Multiple by two to convert number of matched pairs to matched nodes.
    outstring = (
        """There are {} matched nodes in maximum matched graph.""".format(
            int(2 * matched_graph.compute_size_matching())
        )
    )
    print(outstring)

    if args.get("ARG2"):
        matched_dict = matched_graph.create_matching_dict()
        save_matched_pairs(matched_dict, args["ARG2"])


if __name__ == "__main__":
    main()
