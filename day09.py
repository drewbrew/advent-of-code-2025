"""Day 9: movie theater tile decorations"""
from functools import partial
from itertools import combinations
from multiprocessing import Manager, Pool
from pathlib import Path


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
    max_area = 0
    for p1, p2 in combinations(nodes, 2):
        max_area = max(max_area, area(p1, p2))
    return max_area


def valid_y_values(
    x: int,
    perimeter: frozenset[tuple[int, int]],
    cache: dict[int, frozenset[tuple[int, int]]],
) -> frozenset[tuple[int, int]]:
    try:
        return cache[x]
    except KeyError:
        pass
    y_values = sorted(y1 for (x1, y1) in perimeter if x1 == x)
    max_y = y_values[-1]
    result = []
    y = y_values[0]
    y_set = set(y_values)
    # iterate from top to bottom
    # we know we're starting at a wall
    # if our next spot is a wall, we keep going until we hit empty space, then another wall,
    # then the first empty space after that is where we stop
    # if our next spot is not a wall, we keep going until we hit another wall, then the first
    # empty space after that is where we stop

    y_start = y
    hit_first_empty = False
    hit_next_wall = False
    hit_first_wall = True
    while y <= max_y:
        y += 1
        if y not in y_set:
            if not hit_first_wall:
                continue
            if not hit_first_empty:
                hit_first_empty = True
            if hit_next_wall:
                # stop point
                # save where we _just_ were
                result.append((y_start, y - 1))
                # and reset
                hit_next_wall = hit_first_wall = hit_first_empty = False
                y_start = y - 1
                continue
        else:
            if not hit_first_wall:
                hit_first_wall = True
            elif hit_first_empty:
                hit_next_wall = True
    cache[x] = frozenset(result)
    return frozenset(result)


def is_inside_perimeter(
    x: int,
    y: int,
    perimeter: frozenset[tuple[int, int]],
    cache: dict[int, frozenset[tuple[int, int]]],
) -> bool:
    # look up and down
    if (x, y) in perimeter:
        return True
    y_values = valid_y_values(x, perimeter, cache)
    for start, end in y_values:
        if y >= start and y <= end:
            return True

    return False


def is_valid_rectangle(
    point1: tuple[int, int],
    point2: tuple[int, int],
    perimeter: frozenset[tuple[int, int]],
    cache: dict[int, frozenset[tuple[int, int]]],
) -> bool:
    x1, y1 = point1
    x2, y2 = point2
    x_low, x_high = sorted([x1, x2])
    y_low, y_high = sorted([y1, y2])
    print(f"is valid? {point1=} {point2=}")
    if int := perimeter.intersection(
        (x, y) for x in range(x_low + 1, x_high) for y in range(y_low + 1, y_high)
    ):
        print(f"intersection between {point1} and {point2}!")
        for xa, ya in int:
            for xb, yb in [
                [xa + 1, ya],
                [xa - 1, ya],
                [xa, ya + 1],
                [xa, ya - 1],
            ]:
                if (
                    xb < x_low
                    or xb > x_high
                    or yb < y_low
                    or yb > y_high
                    or (xb, yb) in perimeter
                ):
                    continue
                if not is_inside_perimeter(xb, yb, perimeter, cache):
                    print(f"womp, {xb, yb} makes {point1} and {point2} fail")
                    return False
    else:
        # no spots in between!
        # just check the perimeter of the rectangle itself
        points = {point1, point2}
        print(f"no intermediate spots beween {point1} and {point2}")
        for x in range(x_low + 1, x_high):

            if (x, y_low) not in points and not is_inside_perimeter(
                x,
                y_low,
                perimeter,
                cache,
            ):
                print(f"upper boundary fails {point1} and {point2} at {x, y_low}")
                return False
            if (x, y_high) not in points and not is_inside_perimeter(
                x,
                y_high,
                perimeter,
                cache,
            ):
                print(f"lower boundary fails {point1} and {point2} at {x, y_high}")
                return False
        for y in range(y_low + 1, y_high):
            if (x_low, y) not in points and not is_inside_perimeter(
                x_low,
                y,
                perimeter,
                cache,
            ):
                print(f"left boundary fails {point1} and {point2} at {x_low, y}")
                return False
            if (x_high, y) not in points and not is_inside_perimeter(
                x_high,
                y,
                perimeter,
                cache,
            ):
                print(f"right boundary fails {point1} and {point2} at {x_high, y}")
                return False
        print(f"*** no spots between {point1} and {point2}, yay")
        return True
    return True


def part_two(puzzle: str) -> int:
    lines = [line.split(",") for line in puzzle.splitlines()]
    nodes = tuple((int(x), int(y)) for x, y in lines)
    perimeter = frozenset(generate_perimeter(nodes))
    # print(f"{sorted(perimeter)=}")
    manager = Manager()
    cache = manager.dict()
    # use a minimum value to speed things up
    # my answer for part 1 was on the order of 4.7 trillion, so
    # 200 million seems like a reasonable floor
    smallest_area = manager.list([-1 if puzzle == TEST_INPUT else 200_000_000])
    func = partial(
        generate_area,
        perimeter=perimeter,
        cache=cache,
        smallest_area =smallest_area
    )
    with Pool() as executor:
        areas = executor.map(func, combinations(nodes, 2), chunksize=100)
    return max(areas)


def generate_area(
    points: tuple[tuple[int, int], tuple[int, int]],
    perimeter: frozenset[tuple[int, int]],
    cache: dict[int, tuple[frozenset[tuple[int, int]]]],
    smallest_area: list[int],
) -> int:
    point1, point2 = points
    if area(point1, point2) < smallest_area[0]:
        print(f"too small between {point1} and {point2} (smallest area {smallest_area[0]})")
        return -1
    if is_valid_rectangle(point1, point2, perimeter, cache):
        area_used = area(point1, point2)
        print(f"/// found area from {point1} to {point2}: {area_used}")
        smallest_area[0] = max(smallest_area[0], area_used)
        return area_used
    return -1


def generate_perimeter(nodes: tuple[tuple[int, int]]) -> set[tuple[int, int]]:

    raw_perimeter = nodes + (nodes[0],)
    perimeter = set()
    for (x1, y1), (x2, y2) in zip(raw_perimeter[:-1], raw_perimeter[1:]):
        if x1 == x2:
            # going up or down
            direction = 1 if y1 < y2 else -1
            perimeter |= {(x1, y) for y in range(y1, y2 + direction, direction)}
        else:
            # going left or right
            direction = 1 if x1 < x2 else -1
            perimeter |= {(x, y2) for x in range(x1, x2 + direction, direction)}
    return perimeter


def display_grid(grid: set[tuple[int, int]]) -> None:
    min_x, *_, max_x = sorted(x for x, _ in grid)
    min_y, *_, max_y = sorted(y for _, y in grid)
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            print("#" if (x, y) in grid else ".", end="")
        print("")


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
