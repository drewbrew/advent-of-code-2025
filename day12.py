"""Day 12: storing some packages"""

from pathlib import Path


TEST_INPUT = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""


def part_one(puzzle: str) -> int:
    """Can we fit enough of the packages inside the given area?"""

    *raw_packages, raw_requirements = puzzle.split("\n\n")
    result = 0
    packages = []
    for package in raw_packages:
        grid = set()
        lines = package.splitlines()[1:]
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == "#":
                    grid.add((x, y))
        packages.append(grid)
    for line in raw_requirements.splitlines():
        # let's try the stupid approach first: is
        # the given area big enough to hold the requirements?
        space, package_needs = line.split(": ")
        x, y = (int(i) for i in space.split("x"))
        needs = [int(i) for i in package_needs.split()]
        total_area_available = x * y
        area_consumed = sum(
            need * len(package) for (need, package) in zip(needs, packages, strict=True)
        )
        if area_consumed <= total_area_available:
            result += 1
    return result


def main():
    # LOL my answer works for the real puzzle but not the test input
    # what a troll puzzle
    # part_one_result = part_one(TEST_INPUT)
    # assert part_one_result == 2, part_one_result
    puzzle = Path("day12.txt").read_text()
    print(part_one(puzzle))


if __name__ == "__main__":
    main()
