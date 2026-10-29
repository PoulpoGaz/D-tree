from typing import Tuple

from Dtree import Dtree_utils
from Dtree.DTNode import DTNode
from utils import graph_utils
from utils.tree_utils import order
from workload.connectivity import PartialConnectivity


class OptDTreeConnectivity(PartialConnectivity):
    def __init__(self):
        super().__init__()
        self.nodes: dict[int, DTNode] = {}
        # associate to an edge the two endpoints
        self.edges: dict[int, Tuple[int, int]] = {}
        # associate to each pair of ordered vertices, the number of edges between them (multi-edge support)
        self.multi_edges: dict[Tuple[int, int], int] = {}
        self.adjacency_list: dict[int, set[int]] = {}

    def add_vertex(self, vertex: int):
        if vertex not in self.nodes:
            self.nodes[vertex] = DTNode(vertex)
            self.adjacency_list[vertex] = set()
            self.on_add_vertex(vertex)

    def add_edge(self, u: int, v: int, e: int):
        if e in self.edges:
            return # the edge already exists

        u, v = order(u, v)

        if (u, v) in self.multi_edges:
            # an edge between these vertices already exist, don't modify spanning tree

            self.multi_edges[(u, v)] += 1
        else:
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)

            # modify spanning trees
            root_u, distance_u = Dtree_utils.find_root(self.nodes[u])
            root_v, distance_v = Dtree_utils.find_root(self.nodes[v])

            if root_u.val != root_v.val:
                Dtree_utils.insert_te_simple(self.nodes[u], self.nodes[v], root_u, root_v)
                target = graph_utils.best_BFS(self.adjacency_list, len(self.nodes), u)  # find the root of best BFS-tree
                Dtree_utils.reconstruct_BFS_tree(self.nodes[target], self.nodes, set()) # reconstruct the opt
            else:
                target = graph_utils.best_BFS(self.adjacency_list, len(self.nodes), u)  # find the root of best BFS-tree
                Dtree_utils.reconstruct_BFS_tree(self.nodes[target], self.nodes, set()) # reconstruct the opt
                self.nodes[u].nte.add(self.nodes[u])
                self.nodes[v].nte.add(self.nodes[v])

            self.multi_edges[(u, v)] = 1

        self.edges[e] = (u, v)
        self.on_add_edge(u, v, e)

    def remove_edge(self, e: int):
        # remove the edge only if it exists
        if e not in self.edges:
            return
        u, v = self.edges.pop(e)

        if self.multi_edges[(u, v)] == 1:
            del self.multi_edges[(u, v)]
            self.adjacency_list[u].remove(v)
            self.adjacency_list[v].remove(u)

            # update spanning trees only if there is no more edges between u and v
            if self.nodes[u] in self.nodes[v].nte or self.nodes[v] in self.nodes[u].nte:
                Dtree_utils.delete_nte(self.nodes[u], self.nodes[v])
                target = graph_utils.best_BFS(self.adjacency_list, len(self.nodes), u)  # find the root of best BFS-tree
                Dtree_utils.reconstruct_BFS_tree(self.nodes[target], self.nodes, set())  # reconstruct the opt
            else:
                res = Dtree_utils.delete_te(self.nodes[u], self.nodes[v])
                if type(res) is tuple:  # delete tree edge (a, b) splits a spanning tree
                    target_u = graph_utils.best_BFS(self.adjacency_list, len(self.nodes), u)  # find root of the best BFS-tree contains a
                    target_v = graph_utils.best_BFS(self.adjacency_list, len(self.nodes), v)  # find root of the best BFS-tree contain b
                    Dtree_utils.reconstruct_BFS_tree(self.nodes[target_u], self.nodes, set())  # reconstruct the opt
                    Dtree_utils.reconstruct_BFS_tree(self.nodes[target_v], self.nodes, set())  # reconstruct the opt
                else:
                    target = graph_utils.best_BFS(self.adjacency_list, len(self.nodes), u)  # find the root of best BFS-tree
                    Dtree_utils.reconstruct_BFS_tree(self.nodes[target], self.nodes, set())  # reconstruct the opt

        else:
            self.multi_edges[(u, v)] -= 1

        self.on_remove_edge(u, v, e)

    def query(self, u: int, v: int) -> bool:
        pass

    def compute_sum_of_distances(self) -> int:
        sum = 0

        for node in self.nodes.values():
            sum += Dtree_utils.toRoot(node)

        return sum
