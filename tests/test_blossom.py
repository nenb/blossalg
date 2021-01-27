from __future__ import unicode_literals
import pytest
from conftest import snode


def test_ancestors_leaf(binary_tree_path):
    assert binary_tree_path.nodes[6].ancestor_path() == [
        binary_tree_path.nodes[6],
        binary_tree_path.nodes[2],
        binary_tree_path.nodes[0],
    ]


def test_ancestors_root(binary_tree_path):
    assert binary_tree_path.nodes[0].ancestor_path() == [
        binary_tree_path.nodes[0]
    ]


def test_contract_blossom(stem_and_blossom_match):
    nodelist = list(stem_and_blossom_match.nodes.values())
    snode.cycle = nodelist[3:7]
    new_nodelist = snode.contract_nodelist(nodelist)

    stem_and_blossom_match.nodes = {node.name: node for node in new_nodelist}
    stem_and_blossom_match.compute_edges()

    errors = []
    if stem_and_blossom_match.edges != {(0, 1): 1, (1, 2): 1, (2, 8): 1}:
        errors.append("edge error")
    if stem_and_blossom_match.nodes[2].match.name != 8:
        errors.append("stem match error")
    if stem_and_blossom_match.nodes[8].match.name != 2:
        errors.append("blossom match error")
    assert errors == []


def test_expand_blossom(stem_and_blossom_match):
    orig_nodelist = list(stem_and_blossom_match.nodes.values())

    # First contract nodelist
    snode.cycle = orig_nodelist[3:7]
    contract_nodelist = snode.contract_nodelist(orig_nodelist)

    # Now expand nodelist
    expand_nodelist = snode.expand_nodelist(contract_nodelist)
    stem_and_blossom_match.nodes = {
        node.name: node for node in expand_nodelist
    }
    stem_and_blossom_match.compute_edges()

    errors = []
    if stem_and_blossom_match.edges != {
        (0, 1): 1,
        (1, 2): 1,
        (2, 3): 1,
        (3, 4): 1,
        (3, 6): 1,
        (4, 5): 1,
        (5, 6): 1,
    }:
        errors.append("edge error")
    if stem_and_blossom_match.nodes[0].match.name != 1:
        errors.append("stem match error")
    if stem_and_blossom_match.nodes[1].match.name != 0:
        errors.append("stem match error")
    if stem_and_blossom_match.nodes[2].match.name != 3:
        errors.append("stem match error")
    if stem_and_blossom_match.nodes[3].match.name != 2:
        errors.append("stem match error")
    if stem_and_blossom_match.nodes[4].match.name != 5:
        errors.append("blossom match error")
    if stem_and_blossom_match.nodes[5].match.name != 4:
        errors.append("blossom match error")
    assert errors == []


@pytest.mark.parametrize(
    "i,j,node_nums",
    [
        (0, 6, [0, 6, 5, 4, 3, 2, 1]),
        (6, 0, [6, 0, 1]),
        (2, 3, [2, 3, 4, 5, 6, 0, 1]),
        (3, 2, [3, 2, 1]),
    ],
)
def test_cycle_path(i, j, node_nums, cycle_match):
    nodes = list(cycle_match.nodes.values())
    path = nodes[i].cycle_aug_path(nodes[j], nodes)

    nodepath = []
    for num in node_nums:
        nodepath.append(nodes[num])

    assert path == nodepath


def test_expand_path_forward(bud_match):
    cycle = list(bud_match.nodes.values())[1:6]
    snode.cycle = cycle

    nodelist = snode.contract_nodelist(list(bud_match.nodes.values()))
    bud_match.nodes = {node.name: node for node in nodelist}

    path = [bud_match.nodes[0], snode, bud_match.nodes[6], bud_match.nodes[7]]
    aug_path = snode.expand_path(path, cycle)

    nodelist = snode.expand_nodelist(nodelist)
    bud_match.nodes = {node.name: node for node in nodelist}

    assert aug_path == [
        bud_match.nodes[0],
        bud_match.nodes[1],
        bud_match.nodes[5],
        bud_match.nodes[4],
        bud_match.nodes[6],
        bud_match.nodes[7],
    ]


