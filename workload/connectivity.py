from abc import ABC, abstractmethod
from io import UnsupportedOperation

from workload.operations import Operation, AddEdge, RemoveEdge


class Connectivity(ABC):

    @abstractmethod
    def add_vertex(self, vertex: int):
        ...

    @abstractmethod
    def add_edge(self, u: int, v: int, e: int):
        ...

    @abstractmethod
    def remove_edge(self, e: int):
        ...

    @abstractmethod
    def start_temporary_changes(self):
        ...

    @abstractmethod
    def undo_temporary_changes(self):
        ...

    @abstractmethod
    def get_component_number(self, vertex: int) -> int:
        ...

    @abstractmethod
    def set_main_component_vertex(self, vertex: int):
        ...

    @abstractmethod
    def get_nb_connected_component(self) -> int:
        ...

    @abstractmethod
    def get_connected_component(self, vertex: int) -> set[int]:
        ...

    @abstractmethod
    def get_largest_component(self) -> set[int]:
        ...

    @abstractmethod
    def get_vertices_added_to_main_component(self) -> set[int]:
        ...

    @abstractmethod
    def get_edges_added_to_main_component(self) -> set[int]:
        ...

    @abstractmethod
    def get_vertices_removed_from_main_component(self) -> set[int]:
        ...

    @abstractmethod
    def get_edges_removed_from_main_component(self) -> set[int]:
        ...

    @abstractmethod
    def query(self, u: int, v: int) -> bool:
        ...

    @abstractmethod
    def compute_sum_of_distances(self) -> int:
        ...

class PartialConnectivity(Connectivity, ABC):

    def __init__(self):
        self.modifications: list[list[Operation]] = []

    def get_component_number(self, vertex: int) -> int:
        return -1

    def set_main_component_vertex(self, vertex: int):
        pass

    def get_nb_connected_component(self) -> int:
        return -1

    def get_connected_component(self, vertex: int) -> set[int]:
        return set()

    def get_largest_component(self) -> set[int]:
        return set()

    def get_vertices_added_to_main_component(self) -> set[int]:
        return set()

    def get_edges_added_to_main_component(self) -> set[int]:
        return set()

    def get_vertices_removed_from_main_component(self) -> set[int]:
        return set()

    def get_edges_removed_from_main_component(self) -> set[int]:
        return set()

    def start_temporary_changes(self):
        self.modifications.append([])

    def undo_temporary_changes(self):
        last = self.modifications.pop()

        if last is not None:
            for op in reversed(last):
                op.execute(self)

    def on_add_vertex(self, _vertex: int):
        last = peek_stack(self.modifications)
        if last is not None:
            raise UnsupportedOperation("Undo add vertex isn't possible")

    def on_add_edge(self, _u: int, _v: int, e: int):
        last = peek_stack(self.modifications)
        if last is not None:
            last.append(RemoveEdge(e)) # reverse operation

    def on_remove_edge(self, u: int, v: int, e: int):
        last = peek_stack(self.modifications)
        if last is not None:
            last.append(AddEdge(u, v, e)) # reverse operation

def peek_stack(stack: list[list]) -> list | None:
    if stack:
        return stack[-1]
    else:
        return None
