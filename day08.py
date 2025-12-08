from math import sqrt, prod
from pathlib import Path
from typing import Iterable

import networkx

TEST_INPUT = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


def cartesian_distance(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> float:
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def nearest_neighbor(
    point: tuple[int, int, int],
    nodes: Iterable[tuple[int, int, int]],
    graph: networkx.Graph,
) -> tuple[tuple[int, int, int], float]:
    x, y, z = point
    min_dist = 1_000_000_000_000
    x2 = y2 = z2 = -1
    # print(f"{point} is connected to {already_connected_node}")
    for x1, y1, z1 in nodes:
        if x1 == x and y1 == y and z1 == z or graph.has_edge((x1, y1, z1), (x, y, z)):
            continue
        if (dist := cartesian_distance(x, y, z, x1, y1, z1)) < min_dist:
            min_dist = dist
            x2 = x1
            y2 = y1
            z2 = z1
    assert x2 != -1
    # print(f'{point} is closest to {x2, y2, z2} ({min_dist})')
    return (x2, y2, z2), min_dist


def part_one_result(graph: networkx.graph) -> int:
    networks = []
    nodes_seen = set()
    for node in graph.nodes:
        if node in nodes_seen:
            continue
        nodes_seen.add(node)
        neighbors = set(networkx.descendants(graph, node))
        nodes_seen |= neighbors
        networks.append(len(neighbors) + 1)
    networks.sort(reverse=True)
    # print(networks)
    return prod(networks[:3])


def run_puzzle(puzzle: str, part_one_connections: int = 10) -> tuple[int, int]:
    nodes = {tuple(int(i) for i in line.split(",")) for line in puzzle.splitlines()}
    graph = networkx.Graph()
    unconnected_nodes = {node: nearest_neighbor(node, nodes, graph) for node in nodes}
    # pick the node farthest away from everyone else for speed (saves about a second)
    a_node = sorted(unconnected_nodes.items(), key=lambda k: k[1][1], reverse=True)[0][0]
    node_count = len(nodes)
    part_one_final = -1
    while a_node not in graph.nodes or (
        len(networkx.descendants(graph, a_node)) + 1 < node_count
    ):
        if len(graph.edges) == part_one_connections:
            part_one_final = part_one_result(graph)
        for node, (neighbor, dist) in sorted(
            unconnected_nodes.items(), key=lambda item: item[1][1]
        ):
            if graph.has_edge(node, neighbor):
                continue
            # print(
            #     f"connecting {node} to {neighbor} (distance {dist:.2f}), {len(graph.edges)}"
            # )
            graph.add_edge(node, neighbor)
            unconnected_nodes[node] = nearest_neighbor(node, nodes, graph)
            unconnected_nodes[neighbor] = nearest_neighbor(neighbor, nodes, graph)
            break
    # print("done", node, neighbor)
    return part_one_final, node[0] * neighbor[0]


def main():
    part_one_result, part_two_result = run_puzzle(TEST_INPUT, 10)
    assert part_one_result == 40, part_one_result
    assert part_two_result == 25272, part_two_result
    puzzle = Path("day08.txt").read_text()
    part_one_result, part_two_result = run_puzzle(puzzle, 1000)
    print(part_one_result)
    print(part_two_result)


if __name__ == "__main__":
    main()
