import re
from functools import reduce


def solve_part_1(lines: list[str]) -> int:
    max_available = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    result = 0

    for line in lines:
        game_id, sets = parse_game(line)

        if all_sets_fit(sets, max_available):
            result += game_id

    return result


def parse_games(lines: list[str]):
    games = {}

    for line in lines:
        game_id, sets = parse_game(line)
        games[game_id] = sets

    return games


def parse_game(line: str) -> tuple[int,  list[dict[str, int]]]:
    game_str, sets_str = line.split(":")

    match = re.search(r"(\d+)", game_str)
    game_id = int(match.groups()[0])

    sets = [parse_set(s) for s in sets_str.split(";")]

    return game_id, sets


def parse_set(set_value: str) -> dict[str, int]:
    matches = {}

    for match in re.finditer(r"(\d+) (\w+)", set_value):
        groups = match.groups()
        color = groups[1]
        count = int(groups[0])

        matches[color] = count

    return matches


def all_sets_fit(sets: list[dict[str, int]], max: dict[str, int]) -> bool:
    for s in sets:
        if not set_fits(s, max):
            return False

    return True


def set_fits(s: dict[str, int], max: dict[str, int]) -> bool:
    for color, max_count in max.items():
        count = s.get(color, 0)

        if count > max[color]:
            return False

    return True


def solve_part_2(lines: list[str]) -> int:
    result = 0

    for line in lines:
        game_id, sets = parse_game(line)
        min_set = get_min_set(sets)
        game_power = reduce(lambda x, y: x*y, min_set.values())
        result += game_power

    return result


def get_min_set(sets: list[dict[str, int]]) -> dict[str, int]:
    result = {}

    for s in sets:
        for color, count in s.items():
            max_color_cnt = result.get(color, 0)

            result[color] = max(count, max_color_cnt)

    return result


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve_part_1(lines)}")
        print(f"Part 2: {solve_part_2(lines)}")
