import itertools
import time
from itertools import count

from Dtree import Dtree_utils
from Dtree.DTNode import DTNode
from utils.tree_utils import constructST_adjacency_list
from workload.dtree_connectivity import DTreeConnectivity


if __name__ == '__main__':
    dtree = DTreeConnectivity()

    for i in range(0, 8):
        dtree.add_vertex(i)
    dtree.add_edge(7, 7, "7-7")
    dtree.add_edge(0, 0, "0-0")
    dtree.add_edge(6, 4, "6-4")
    dtree.add_edge(0, 3, "0-3")
    dtree.add_edge(7, 3, "7-3")
    dtree.add_edge(4, 5, "4-5")
    dtree.add_edge(1, 4, "1-4")
    dtree.add_edge(2, 7, "2-7")
    dtree.add_edge(3, 6, "3-6")
    dtree.add_edge(2, 3, "2-3")
    dtree.add_edge(2, 6, "2-6")
    dtree.add_edge(5, 1, "5-1")
    dtree.add_edge(4, 2, "4-2")
    dtree.add_edge(1, 1, "1-1")
    dtree.add_edge(6, 5, "6-5")
    dtree.add_edge(0, 5, "0-5")

    dtree.remove_edge("2-6")
    dtree.remove_edge("4-2")
    dtree.remove_edge("3-6")
    dtree.remove_edge("0-3")

    print(dtree.query(1, 4))
    print(dtree.query(1, 4))
