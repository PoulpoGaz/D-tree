from abc import ABC, abstractmethod
from dataclasses import dataclass
from io import TextIOWrapper
from pathlib import Path
from typing import Tuple
from zipfile import ZipFile

from pip._internal import operations


@dataclass
class Operation(ABC):
    @abstractmethod
    def execute(self, connectivity):
        ...

    @abstractmethod
    def short_name(self) -> str:
        ...


@dataclass
class AddVertex(Operation):
    vertex: int

    def execute(self, connectivity):
        connectivity.add_vertex(self.vertex)

    def short_name(self) -> str:
        return "v"

@dataclass
class AddEdge(Operation):
    u: int
    v: int
    e: int

    def execute(self, connectivity):
        connectivity.add_edge(self.u, self.v, self.e)

    def short_name(self) -> str:
        return "e"

@dataclass
class RemoveEdge(Operation):
    e: int

    def execute(self, connectivity):
        connectivity.remove_edge(self.e)

    def short_name(self) -> str:
        return "rm"


@dataclass
class StartTemporaryChanges(Operation):
    quick: bool

    def execute(self, connectivity):
        connectivity.start_temporary_changes()

    def short_name(self) -> str:
        return "start"

@dataclass
class UndoTemporaryChanges(Operation):
    def execute(self, connectivity):
        connectivity.undo_temporary_changes()

    def short_name(self) -> str:
        return "undo"

@dataclass
class GetNum(Operation):
    vertex: int

    def execute(self, connectivity):
        connectivity.get_component_number(self.vertex)

    def short_name(self) -> str:
        return "get_num"


@dataclass
class SetMain(Operation):
    vertex: int

    def execute(self, connectivity):
        connectivity.set_main_component_vertex(self.vertex)

    def short_name(self) -> str:
        return "set_main"

@dataclass
class Count(Operation):

    def execute(self, connectivity):
        connectivity.get_nb_connected_component()

    def short_name(self) -> str:
        return "count"

@dataclass
class GetComponent(Operation):
    vertex: int

    def execute(self, connectivity):
        connectivity.get_connected_component(self.vertex)

    def short_name(self) -> str:
        return "get_comp"

@dataclass
class GetLargestComponent(Operation):
    def execute(self, connectivity):
        connectivity.get_largest_component()

    def short_name(self) -> str:
        return "largest"

@dataclass
class GetVerticesAdded(Operation):
    def execute(self, connectivity):
        connectivity.get_vertices_added_to_main_component()

    def short_name(self) -> str:
        return "v_added"

@dataclass
class GetEdgesAdded(Operation):
    def execute(self, connectivity):
        connectivity.get_edges_added_to_main_component()

    def short_name(self) -> str:
        return "e_added"

@dataclass
class GetVerticesRemoved(Operation):
    def execute(self, connectivity):
        connectivity.get_vertices_removed_from_main_component()

    def short_name(self) -> str:
        return "v_removed"

@dataclass
class GetEdgesRemoved(Operation):
    def execute(self, connectivity):
        connectivity.get_edges_removed_from_main_component()

    def short_name(self) -> str:
        return "e_added"

@dataclass
class Query(Operation):
    u: int
    v: int

    def execute(self, connectivity):
        connectivity.query(self.u, self.v)

    def short_name(self) -> str:
        return "q"

@dataclass
class TestPoint(Operation):
    size: int
    seed: int

    def execute(self, connectivity):
        pass

    def short_name(self) -> str:
        return "testpoint"

@dataclass
class Sd(Operation):
    pass

    def execute(self, connectivity):
        connectivity.compute_sum_of_distances()

    def short_name(self) -> str:
        return "Sd"

@dataclass
class New(Operation):
    pass

    def execute(self, connectivity):
        pass

    def short_name(self) -> str:
        return "new"


def parse_operation(line: str) -> Operation | None:
    parts = line.split(" ")

    match parts[0]:
        case "v":
            return AddVertex(int(parts[1]))
        case "e":
            return AddEdge(int(parts[1]), int(parts[2]), int(parts[3]))
        case "rm":
            return RemoveEdge(int(parts[1]))
        case "start":
            return StartTemporaryChanges(parts[1].lower() == "true")
        case "undo":
            return UndoTemporaryChanges()
        case "get_num":
            return GetNum(int(parts[1]))
        case "set_main":
            return SetMain(int(parts[1]))
        case "count":
            return Count()
        case "get_comp":
            return GetComponent(int(parts[1]))
        case "largest":
            return GetLargestComponent()
        case "v_added":
            return GetVerticesAdded()
        case "e_added":
            return GetEdgesAdded()
        case "v_removed":
            return GetVerticesRemoved()
        case "e_removed":
            return GetEdgesRemoved()
        case "q":
            return Query(int(parts[1]), int(parts[2]))
        case "testpoint":
            return TestPoint(int(parts[1]), int(parts[2]))
        case "Sd":
            return Sd()
        case "new":
            return New()
        case _:
            return None

@dataclass
class Operations:
    file: str
    operations: list[Operation]

    def __iter__(self):
        return self.operations.__iter__()

@dataclass
class Workload:
    file: Path
    operations: list[Operations]

def read_operations(file: str, lines) -> Operations:
    operations = []

    for line in lines:
        operation = parse_operation(line.strip())
        if operation is not None:
            operations.append(operation)

    return Operations(file, operations)

def read_workload(file: Path) -> Workload:
    if file.name.endswith(".zip"):
        with ZipFile(file) as zip_file:
            operations = []
            for op_file in zip_file.namelist():
                with zip_file.open(op_file) as f:
                    operations.append(read_operations(op_file, TextIOWrapper(f, encoding="utf-8")))

            return Workload(file, operations)
    else:
        with file.open(mode='r', encoding='utf-8') as f:
            return Workload(file, [read_operations(file.name, f)])
