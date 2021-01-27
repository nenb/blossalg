"""Classes for constructing graph, methods for computing maximum matching"""
from __future__ import division
from __future__ import unicode_literals
from past.utils import old_div
from builtins import object
import logging

# Logger setup - output errors only to blossom_errorfile
logger = logging.getLogger(__name__)
f_handler = logging.FileHandler("blossom_errorfile.log")
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


class Node(object):
    _name = 0

    def __init__(self):
        self.name = Node._name
        Node._name += 1
        self.neighbors = []
        self.match = None
        self.mark = False
        self.parent = None
        self.root = None

    def ancestor_path(self):
        """Compute the path from a node to its root"""
        path = [self]
        node = self
        while node != node.root:
            node = node.parent
            path.append(node)
        return path

    def cycle_aug_path(self, match_node, cycle):
        """Compute an augmenting path on a cycle graph"""
        idx1 = cycle.index(self)
        idx2 = cycle.index(match_node)
        path = []

        if (idx1 > 0 and idx2 == idx1 - 1) or (
            idx1 == 0 and idx2 == len(cycle) - 1
        ):
            reverse_cycle = cycle[idx1::-1] + cycle[:idx1:-1]
            for node in reverse_cycle:
                path.append(node)
                if node.match not in reverse_cycle:
                    return path
            logger.error("No matched node in reverse_cycle.")

        else:
            forward_cycle = cycle[idx1::] + cycle[:idx1]
            for node in forward_cycle:
                path.append(node)
                if node.match not in forward_cycle:
                    return path
            logger.error("No matched node in forward_cycle.")


class Supernode(Node):
    def __init__(self, cycle=None):
        super(Supernode, self).__init__()
        self.cycle = cycle

    def contract_nodelist(self, nodelist):
        """Contract a cycle to a supernode"""
        # Remove cycle from nodelist
        nodelist = [node for node in nodelist if node not in self.cycle]
        nodelist.append(self)

        # Compute supernode neighbors
        for node in self.cycle:
            if node.match and node.match not in self.cycle:
                self.match = node.match
            for neighbor in node.neighbors:
                if neighbor not in self.cycle:
                    self.neighbors.append(neighbor)
        self.neighbors = list(set(self.neighbors))

        # Modify node neighbors if neighbor in cycle
        for node in nodelist:
            if node.match in self.cycle:
                node.match = self
            node.neighbors = [
                neighbor
                for neighbor in node.neighbors
                if neighbor not in self.cycle
            ]
            if node in self.neighbors:
                node.neighbors.append(self)

        return nodelist

    def expand_nodelist(self, nodelist):
        """Expand a supernode to a cycle"""
        # Remove supernode from nodelist
        nodelist = [node for node in nodelist if node is not self]
        for node in nodelist:
            node.neighbors = [
                neighbor for neighbor in node.neighbors if neighbor is not self
            ]

        # Modify node neighbors if node is cycle neighbor and not in cycle
        for cnode in self.cycle:
            nodelist.append(cnode)
            if cnode.match and cnode.match not in self.cycle:
                cnode.match.match = cnode
            for node in cnode.neighbors:
                if node not in self.cycle:
                    node.neighbors.append(cnode)

        return nodelist

    def expand_path(self, path, cycle):
        """Replace supernode in augmenting path with corresponding cycle
        nodes"""
        if self not in path:
            return path

        elif self == path[0]:
            for node in cycle:
                if path[1] in node.neighbors:
                    if node.match:
                        cpath = node.cycle_aug_path(node.match, cycle)
                    else:
                        cpath = [node]
                    return cpath[::-1] + path[1:]
            logger.error("Supernode (head) not connected to rest of graph.")

        elif self == path[-1]:
            for node in cycle:
                if path[-2] in node.neighbors:
                    if node.match:
                        cpath = node.cycle_aug_path(node.match, cycle)
                    else:
                        cpath = [node]
                    return path[:-1] + cpath
            logger.error("Supernode (tail) not connected to rest of graph.")

        else:
            idx = path.index(self)
            if path.index(self.match) == idx - 1:
                for node in cycle:
                    if path[idx + 1] in node.neighbors:
                        cpath = node.cycle_aug_path(node.match, cycle)
                        return path[:idx] + cpath[::-1] + path[idx + 1 :]
                logger.error(
                    "Supernode (inner 1) not connected to rest of graph."
                )

            elif path.index(self.match) == idx + 1:
                for node in cycle:
                    if path[idx - 1] in node.neighbors:
                        cpath = node.cycle_aug_path(node.match, cycle)
                        return path[:idx] + cpath + path[idx + 1 :]
                logger.error(
                    "Supernode (inner 2) not connected to rest of graph."
                )

            else:
                logger.error(
                    "Supernode not matched correctly to rest of graph."
                )


