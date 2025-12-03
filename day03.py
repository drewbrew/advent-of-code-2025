from pathlib import Path

TEST_INPUT = """987654321111111
811111111111119
234234234234278
818181911112111"""


def part_one(puzzle: str, number_of_batteries: int = 2) -> int:
    """Find the max joltage from each row"""
    result = 0
    for line in puzzle.splitlines():
        digits_accrued = []
        last_digit_index = 0
        while len(digits_accrued) < number_of_batteries:
            batteries_remaining = number_of_batteries - len(digits_accrued)
            max_next_digit = max(
                # need this to avoid off-by-one issues because [:0] gives an empty string
                line[last_digit_index:]
                if batteries_remaining == 1
                else line[last_digit_index : -(batteries_remaining - 1)]
            )
            last_digit_index += line[last_digit_index:].index(max_next_digit) + 1
            digits_accrued.append(max_next_digit)
            # print(f'found {max_next_digit} at index {last_digit_index}, current score {"".join(digits_accrued)}')

        result += int("".join(digits_accrued))
    return result


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 357, part_one_result
    puzzle = Path("day03.txt").read_text()
    print(part_one(puzzle))
    part_two_result = part_one(TEST_INPUT, 12)
    assert part_two_result == 3121910778619, part_two_result
    print(part_one(puzzle, 12))


if __name__ == "__main__":
    main()
