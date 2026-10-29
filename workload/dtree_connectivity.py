from typing import Tuple

from Dtree import Dtree_utils
from Dtree.DTNode import DTNode
from utils.tree_utils import order
from workload.connectivity import PartialConnectivity


class DTreeConnectivity(PartialConnectivity):
    def __init__(self):
        super().__init__()
        self.nodes: dict[int, DTNode] = {}
        self.edges: dict[int, Tuple[int, int]] = {}
        # associate to each pair of ordered vertices, the number of edges between them (multi-edge support)
        self.graph: dict[Tuple[int, int], int] = {}

    def add_vertex(self, vertex: int):
        if vertex not in self.nodes:
            self.nodes[vertex] = DTNode(vertex)
            self.on_add_vertex(vertex)

    def add_edge(self, u: int, v: int, e: int):
        if e in self.edges:
            return # the edge already exists

        u, v = order(u, v)

        if (u, v) in self.graph:
            # an edge between these vertices already exist, don't modify spanning tree

            self.graph[(u, v)] += 1
        else:
            # modify spanning trees
            root_u, distance_u = Dtree_utils.find_root(self.nodes[u])
            root_v, distance_v = Dtree_utils.find_root(self.nodes[v])

            if root_u.val != root_v.val:
                Dtree_utils.insert_te(self.nodes[u], self.nodes[v], root_u, root_v)
            else:
                Dtree_utils.insert_nte(root_u, self.nodes[u], distance_u, self.nodes[v], distance_v)

            self.graph[(u, v)] = 1

        self.edges[e] = (u, v)
        self.on_add_edge(u, v, e)

    def remove_edge(self, e: int):
        # remove the edge only if it exists
        if e not in self.edges:
            return
        u, v = self.edges.pop(e)

        if self.graph[(u, v)] == 1:
            del self.graph[(u, v)]

            # update spanning trees only if there is no more edges between u and v
            if self.nodes[u] in self.nodes[v].nte or self.nodes[v] in self.nodes[u].nte:
                Dtree_utils.delete_nte(self.nodes[u], self.nodes[v])
            else:
                Dtree_utils.delete_te(self.nodes[u], self.nodes[v])
        else:
            self.graph[(u, v)] -= 1

        self.on_remove_edge(u, v, e)

    def query(self, u: int, v: int) -> bool:
        return Dtree_utils.query(self.nodes[u], self.nodes[v])

    def compute_sum_of_distances(self) -> int:
        sum = 0

        for node in self.nodes.values():
            sum += Dtree_utils.toRoot(node)

        return sum
