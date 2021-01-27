<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/5/5b/6n-graf.svg" alt="Logo" />
</p>
<h1 align="center">blossalg</h1>

<p align="center">
  <a href="https://github.com/nenb/bloassalg/actions?workflow=CI">
    <img src="https://github.com/nenb/blossalg/workflows/CI/badge.svg" alt="CI Status" />
  </a>
  <a href="https://codecov.io/gh/nenb/blossalg">
    <img src="https://codecov.io/gh/nenb/blossalg/branch/main/graph/badge.svg" alt="Test Coverage" />
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black" />
  </a>
</p>

blossalg is a Python implementation of the Edmonds algorithm for constructing maximum matchings on graphs.
For more information on how the Edmonds algorithm works see the [Wikipedia](https://en.wikipedia.org/wiki/Blossom_algorithm) page.




## Installation

You can install blossalg from PyPI:

```sh
pip install blossalg
```
blossalg is supported on Python 2.7 and Python 3.8.

## Usage

You can run blossalg as follows:

```sh
blossalg infile.csv [outfile.txt]
```

The input file `infile.csv` contains information on the number of nodes and the neighbours
of each node. This information is stored using a series of comma-delimited
binary-valued strings. Nodes are identified by different rows and columns
and a value of 1 indicates a node neighbour. By convention a node cannot be
a neighbour with itself.

For example, the input file of a three node graph where both node 0 and node 2
are neighbours of node 1 would look as follows:
```
0,1,0
1,0,1
0,1,0
```

Given an input file, blossalg will compute the maximum matching
using the Edmonds blossom algorithm. The total number of
matched nodes will then be output to screen.

If an output file `outfile.txt` is supplied the matched pairs from the
maximal matching will be saved to the file. The format of the output is as follows.
Each node and its matched node will be stored as `node_number: matched_node_number`.
The node number will correspond to the node number from the input file (e.g. row 1
in the input file will represent node 0 in the output file). Each matched pair in
the output file will be separated by a newline. By convention, unmatched nodes are
not included in the outfile.
