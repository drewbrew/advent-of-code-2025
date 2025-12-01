from collections import deque
from pathlib import Path


TEST_INPUT = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""".splitlines()


def part_1(puzzle_input: list[str], start: int = 50) -> int:
    """How many times does the pudialzzle point at 0?"""
    dial = deque(range(100))
    dial.rotate(start)
    count = 0
    for line in puzzle_input:
        amount = int(line[1:]) * (-1 if line[0] == "L" else 1)
        dial.rotate(amount)
        if dial[0] == 0:
            count += 1
    return count


def part_2(puzzle_input: list[str], start: int = 50) -> int:
    """How many times does the dial cross 0?"""
    dial = deque(range(100))
    dial.rotate(start)
    count = 0
    for line in puzzle_input:
        amount = int(line[1:])
        tick = -1 if line[0] == "L" else 1
        for _ in range(amount):
            dial.rotate(tick)
            if dial[0] == 0:
                count += 1
    return count


def main():
    part_one_result = part_1(TEST_INPUT)
    assert part_one_result == 3, part_one_result
    real_input = Path("day01.txt").read_text().splitlines()
    print(part_1(real_input))
    part_two_result = part_2(TEST_INPUT)
    assert part_two_result == 6, part_two_result
    print(part_2(real_input))


if __name__ == "__main__":
    main()
