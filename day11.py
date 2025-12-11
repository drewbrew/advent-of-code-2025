import multiprocessing
from pathlib import Path

import networkx

TEST_INPUT = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

PART_TWO_TEST_INPUT = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


def part_one(puzzle: str) -> int:
    """How many paths from you to out?"""

    graph = networkx.DiGraph()
    for line in puzzle.splitlines():
        source, dests = line.split(": ")
        for dest in dests.split():
            graph.add_edge(source, dest)
    return sum(1 for _ in networkx.all_simple_paths(graph, "you", "out"))


def paths_from_a_to_b_excluding_c(graph: networkx.DiGraph, source: str, dest: str, excluded_node: str) -> int:
    result = 0
    for path in networkx.all_simple_paths(graph, source, dest):
        if excluded_node not in path:
            result += 1
    print(f'from {source} to {dest} excluding {excluded_node} = {result}')
    return result


def part_two(puzzle: str) -> int:
    """How many paths from you to out?"""

    graph = networkx.DiGraph()
    for line in puzzle.splitlines():
        source, dests = line.split(": ")
        for dest in dests.split():
            graph.add_edge(source, dest)
    # need to look at:
    # svr -> fft (without hitting dac) -> dac -> out
    # svr -> dac (without hitting fft) -> dac -> out
    result = 0
    svr_paths_to_fft = svr_paths_to_dac = dac_paths_to_fft = fft_paths_to_dac = (
        fft_paths_to_out
    ) = dac_paths_to_out = 0
    args_list = [
        (graph, 'svr', 'dac', 'fft'),
        (graph, 'svr', 'fft', 'dac'),
        (graph, 'dac', 'fft', 'out'),
        (graph, 'fft', 'dac', 'out'),
        (graph, 'dac', 'out', 'fft'),
        (graph, 'fft', 'out', 'dac'),
    ]
    with multiprocessing.Pool() as pool:
        (svr_paths_to_dac, svr_paths_to_fft, dac_paths_to_fft, fft_paths_to_dac, dac_paths_to_out, fft_paths_to_out) = pool.starmap(
            paths_from_a_to_b_excluding_c, args_list
        )
    result = (svr_paths_to_dac * dac_paths_to_fft * fft_paths_to_out) + (
        svr_paths_to_fft * fft_paths_to_dac * dac_paths_to_out
    )
    return result


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 5, part_one_result
    puzzle = Path("day11.txt").read_text()
    print(part_one(puzzle=puzzle))
    part_two_result = part_two(PART_TWO_TEST_INPUT)
    assert part_two_result == 2, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
