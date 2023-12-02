from typing import Callable


def solve(lines: list[str], part: Callable) -> int:
    result: int = 0

    for line in lines:
        result += part(line)

    return result


def part_1(line: str) -> int:
    numbers = []

    for c in line:
        if c.isnumeric():
            numbers.append(int(c))

    return numbers[0] * 10 + numbers[-1]


def part_2(line: str) -> int:
    map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9
    }

    numbers = []

    for i, c in enumerate(line):
        if c.isnumeric():
            numbers.append(int(c))

        for key, value in map.items():
            if line[i:].startswith(key):
                numbers.append(value)

    return numbers[0] * 10 + numbers[-1]


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve(lines, part_1)}")
        print(f"Part 2: {solve(lines, part_2)}")
