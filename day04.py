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


def is_roll_accessible(x: int, y: int, grid: set[tuple[int, int]]) -> bool:
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
    return sum(neighbor in grid for neighbor in neighbors) < 4

def find_accessible_rolls(grid: set[tuple[int, int]]) -> set[tuple[int, int]]:
    return {(x, y) for (x, y) in grid if is_roll_accessible(x, y, grid)}


def part_1(puzzle: str) -> int:
    """How many rolls are surrounded by fewer than 4 other rolls?"""
    grid = parse_input(puzzle=puzzle)
    return len(find_accessible_rolls(grid))


def part_2(puzzle: str) -> int:
    """Keep removing rolls until no further rolls are accessible"""
    grid = parse_input(puzzle=puzzle)
    rolls_removed = 0
    while (rolls_removed_this_turn := find_accessible_rolls(grid)) != set():
        rolls_removed += len(rolls_removed_this_turn)
        grid ^= rolls_removed_this_turn
    return rolls_removed


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
