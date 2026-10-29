import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from workload.connectivity import Connectivity
from workload.dtree_connectivity import DTreeConnectivity
from workload.dtree_opt_connectivity import OptDTreeConnectivity
from workload.operations import read_workload, Workload, Operations


def run(output_folder: Path, operations: Operations, connectivity: Connectivity):
    conn_name = connectivity.__class__.__name__
    print("Using", conn_name)

    output = output_folder.joinpath(conn_name).joinpath(operations.file)
    print("Writing output at", output)

    if output.parent is not None:
        output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, mode="x", encoding="utf-8") as f:
        last_time = time.time()
        for i, op in enumerate(operations):
            start = time.perf_counter_ns()
            op.execute(connectivity)
            nanos = time.perf_counter_ns() - start

            f.write("{i} {op} {nanos} {sd}\n".format(i=i + 1, op=op.short_name(), nanos=nanos,
                                                     sd=connectivity.compute_sum_of_distances()))

            if time.time() - last_time > 8:
                print(i)
                last_time = time.time()


def run_operation(args):
    folder, op, connectivity_type = args
    run(folder, op, connectivity_type())


if __name__ == '__main__':
    output_folder = Path("../powsybl/powsybl-open-loadflow/sum_of_distances/data/")

    workloads = [
        read_workload(Path("../powsybl/powsybl-open-loadflow/workload/spy_5541_1_1_2026-07-03T12:31:54.685462530Z.txt"))
    ]
    connectivities = [
        OptDTreeConnectivity
    ]

    for workload in workloads:
        print("Running workload at", workload.file)

        for connectivity in connectivities:
            folder = output_folder.joinpath(workload.file.name)

            if len(workload.operations) >= 2:
                with ProcessPoolExecutor(8) as executor:
                    executor.map(
                        run_operation,
                        [
                            (folder, op, connectivity)
                            for op in workload.operations
                        ],
                    )
            else:
                for op in workload.operations:
                    run(folder, op, connectivity())