class Graph(object):
    def __init__(self):
        self.nodes = None
        self.edges = None

    def compute_edges(self):
        self.edges = {}
        for key in self.nodes:
            for node in self.nodes[key].neighbors:
                self.edges[tuple(sorted([key, node.name]))] = 1

    def mark_edges(self, node1, node2):
        self.edges[tuple(sorted([node1.name, node2.name]))] = 0

    def clean_graph(self):
        for key in self.nodes:
            self.nodes[key].mark = False
            self.nodes[key].parent = None
            self.nodes[key].root = None

    def compute_size_matching(self):
        """Compute number of matched pairs"""
        size = 0
        for key in self.nodes:
            if self.nodes[key].match:
                size += 1
        assert size % 2 == 0
        return old_div(size, 2)

    def create_matching_dict(self):
        """Create dictionary of matched pairs"""
        matching_dict = {}
        for key in self.nodes:
            if self.nodes[key].match:
                matching_dict[key] = self.nodes[key].match.name
        return matching_dict

    def find_max_matching(self):
        """Wrapper function for computing maximum matching"""
        path = self.find_aug_path()
        if not path:
            return self
        else:
            self.aug_old_matching(path)
            return self.find_max_matching()

    def find_aug_path(self):
        """Edmonds algorithm for computing maximum matching"""
        self.clean_graph()
        self.compute_edges()

        exposed_node = [
            node for node in list(self.nodes.values()) if node.match is None
        ]
        for node in exposed_node:
            node.parent = node
            node.root = node

        for node in exposed_node:
            if not node.mark:
                for adj_node in node.neighbors:
                    if self.edges[tuple(sorted([node.name, adj_node.name]))]:
                        if adj_node not in exposed_node:
                            adj_node.parent = node
                            adj_node.root = node.root
                            adj_node.mark = True  # odd distance from root
                            self.mark_edges(node, adj_node)
                            exposed_node.append(adj_node)

                            adj_match = adj_node.match
                            adj_match.parent = adj_node
                            adj_match.root = adj_node.root
                            self.mark_edges(adj_node, adj_match)
                            exposed_node.append(adj_match)
                        else:
                            if not (len(adj_node.ancestor_path()) % 2):
                                self.mark_edges(node, adj_node)
                            else:
                                if node.root != adj_node.root:
                                    path1 = node.ancestor_path()
                                    path2 = adj_node.ancestor_path()
                                    return path1[::-1] + path2
                                else:
                                    return self.blossom(node, adj_node)
                node.mark = True

        return []

    def blossom(self, node1, node2):
        """Find augmenting path on blossom (cycle)"""
        path1 = node1.ancestor_path()
        path2 = node2.ancestor_path()
        cycle = path1[::-1] + path2[:-1]

        # Contract cycle nodes to supernode
        snode = Supernode(cycle)
        nodelist = snode.contract_nodelist(list(self.nodes.values()))
        self.nodes = {node.name: node for node in nodelist}
        self.compute_edges()
        aug_path = self.find_aug_path()

        # Expand supernode back to original cycle nodes
        aug_path = snode.expand_path(aug_path, cycle)
        nodelist = snode.expand_nodelist(list(self.nodes.values()))
        self.nodes = {node.name: node for node in nodelist}
        self.compute_edges()

        return aug_path

    @staticmethod
    def aug_old_matching(path):
        """Apply augmenting path to current matching on graph"""
        for idx, node in enumerate(path):
            if (idx + 1) % 2:
                node.match = path[idx + 1]
            else:
                node.match = path[idx - 1]
