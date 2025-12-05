from pathlib import Path


TEST_INPUT = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


def part_1(puzzle: str) -> int:
    fresh_ranges, raw_ingredient_ids = puzzle.split("\n\n")
    ingredient_ids = [int(line) for line in raw_ingredient_ids.splitlines()]
    fresh_list = []
    for line in fresh_ranges.splitlines():
        start, end = line.split("-")
        fresh_list.append((int(start), int(end)))
    result = 0
    for pk in ingredient_ids:
        if any(pk >= start and pk <= end for (start, end) in fresh_list):
            result += 1
    return result


def part_2(puzzle: str) -> int:
    fresh_ranges, _ = puzzle.split("\n\n")
    fresh_list = []
    for line in fresh_ranges.splitlines():
        start, end = line.split("-")
        fresh_list.append((int(start), int(end)))
    fresh_list.sort()
    while True:
        # deduplicate!
        for first_index, ((a, b), (c, d)) in enumerate(
            zip(fresh_list[:-1], fresh_list[1:])
        ):
            if b >= c:
                start = min([a, c])
                end = max([b, d])
                # print(f'replacing {a, b} and {c, d} with {start, end} at index {first_index}, length is {len(fresh_list)}')
                del fresh_list[first_index + 1]
                fresh_list[first_index] = (start, end)
                break
        else:
            # we're done here
            break
    result = sum((end - start) + 1 for (start, end) in fresh_list)
    return result


def main():
    part_one_result = part_1(TEST_INPUT)
    assert part_one_result == 3, part_one_result
    puzzle = Path("day05.txt").read_text()
    print(part_1(puzzle=puzzle))
    part_two_result = part_2(TEST_INPUT)
    assert part_two_result == 14, part_two_result
    print(part_2(puzzle=puzzle))


if __name__ == "__main__":
    main()
