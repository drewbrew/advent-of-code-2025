from pathlib import Path
from math import prod

TEST_INPUT = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""


def part_1(puzzle: str) -> int:
    lines = puzzle.splitlines()
    inputs = []
    for line in lines[:-1]:
        row = line.split()
        inputs.append([int(i) for i in row])
    operators = lines[-1].split()
    assert all(len(line) == len(operators) for line in inputs), (inputs, operators)
    result = 0
    for index, operator in enumerate(operators):
        match operator:
            case "+":
                func = sum
            case "*":
                func = prod
            case _:
                raise ValueError(f"Unknown operator {operator}")
        result += func(line[index] for line in inputs)
    return result


def part_2(puzzle: str) -> int:
    lines = puzzle.splitlines()
    *transposed_inputs, operator_line = lines
    operators = [i for i in operator_line if i != " "]
    result = 0
    line_list = [list(line) for line in transposed_inputs]
    max_length = max(len(line) for line in line_list)
    for line in line_list:
        # make sure every row is the same length so we don't lose
        # any digits in the zip()
        if len(line) < max_length:
            difference = max_length - len(line)
            line.extend(" " for _ in range(difference))
    # transpose our result into a list of strings
    transposed_list = [list(row) for row in zip(*line_list)]
    transposed_strs = ["".join(row) for row in transposed_list]
    # it looks like ['1', '2', '3', '   ', ...]
    # where each list entry that's all whitespace is a break between
    # equations
    groups = []
    interim = []
    for word in transposed_strs:
        if stripped := word.strip():
            interim.append(int(stripped))
        else:
            groups.append(interim)
            interim = []
    groups.append(interim)
    assert len(groups) == len(operators), (groups, operators)
    # now we're basically redoing part 1
    for numbers, operator in zip(groups, operators):
        match operator:
            case "+":
                func = sum
            case "*":
                func = prod
            case _:
                raise ValueError(f"Unknown operator {operator}")
        result += func(numbers)
    return result


def main():
    part_one_result = part_1(TEST_INPUT)
    assert part_one_result == 4277556, part_one_result
    puzzle = Path("day06.txt").read_text()
    print(part_1(puzzle))
    part_two_result = part_2(TEST_INPUT)
    assert part_two_result == 3263827, part_two_result
    print(part_2(puzzle))


if __name__ == "__main__":
    main()
