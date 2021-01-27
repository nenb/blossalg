from __future__ import unicode_literals
from builtins import range
import pytest
from blossom import blossom

# WARNING
# Tests have been developed under the assumption
# that there are 8 nodes and 1 supernode. Tests
# may fail in unexpected ways if this assumption
# is no longer valid.

# Create 8 node instances and 1 supernode instance.
nodelist = [blossom.Node() for _ in range(7)]
nodelist2 = nodelist + [blossom.Node()]
snode = blossom.Supernode()


@pytest.fixture
def binary_tree_path():

    #          .
    #         | \
    #        .   .
    #       | \ | \
    #      .  . .  .

    nodelist[0].neighbors = [nodelist[1], nodelist[2]]
    nodelist[1].neighbors = [nodelist[0], nodelist[3], nodelist[4]]
    nodelist[2].neighbors = [nodelist[0], nodelist[5], nodelist[6]]
    nodelist[3].neighbors = [nodelist[1]]
    nodelist[4].neighbors = [nodelist[1]]
    nodelist[5].neighbors = [nodelist[2]]
    nodelist[6].neighbors = [nodelist[2]]

    nodelist[0].parent = nodelist[0]
    nodelist[1].parent = nodelist[0]
    nodelist[2].parent = nodelist[0]
    nodelist[3].parent = nodelist[1]
    nodelist[4].parent = nodelist[1]
    nodelist[5].parent = nodelist[2]
    nodelist[6].parent = nodelist[2]

    for i in range(7):
        nodelist[i].root = nodelist[0]

    graph = blossom.Graph()
    graph.nodes = {n.name: n for n in nodelist}

    return graph


@pytest.fixture
def stem_and_blossom_match():

    #        .
    #       m\m
    #        .
    #        |
    #        .
    #       m\m
    #        .
    #       | \
    #      .  .
    #      \ m|m
    #       .
    #
    # 'm' indicates matched edge

    nodelist[0].neighbors = [nodelist[1]]
    nodelist[1].neighbors = [nodelist[0], nodelist[2]]
    nodelist[2].neighbors = [nodelist[1], nodelist[3]]
    nodelist[3].neighbors = [nodelist[2], nodelist[4], nodelist[6]]
    nodelist[4].neighbors = [nodelist[3], nodelist[5]]
    nodelist[5].neighbors = [nodelist[4], nodelist[6]]
    nodelist[6].neighbors = [nodelist[3], nodelist[5]]

    nodelist[0].match = nodelist[1]
    nodelist[1].match = nodelist[0]
    nodelist[2].match = nodelist[3]
    nodelist[3].match = nodelist[2]
    nodelist[4].match = nodelist[5]
    nodelist[5].match = nodelist[4]
    nodelist[6].match = None

    graph = blossom.Graph()
    graph.nodes = {node.name: node for node in nodelist}

    return graph


@pytest.fixture
def cycle_match():

    #
    #        .
    #      m|m\
    #      .   .
    #     |    \
    #     .    .
    #    m\m  m|m
    #      .--.
    #
    # 'm' indicates matched edge

    nodelist[0].neighbors = [nodelist[1], nodelist[6]]
    nodelist[1].neighbors = [nodelist[0], nodelist[2]]
    nodelist[2].neighbors = [nodelist[1], nodelist[3]]
    nodelist[3].neighbors = [nodelist[2], nodelist[4]]
    nodelist[4].neighbors = [nodelist[3], nodelist[5]]
    nodelist[5].neighbors = [nodelist[4], nodelist[6]]
    nodelist[6].neighbors = [nodelist[5], nodelist[0]]

    nodelist[0].match = nodelist[6]
    nodelist[6].match = nodelist[0]
    nodelist[2].match = nodelist[3]
    nodelist[3].match = nodelist[2]
    nodelist[4].match = nodelist[5]
    nodelist[5].match = nodelist[4]
    nodelist[1].match = None

    graph = blossom.Graph()
    graph.nodes = {node.name: node for node in nodelist}

    return graph


@pytest.fixture
def bud_match():

    #
    #        .
    #        |
    #        .
    #      m|m\
    #      .   .
    #      \  m|m
    #      .--.
    #     m\m
    #      .
    #      \
    #      .
    #
    # 'm' indicates matched edge

    nodelist2[0].neighbors = [nodelist2[1]]
    nodelist2[1].neighbors = [nodelist2[0], nodelist2[2], nodelist2[5]]
    nodelist2[2].neighbors = [nodelist2[1], nodelist2[3]]
    nodelist2[3].neighbors = [nodelist2[2], nodelist2[4]]
    nodelist2[4].neighbors = [nodelist2[3], nodelist2[5], nodelist2[6]]
    nodelist2[5].neighbors = [nodelist2[4], nodelist2[1]]
    nodelist2[6].neighbors = [nodelist2[4], nodelist2[7]]
    nodelist2[7].neighbors = [nodelist2[6]]

    nodelist2[0].match = None
    nodelist2[1].match = nodelist2[5]
    nodelist2[2].match = nodelist2[3]
    nodelist2[3].match = nodelist2[2]
    nodelist2[4].match = nodelist2[6]
    nodelist2[5].match = nodelist2[1]
    nodelist2[6].match = nodelist2[4]
    nodelist2[7].match = None

    graph = blossom.Graph()
    graph.nodes = {node.name: node for node in nodelist2}

    return graph


@pytest.fixture
def blossom_tail_match():

    #        .
    #        \
    #        .
    #       m|m
    #        .
    #        \
    #        .--.
    #       m\m \
    #        .  .
    #        \m|m
    #         .
    #
    # 'm' indicates matched edge

    nodelist2[0].neighbors = [nodelist2[1]]
    nodelist2[1].neighbors = [nodelist2[0], nodelist2[2]]
    nodelist2[2].neighbors = [nodelist2[1], nodelist2[3]]
    nodelist2[3].neighbors = [nodelist2[2], nodelist2[4], nodelist2[7]]
    nodelist2[4].neighbors = [nodelist2[3], nodelist2[5]]
    nodelist2[5].neighbors = [nodelist2[4], nodelist2[6]]
    nodelist2[6].neighbors = [nodelist2[5], nodelist2[7]]
    nodelist2[7].neighbors = [nodelist2[6], nodelist2[3]]

    nodelist2[0].match = None
    nodelist2[1].match = nodelist2[2]
    nodelist2[2].match = nodelist2[1]
    nodelist2[3].match = nodelist2[4]
    nodelist2[4].match = nodelist2[3]
    nodelist2[5].match = nodelist2[6]
    nodelist2[6].match = nodelist2[5]
    nodelist2[7].match = None

    graph = blossom.Graph()
    graph.nodes = {node.name: node for node in nodelist2}

    return graph


@pytest.fixture
def triangle():

    #        .
    #       | \
    #      .--.
    #

    nodelist2[0].neighbors = [nodelist2[1], nodelist2[2]]
    nodelist2[1].neighbors = [nodelist2[2], nodelist2[0]]
    nodelist2[2].neighbors = [nodelist2[0], nodelist2[1]]
    nodelist2[3].neighbors = []
    nodelist2[4].neighbors = []
    nodelist2[5].neighbors = []
    nodelist2[6].neighbors = []
    nodelist2[7].neighbors = []

    nodelist2[0].match = None
    nodelist2[1].match = None
    nodelist2[2].match = None
    nodelist2[3].match = None
    nodelist2[4].match = None
    nodelist2[5].match = None
    nodelist2[6].match = None
    nodelist2[7].match = None

    graph = blossom.Graph()
    graph.nodes = {node.name: node for node in nodelist2}

    return graph