def test_expand_path_reverse(bud_match):
    cycle = list(bud_match.nodes.values())[1:6]
    snode.cycle = cycle

    nodelist = snode.contract_nodelist(list(bud_match.nodes.values()))
    bud_match.nodes = {node.name: node for node in nodelist}

    reverse_path = [
        bud_match.nodes[7],
        bud_match.nodes[6],
        snode,
        bud_match.nodes[0],
    ]
    aug_path = snode.expand_path(reverse_path, cycle)

    nodelist = snode.expand_nodelist(nodelist)
    bud_match.nodes = {node.name: node for node in nodelist}

    assert aug_path == [
        bud_match.nodes[7],
        bud_match.nodes[6],
        bud_match.nodes[4],
        bud_match.nodes[5],
        bud_match.nodes[1],
        bud_match.nodes[0],
    ]


def test_expand_path_head(blossom_tail_match):
    cycle = list(blossom_tail_match.nodes.values())[3:8]
    snode.cycle = cycle

    nodelist = snode.contract_nodelist(list(blossom_tail_match.nodes.values()))
    blossom_tail_match.nodes = {node.name: node for node in nodelist}

    reverse_path = [
        blossom_tail_match.nodes[8],
        blossom_tail_match.nodes[2],
        blossom_tail_match.nodes[1],
        blossom_tail_match.nodes[0],
    ]
    aug_path = snode.expand_path(reverse_path, cycle)

    nodelist = snode.expand_nodelist(nodelist)
    blossom_tail_match.nodes = {node.name: node for node in nodelist}

    assert aug_path == [
        blossom_tail_match.nodes[7],
        blossom_tail_match.nodes[6],
        blossom_tail_match.nodes[5],
        blossom_tail_match.nodes[4],
        blossom_tail_match.nodes[3],
        blossom_tail_match.nodes[2],
        blossom_tail_match.nodes[1],
        blossom_tail_match.nodes[0],
    ]


def test_expand_path_tail(blossom_tail_match):
    cycle = list(blossom_tail_match.nodes.values())[3:8]
    snode.cycle = cycle

    nodelist = snode.contract_nodelist(list(blossom_tail_match.nodes.values()))
    blossom_tail_match.nodes = {node.name: node for node in nodelist}

    path = [
        blossom_tail_match.nodes[0],
        blossom_tail_match.nodes[1],
        blossom_tail_match.nodes[2],
        blossom_tail_match.nodes[8],
    ]
    aug_path = snode.expand_path(path, cycle)

    nodelist = snode.expand_nodelist(nodelist)
    blossom_tail_match.nodes = {node.name: node for node in nodelist}

    assert aug_path == [
        blossom_tail_match.nodes[0],
        blossom_tail_match.nodes[1],
        blossom_tail_match.nodes[2],
        blossom_tail_match.nodes[3],
        blossom_tail_match.nodes[4],
        blossom_tail_match.nodes[5],
        blossom_tail_match.nodes[6],
        blossom_tail_match.nodes[7],
    ]


def test_matching_stem_and_blossom(stem_and_blossom_match):
    for node in list(stem_and_blossom_match.nodes.values()):
        node.match = None
    stem_and_blossom_match.compute_edges()
    stem_and_blossom_match.find_max_matching()

    assert stem_and_blossom_match.compute_size_matching() == 3


def test_matching_bud(bud_match):
    for node in list(bud_match.nodes.values()):
        node.match = None
    bud_match.compute_edges()
    bud_match.find_max_matching()

    assert bud_match.compute_size_matching() == 4


def test_matching_blossom_tail(blossom_tail_match):
    for node in list(blossom_tail_match.nodes.values()):
        node.match = None
    blossom_tail_match.compute_edges()
    blossom_tail_match.find_max_matching()

    assert blossom_tail_match.compute_size_matching() == 4


def test_matching_binary_tree(binary_tree_path):
    for node in list(binary_tree_path.nodes.values()):
        node.match = None
    binary_tree_path.compute_edges()
    binary_tree_path.clean_graph()
    binary_tree_path.find_max_matching()

    assert binary_tree_path.compute_size_matching() == 2


def test_matching_triangle(triangle):
    triangle.compute_edges()
    triangle.find_max_matching()

    assert triangle.compute_size_matching() == 1
