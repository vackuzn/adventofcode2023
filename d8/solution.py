import re
from functools import reduce


def solve_part_1(lines: list[str]) -> int:
    directions, m = parse_input(lines)

    return get_number_of_steps(directions, m, "AAA", end_nodes=["ZZZ"])


def solve_part_2(lines: list[str]) -> int:
    directions, m = parse_input(lines)

    nodes = [n for n in m.keys() if n[2] == "A"]
    end_nodes = [n for n in m.keys() if n[2] == "Z"]

    steps = []
    for node in nodes:
        steps.append(get_number_of_steps(directions, m, node, end_nodes=end_nodes))

    result = reduce(compute_lcm, steps)
    return result


def parse_input(lines: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    directions = lines[0]

    m = {}

    for line in lines[2:]:
        match = re.match(r"(\w{3}) = \((\w{3}), (\w{3})\)", line)  # AAA = (BBB, CCC)

        node = match.groups()[0]
        left = match.groups()[1]
        right = match.groups()[2]

        m[node] = (left, right)

    return directions, m


def get_number_of_steps(directions: str, m: dict[str, tuple[str, str]], start_node: str, end_nodes: list[str]) -> int:
    node = start_node

    steps = 0
    while True:
        if directions[steps % len(directions)] == "L":
            node = m[node][0]
        else:
            node = m[node][1]

        steps += 1

        if node in end_nodes:
            break

    return steps


def compute_gcd(x: int, y: int) -> int:
    while y:
        x, y = y, x % y

    return x


def compute_lcm(x: int, y: int) -> int:
    lcm = (x * y) // compute_gcd(x, y)
    return lcm


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve_part_1(lines)}")  # 18673
        print(f"Part 2: {solve_part_2(lines)}")  # 17972669116327
