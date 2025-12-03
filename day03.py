from itertools import combinations
from pathlib import Path

TEST_INPUT = """987654321111111
811111111111119
234234234234278
818181911112111"""

def part_one(puzzle: str, number_of_batteries: int = 2) -> int:
    """Find the max joltage from each row"""
    result = 0
    for line in puzzle.splitlines():
        line_max = 0
        for battery in combinations(line, number_of_batteries):
            score = int(''.join(battery))
            if score > line_max:
                print(f'new max for {line}: {score}')
                line_max = score
        print(f'max for {line} is {line_max}')
        result += line_max
    return result


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 357, part_one_result
    puzzle = Path('day03.txt').read_text()
    print(part_one(puzzle))
    part_two_result = part_one(TEST_INPUT, 12)
    assert part_two_result == 3121910778619, part_two_result
    print(part_one(puzzle, 12))

if __name__ == '__main__':
    main()
