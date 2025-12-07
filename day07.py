from collections import defaultdict
from pathlib import Path


TEST_INPUT = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""


def part_one(puzzle: str) -> int:
    """how many tachyon beams form?"""
    lines = puzzle.splitlines()
    beams = {lines[0].index("S")}
    max_x = len(lines[0])
    splits = 0
    for line in lines[1:]:
        for beam in list(beams):
            if line[beam] == "^":
                beams.remove(beam)
                assert beam not in (0, max_x)
                beams |= {beam + 1, beam - 1}
                splits += 1
    return splits


def part_two(puzzle: str) -> int:
    lines = puzzle.splitlines()
    beams = defaultdict(int)
    # instead of just having a set of beams (above),
    # count the number of ways we can reach that splitter
    beams[lines[0].index("S")] = 1
    max_x = len(lines[0])
    for line in lines[1:]:
        for beam in list(beams):
            if line[beam] == "^":
                routes = beams.pop(beam)
                assert beam not in (0, max_x)
                # then add the number of ways we could get to the parent
                # to the child
                beams[beam + 1] += routes
                beams[beam - 1] += routes
    return sum(beams.values())


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 21, part_one_result
    puzzle = Path("day07.txt").read_text()
    print(part_one(puzzle=puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 40, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
