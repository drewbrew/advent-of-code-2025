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


def run_puzzle(puzzle: str) -> tuple[int, int]:
    lines = puzzle.splitlines()
    beams = defaultdict(int)
    # count the number of ways we can reach that splitter (part 2)
    beams[lines[0].index("S")] = 1
    # and the number of splits (part 1)
    splits = 0
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
                # part 1 result
                splits += 1
    return splits, sum(beams.values())


def main():
    part_one_result, part_two_result = run_puzzle(TEST_INPUT)
    assert part_one_result == 21, part_one_result
    assert part_two_result == 40, part_two_result
    puzzle = Path("day07.txt").read_text()
    part_two_result = run_puzzle(TEST_INPUT)
    print("\n".join(str(i) for i in run_puzzle(puzzle)))


if __name__ == "__main__":
    main()
