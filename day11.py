from itertools import cycle
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


# SVG color scheme with white-ish and hard-to-see colors removed
COLORS = """aqua	aquamarine	azure
bisque	black	blue
blueviolet	brown	burlywood	cadetblue	chartreuse
chocolate	coral	cornflowerblue	crimson
cyan	darkblue	darkcyan	darkgoldenrod
darkgreen	darkgrey	darkkhaki	darkmagenta	darkolivegreen
darkorange	darkorchid	darkred	darksalmon	darkseagreen
darkslateblue	darkslategrey	darkturquoise	darkviolet
deeppink	deepskyblue	dimgrey	dodgerblue
firebrick	forestgreen	fuchsia
gold	goldenrod	grey
green	greenyellow	honeydew	hotpink	indianred
indigo	ivory	khaki	lavender
lawngreen	lightblue	lightcoral	lightcyan
lightgreen	lightgrey	lightpink
lightsalmon	lightseagreen	lightskyblue	lightslategrey
lightsteelblue	lime	limegreen
magenta	maroon	mediumaquamarine	mediumblue	mediumorchid
mediumpurple	mediumseagreen	mediumslateblue	mediumspringgreen	mediumturquoise
mediumvioletred	midnightblue	mintcream	mistyrose	moccasin
navy	oldlace	olive	olivedrab
orange	orangered	orchid	palegoldenrod	palegreen
paleturquoise	palevioletred	papayawhip	peachpuff	peru
pink	plum	powderblue	purple	red
rosybrown	royalblue	saddlebrown	salmon	sandybrown
seagreen	sienna	silver	skyblue
slateblue	slategrey	springgreen
steelblue	tan	teal	thistle	tomato
turquoise	violet	wheat   yellow	yellowgreen""".split()


def part_one(puzzle: str) -> int:
    """How many paths from you to out?"""

    graph = networkx.DiGraph()
    for line in puzzle.splitlines():
        source, dests = line.split(": ")
        for dest in dests.split():
            graph.add_edge(source, dest)
    return sum(1 for _ in networkx.all_simple_paths(graph, "you", "out"))


def paths_from_a_to_b(
    source: str,
    dest: str,
    cache: dict[tuple[str, str], int],
    children: dict[str, list[str]],
) -> int:
    # time for some recursion!
    try:
        result = cache[source, dest]
    except KeyError:
        try:
            result = sum(
                paths_from_a_to_b(node2, dest, cache, children) if dest != node2 else 1
                for node2 in children[source]
            )
        except KeyError:
            # we got to out but weren't looking for it
            result = 0

        cache[source, dest] = result

    # if source in ['svr', 'dac', 'fft']:
    #     print(f'{source} -> {dest} = {result}')
    return result


def graph_to_dot(graph: networkx.DiGraph) -> str:
    output = [
        "digraph {",
        "    node [colorscheme=svg]",
        '    fft [color="red",shape=box,style=filled]',
        '    dac [color="blue",shape=box,style=filled]',
        '    you [color="green",style=filled]',
    ]
    colors = cycle(COLORS)
    for node1, node2 in graph.edges:
        output.append(f'    {node1} -> {node2} [color="{next(colors)}"]')
    output.append("}")
    return "\n".join(output)


def part_two(puzzle: str) -> int:
    """How many paths from svr to out that go through both dac and fft?"""
    children = {}
    visualize = puzzle != PART_TWO_TEST_INPUT
    if visualize:
        graph = networkx.DiGraph()
    for line in puzzle.splitlines():
        source, dests = line.split(": ")
        if visualize:
            for dest in dests.split():
                graph.add_edge(source, dest)
        children[source] = dests.split()
    if visualize:
        dotfile = "day11.dot"
        Path(dotfile).write_text(graph_to_dot(graph))
        try:
            output = subprocess.run(["dot", "-Tsvg", dotfile], capture_output=True)
        except FileNotFoundError:
            print("Unable to write svg. Install graphviz and try again")
        else:
            assert not output.stderr, output.stderr
            Path("day11.svg").write_bytes(output.stdout)
            print("take a look at day11.svg")
            print("if fft (red) is below dac (blue), everything here will break")

    # need to look at:
    # svr -> fft (without hitting dac) -> dac -> out (possible)
    # svr -> dac (without hitting fft) -> fft -> out (impossible)
    result = 0
    svr_paths_to_fft = fft_paths_to_dac = dac_paths_to_out = 0
    manager = multiprocessing.Manager()
    cache = manager.dict()
    args_list = [
        ("svr", "fft", cache, children),
        ("fft", "dac", cache, children),
        ("dac", "out", cache, children),
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
