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


def run_puzzle(puzzle_input: list[str], start: int = 50) -> tuple[int, int]:
    """How many times does the dial point at 0?"""
    dial = deque(range(100))
    dial.rotate(start)
    p1_count = 0
    p2_count = 0
    for line in puzzle_input:
        amount = int(line[1:])
        tick = -1 if line[0] == "L" else 1
        for _ in range(amount):
            dial.rotate(tick)
            if dial[0] == 0:
                p2_count += 1
        if dial[0] == 0:
            p1_count += 1
    return p1_count, p2_count


def main():
    part_one_result, part_two_result = run_puzzle(TEST_INPUT)
    assert part_one_result == 3, part_one_result
    real_input = Path("day01.txt").read_text().splitlines()
    assert part_two_result == 6, part_two_result
    part_one_result, part_two_result = run_puzzle(real_input)
    print(part_one_result)
    print(part_two_result)


if __name__ == "__main__":
    main()
