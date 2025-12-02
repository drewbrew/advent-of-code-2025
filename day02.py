from pathlib import Path

TEST_INPUT = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""


def part_one(puzzle: str) -> int:
    groups = puzzle.split(",")
    result = 0
    for group in groups:
        start, end = (int(i) for i in group.split("-"))
        for pk in range(start, end + 1):
            pk_str = str(pk)
            length = len(pk_str) // 2
            if pk_str[:length] == pk_str[length:]:
                # print("found invalid ID", pk)
                result += pk
    return result


def part_two(puzzle: str) -> int:
    groups = puzzle.split(",")
    result = 0
    for group in groups:
        results_found = set()
        start, end = (int(i) for i in group.split("-"))
        for pk in range(start, end + 1):
            pk_str = str(pk)
            length = len(pk_str)
            for span in range(1, length):
                if length % span:
                    # not a clean multiple
                    continue
                multiplier = length // span
                if pk_str[:span] * multiplier == pk_str:
                    if pk in results_found:
                        # skip duplicates
                        continue
                    # print("found invalid ID", pk)
                    result += pk
                    results_found.add(pk)
    return result


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 1227775554, part_one_result
    puzzle = Path("day02.txt").read_text()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 4174379265, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
