import heapq
from pathlib import Path

TEST_INPUT = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""


def parse_input(puzzle: str) -> list[tuple[int, int]]:
    result = []
    for line in puzzle.splitlines():
        end_of_target = line.index("]")
        numeric_target = 0
        for char in reversed(line[1:end_of_target]):
            # need to reverse our bit order so that the indexes work
            numeric_target <<= 1
            numeric_target |= char == "#"

        start_of_joltage = line.index("{")
        raw_switch_groups = line[end_of_target + 3 : start_of_joltage - 2].split(") (")
        # print(raw_switch_groups)
        switch_groups = [
            tuple(int(i) for i in group.split(",")) for group in raw_switch_groups
        ]
        numeric_switches = []
        for group in switch_groups:
            numeric_switch = sum(1 << i for i in group)
            numeric_switches.append(numeric_switch)
        result.append((numeric_target, numeric_switches))
    return result


def parse_input_part_2(puzzle: str) -> list[tuple[list[int], list[int]]]:
    result = []
    for line in puzzle.splitlines():
        end_of_target = line.index("]")

        start_of_joltage = line.index("{")
        raw_switch_groups = line[end_of_target + 3 : start_of_joltage - 2].split(") (")
        switch_groups = [
            list(int(i) for i in group.split(",")) for group in raw_switch_groups
        ]
        joltage = [int(i) for i in line[start_of_joltage + 1 : -1].split(",")]
        result.append((switch_groups, joltage))
    return result


def do_invert(initial_state: int, switches_to_flip: int) -> list[bool]:
    result = initial_state ^ switches_to_flip
    return result


def part_one(puzzle: str) -> int:
    lines = parse_input(puzzle=puzzle)
    answer = 0
    for target, switch_groups in lines:
        # print(f'{target=}, {switch_groups=}')
        state = 0
        search = [(1, do_invert(state, group)) for group in switch_groups]
        heapq.heapify(search)
        while True:
            step_count, state = heapq.heappop(search)
            print(step_count, end="\r")
            if state == target:
                print("\ndone", step_count)
                answer += step_count
                break
            for group in switch_groups:
                heapq.heappush(search, (step_count + 1, do_invert(state, group)))
    return answer


def push_button_p2(state: list[int], buttons: list[int]) -> list[int]:
    result = state[:]
    for button in buttons:
        result[button] += 1
    return result


def part_two(puzzle: str) -> int:
    lines = parse_input_part_2(puzzle=puzzle)
    answer = 0
    for switch_groups, joltage in lines:
        # print(f'{target=}, {switch_groups=}')
        state = [0 for _ in range(len(joltage))]
        search = [(1, push_button_p2(state, group)) for group in switch_groups]
        heapq.heapify(search)
        while True:
            step_count, state = heapq.heappop(search)
            print(step_count, end="\r")
            if state == joltage:
                print("\ndone", step_count)
                answer += step_count
                break
            if any(level > target_level for level, target_level in zip(state, joltage)):
                # print("pruning")
                continue
            for group in switch_groups:
                heapq.heappush(search, (step_count + 1, push_button_p2(state, group)))
    return answer


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 7, part_one_result
    puzzle = Path("day10.txt").read_text()
    print(part_one(puzzle))
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 33, part_two_result
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
