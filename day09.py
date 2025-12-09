"""Day 9: movie theater tile decorations"""

from functools import partial
from itertools import combinations
from multiprocessing import Pool
from pathlib import Path
from typing import Iterable

from matplotlib.patches import Polygon as mpl_polygon
from matplotlib import pyplot as plt

from shapely.geometry import Polygon, box


TEST_INPUT = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


def area(point1: tuple[int, int], point2: tuple[int, int]) -> int:
    x1, y1 = point1
    x2, y2 = point2
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    return (x2 - x1 + 1) * (y2 - y1 + 1)


def part_one(puzzle: str) -> int:
    lines = [line.split(",") for line in puzzle.splitlines()]
    nodes = [(int(x), int(y)) for x, y in lines]
    return part_one_internal(nodes)


def part_one_internal(nodes: Iterable[tuple[int, int]]) -> int:
    max_area = 0
    for p1, p2 in combinations(nodes, 2):
        max_area = max(max_area, area(p1, p2))
    return max_area


def draw_polygon(nodes: tuple[int, int], name: str) -> None:
    polygon = mpl_polygon(nodes, closed=True, facecolor="white", edgecolor="red")
    fig, ax = plt.subplots()
    ax.add_patch(polygon)
    min_x, *_, max_x = sorted(x for x, _ in nodes)
    min_y, *_, max_y = sorted(y for _, y in nodes)
    ax.set_xlim(min_x - 100, max_x + 100)
    ax.set_ylim(min_y - 100, max_y + 100)
    plt.savefig(name)


def check_rectangle(p1: tuple[int, int], p2: tuple[int, int], polygon: Polygon) -> int:
    x1, y1 = p1
    x2, y2 = p2

    rectangle = box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

    if polygon.contains(rectangle):
        return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
    return 0


def part_two(puzzle: str) -> int:
    lines = [line.split(",") for line in puzzle.splitlines()]
    nodes = [(int(x), int(y)) for x, y in lines]
    polygon = Polygon(nodes)

    with Pool() as pool:
        func = partial(check_rectangle, polygon=polygon)
        areas = pool.starmap(
            func,
            combinations(nodes, 2),
        )

    return max(areas)


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 50, part_one_result
    puzzle = Path("day09.txt").read_text()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 24, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
