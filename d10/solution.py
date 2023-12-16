from typing import Optional


def solve_part_1(lines: list[str]) -> int:
    grid = Grid(lines)
    curve_points = get_curve_points(grid)

    return len(curve_points) // 2


def get_curve_points(grid: "Grid") -> list[tuple[int, int]]:
    current = grid.get_start_cell_coordinates()
    visited = []

    while True:
        visited.append(current)
        next_cell = grid.get_next_connected_cell(current[0], current[1], visited)

        if next_cell is None:
            break

        current = next_cell

    return visited


# Use more complex ray tracing algorithm for a change
def solve_part_2(lines: list[str]) -> int:
    grid = Grid(lines)
    curve_points = get_curve_points(grid)

    outside_points = set()
    inside_points = set()

    for y in range(len(lines) - 1):
        for x in range(len(lines[y]) - 1):
            if (x, y) in curve_points:
                continue

            if y == 0 or y == len(curve_points) - 1 or x == 0 or x == len(curve_points[y]) - 1:
                outside_points.add((x, y))
                continue

            curve_crossed_times = 0
            curve_enter_symbol = None
            for ray_y in range(y - 1, -2, -1):
                if (x, ray_y) in curve_points:
                    symbol = grid.get(x, ray_y)
                    if symbol in ["L", "J"]:
                        curve_enter_symbol = symbol
                    elif symbol in ["7", "F"]:
                        if (curve_enter_symbol == "J" and symbol == "F") or (curve_enter_symbol == "L" and symbol == "7"):
                            curve_crossed_times += 1
                        curve_enter_symbol = None
                    elif symbol in ["-"]:
                        curve_crossed_times += 1

                    continue

                if (x, ray_y) in outside_points or ray_y < 0:
                    if curve_crossed_times % 2 == 0:
                        outside_points.add((x, y))
                    else:
                        inside_points.add((x, y))
                    break

                if (x, ray_y) in inside_points:
                    if curve_crossed_times % 2 == 1:
                        outside_points.add((x, y))
                    else:
                        inside_points.add((x, y))
                    break

    return len(inside_points)


class Grid:
    def __init__(self, lines: list[str]):
        self.lines = lines.copy()
        self.start_cell_coordinates = self.get_start_cell_coordinates()
        self._restore_start_cell_value()

    def _restore_start_cell_value(self):
        x, y = self.get_start_cell_coordinates()

        if self.lines[y][x] != "S":
            return

        form = ""

        # up
        if y > 0:
            value = self.lines[y - 1][x]
            if value in ["|", "7", "F"]:
                form += "U"

        # down
        if y < len(self.lines) - 1:
            value = self.lines[y + 1][x]
            if value in ["|", "L", "J"]:
                form += "D"

        # left
        if x > 0:
            value = self.lines[y][x - 1]
            if value in ["-", "L", "F"]:
                form += "L"

        # right
        if x < len(self.lines[0]) - 1:
            value = self.lines[y][x + 1]
            if value in ["-", "J", "7"]:
                form += "R"

        if form == "UD":
            result = "|"
        elif form == "LR":
            result = "-"
        elif form == "UL":
            result = "J"
        elif form == "UR":
            result = "L"
        elif form == "DL":
            result = "7"
        elif form == "DR":
            result = "F"
        else:
            raise Exception("Unexpected form " + form)

        self.lines[y] = self.lines[y].replace("S", result)

    def get_next_connected_cell(self, x: int, y: int, visited: list[tuple[int, int]]) -> Optional[tuple[int, int]]:
        value = self.lines[y][x]

        if value == "-":
            connections = {(x - 1, y), (x + 1, y)}
        elif value == "|":
            connections = {(x, y + 1), (x, y - 1)}
        elif value == "L":
            connections = {(x, y - 1), (x + 1, y)}
        elif value == "J":
            connections = {(x, y - 1), (x - 1, y)}
        elif value == "7":
            connections = {(x, y + 1), (x - 1, y)}
        elif value == "F":
            connections = {(x, y + 1), (x + 1, y)}
        else:
            raise Exception("Unexpected cell value " + value)

        result = list(connections - set(visited))

        if len(result) == 0:
            return None

        return result[0]

    def get_start_cell_coordinates(self):
        for y in range(len(self.lines)):
            for x in range(len(self.lines[y])):
                if self.lines[y][x] == "S":
                    return x, y

        return self.start_cell_coordinates

    def get(self, x: int, y: int) -> str:
        return self.lines[y][x]


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve_part_1(lines)}")  # 6714
        print(f"Part 2: {solve_part_2(lines)}")  # 429
