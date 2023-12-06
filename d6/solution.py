import re
from math import sqrt, ceil, floor


def solve_part_1(lines: list[str]) -> int:
    inp = parse_input_p1(lines)
    result = 1

    for race_time, min_distance in inp:
        result *= solve_quadratic_equation(race_time, min_distance)

    return result


def parse_input_p1(lines: list[str]) -> list[tuple[int, int]]:
    times = []
    distances = []

    for m in re.finditer(r"(\d+)", lines[0]):
        times.append(int(m.group(0)))

    for m in re.finditer(r"(\d+)", lines[1]):
        distances.append(int(m.group(0)))

    return list(zip(times, distances))


def solve_quadratic_equation(time, distance) -> int:
    d = time * time - 4 * distance
    t_min = (time - sqrt(d)) / 2
    t_max = (time + sqrt(d)) / 2

    t_start = ceil(t_min) if ceil(t_min) > t_min else ceil(t_min) + 1
    t_end = floor(t_max) if floor(t_max) < t_max else floor(t_max) - 1

    return t_end - t_start + 1


def solve_brute_force(time, distance) -> int:
    win_ways = 0

    for t_press in range(1, time):
        d = t_press * (time - t_press)
        if d > distance:
            win_ways += 1

    return win_ways


def solve_part_2(lines: list[str]) -> int:
    time, distance = parse_input_p2(lines)
    return solve_quadratic_equation(time, distance)


def parse_input_p2(lines: list[str]) -> tuple[int, int]:
    time = int(re.search(r"(\d+)", lines[0].replace(" ", "")).groups()[0])
    distance = int(re.search(r"(\d+)", lines[1].replace(" ", "")).groups()[0])

    return time, distance


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve_part_1(lines)}")  # 252000
        print(f"Part 2: {solve_part_2(lines)}")  # 37806486
