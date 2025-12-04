from pathlib import Path

TEST_INPUT = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""


def parse_input(puzzle: str) -> set[tuple[int, int]]:
    grid = set()
    for y, row in enumerate(puzzle.splitlines()):
        for x, char in enumerate(row):
            if char == "@":
                grid.add((x, y))
    return grid


def part_1(puzzle: str) -> int:
    """How many rolls are surrounded by fewer than 4 other rolls?"""
    grid = parse_input(puzzle=puzzle)
    result = 0
    for x, y in grid:
        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x + 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y + 1),
            (x - 1, y - 1),
            (x, y + 1),
            (x, y - 1),
        ]
        if sum(neighbor in grid for neighbor in neighbors) < 4:
            result += 1
    return result


def part_2(puzzle: str) -> int:
    """Keep removing rolls until no further rolls are accessible"""
    grid = parse_input(puzzle=puzzle)
    rolls_removed = set()
    while True:
        rolls_removed_this_turn = set()
        for x, y in list(grid):
            neighbors = [
                (x + 1, y),
                (x - 1, y),
                (x + 1, y + 1),
                (x + 1, y - 1),
                (x - 1, y + 1),
                (x - 1, y - 1),
                (x, y + 1),
                (x, y - 1),
            ]
            if sum(neighbor in grid for neighbor in neighbors) < 4:
                rolls_removed_this_turn.add((x, y))
                grid.remove((x, y))
        if not rolls_removed_this_turn:
            # done
            return len(rolls_removed)
        rolls_removed |= rolls_removed_this_turn


def main():
    part_one_result = part_1(TEST_INPUT)
    assert part_one_result == 13, part_one_result
    puzzle = Path("day04.txt").read_text()
    print(part_1(puzzle))
    part_two_result = part_2(TEST_INPUT)
    assert part_two_result == 43, part_two_result
    print(part_2(puzzle=puzzle))


if __name__ == "__main__":
    main()
