from functools import reduce

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_adjacent_points(self, max_y: int, max_x: int) -> list["Point"]:
        possible_neighbors = [
            # above
            (self.y - 1, self.x - 1),
            (self.y - 1, self.x),
            (self.y - 1, self.x + 1),

            # left, right
            (self.y, self.x - 1),
            (self.y, self.x + 1),

            # below
            (self.y + 1, self.x - 1),
            (self.y + 1, self.x),
            (self.y + 1, self.x + 1),
        ]

        result = []
        for n_y, n_x in possible_neighbors:
            if n_y < 0 or n_y > max_y or n_x < 0 or n_x > max_x:
                continue
            result.append(Point(y=n_y, x=n_x))

        return result

    def get_value(self, lines: list[str]) -> str:
        return lines[self.y][self.x]


@dataclass(frozen=True)
class Number:
    coords: Point
    length: int
    value: int


def solve_part_1(lines: list[str]) -> int:
    symbol_points = read_symbol_points(lines)

    digit_points = set()
    for symbol_point in symbol_points:
        d_points = get_adjacent_digits(lines, symbol_point)
        digit_points |= d_points

    numbers = recreate_numbers(lines, digit_points)
    return sum(n.value for n in numbers)


def solve_part_2(lines: list[str]) -> int:
    star_points = read_star_points(lines)

    result = 0
    for star_point in star_points:
        digit_points = get_adjacent_digits(lines, star_point)
        numbers = recreate_numbers(lines, digit_points)

        if len(numbers) == 2:
            result += reduce((lambda x, y: x * y), [n.value for n in numbers])

    return result


def read_symbol_points(lines: list[str]) -> list[Point]:
    points = []

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                continue
            elif char.isnumeric():
                continue
            else:
                points.append(Point(y=y, x=x))

    return points


def get_adjacent_digits(lines: list[str], symbol_point: Point) -> set[Point]:
    max_x = len(lines[0]) - 1
    max_y = len(lines) - 1

    digits_points = set()

    for adj_point in symbol_point.get_adjacent_points(max_y, max_x):
        if adj_point.get_value(lines).isnumeric():
            digits_points.add(adj_point)

    return digits_points


def recreate_numbers(lines: list[str], digit_points: set[Point]) -> set[Number]:
    numbers = set()

    for digit_point in digit_points:
        line = lines[digit_point.y]
        x_start = digit_point.x
        x_end = digit_point.x

        while x_start > 0 and line[x_start - 1].isnumeric():
            x_start -= 1

        while x_end < len(line) - 1 and line[x_end + 1].isnumeric():
            x_end += 1

        value = int(line[x_start:x_end + 1])

        numbers.add(Number(coords=Point(y=digit_point.y, x=x_start), length=x_end - x_start + 1, value=value))

    return numbers


def read_star_points(lines: list[str]) -> list[Point]:
    points = []

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "*":
                points.append(Point(y=y, x=x))

    return points


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve_part_1(lines)}")  # 519444
        print(f"Part 2: {solve_part_2(lines)}")  # 74528807
