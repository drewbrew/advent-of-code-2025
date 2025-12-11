import multiprocessing
from pathlib import Path
import subprocess

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


def paths_from_a_to_b(
    graph: networkx.DiGraph, source: str, dest: str, cache: dict[tuple[str, str], int],
) -> int:
    # time for some recursion!
    # print(f'{source=}, {dest=}')
    if source == dest:
        # print('end')
        return 1
    try:
        result = cache[source, dest]
    except KeyError:

        result = sum(
            paths_from_a_to_b(graph, node2, dest, cache)
            for node1, node2 in graph.edges
            if node1 == source
        )
        cache[source, dest] = result

    # if source in ['svr', 'dac', 'fft']:
    #     print(f'{source} -> {dest} = {result}')
    return result


def graph_to_dot(graph: networkx.Graph) -> str:
    output = ["graph {"]
    for node1, node2 in graph.edges:
        output.append(f"    {node1} -- {node2}")
    output.append("}")
    return "\n".join(output)


def part_two(puzzle: str) -> int:
    """How many paths from you to out?"""

    graph = networkx.DiGraph()
    for line in puzzle.splitlines():
        source, dests = line.split(": ")
        for dest in dests.split():
            graph.add_edge(source, dest)
    if puzzle != PART_TWO_TEST_INPUT:
        dotfile = "day11.dot"
        Path(dotfile).write_text(graph_to_dot(graph))
        try:
            output = subprocess.run(["dot", "-Tsvg", "day11.dot"], capture_output=True)
        except FileNotFoundError:
            print("Unable to write svg. Install graphviz and try again")
        else:
            assert not output.stderr, output.stderr
            Path("day11.svg").write_bytes(output.stdout)
            print("take a look at day11.svg")
            print("if fft is below dac, everything here will break")

    # need to look at:
    # svr -> fft (without hitting dac) -> dac -> out (possible)
    # svr -> dac (without hitting fft) -> fft -> out (impossible)
    result = 0
    svr_paths_to_fft = fft_paths_to_dac = dac_paths_to_out = 0
    manager = multiprocessing.Manager()
    cache = manager.dict()
    args_list = [
        (graph, "svr", "fft", cache),
        (graph, "fft", "dac", cache),
        (graph, "dac", "out", cache),
    ]
    with multiprocessing.Pool() as pool:
        (
            svr_paths_to_fft,
            fft_paths_to_dac,
            dac_paths_to_out,
        ) = pool.starmap(paths_from_a_to_b, args_list)
    result = svr_paths_to_fft * fft_paths_to_dac * dac_paths_to_out

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
