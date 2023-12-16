from typing import Optional, List, Tuple


def solve_part_1(lines: list[str]) -> int:
    return solve(SpaceGrid(lines), 2)


def solve_part_2(lines: list[str]) -> int:
    return solve(SpaceGrid(lines), 1000000)


def solve(grid: "SpaceGrid", exp_rate: int) -> int:
    grid.expand_space(exp_rate)

    galaxy_pairs = get_galaxy_pairs(grid.galaxies)

    result = 0
    for g1, g2 in galaxy_pairs:
        exp_rate = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
        result += exp_rate

    return result


def get_galaxy_pairs(galaxies: list[tuple[int, int]]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    result = []

    for g1_idx in range(len(galaxies) - 1):
        for g2_idx in range(g1_idx + 1, len(galaxies)):
            result.append((galaxies[g1_idx], galaxies[g2_idx]))

    return result


class SpaceGrid:
    def __init__(self, lines: list[str]):
        self.lines = lines.copy()
        self.galaxies = self._get_initial_galaxy_positions()

    def expand_space(self, exp_rate: int) -> None:
        for idx in range(len(self.lines) - 1, -1, -1):
            if all([elem == "." for elem in self.lines[idx]]):
                self._move_galaxies_down(idx, exp_rate)

        for idx in range(len(self.lines[0]) - 1, -1, -1):
            if all([elem == "." for elem in self._get_column(idx)]):
                self._move_galaxies_right(idx, exp_rate)

    def _get_column(self, idx: int) -> str:
        return ''.join([row[idx] for row in self.lines])

    def _get_initial_galaxy_positions(self) -> list[tuple[int, int]]:
        result = []

        for y, line in enumerate(self.lines):
            for x, symbol in enumerate(line):
                if symbol == "#":
                    result.append((x, y))

        return sorted(result)

    def _move_galaxies_down(self, min_y: int, exp_rate: int) -> None:
        for idx, galaxy in enumerate(self.galaxies):
            g_x, g_y = galaxy

            if g_y > min_y:
                self.galaxies[idx] = (g_x, g_y + exp_rate - 1)

    def _move_galaxies_right(self, min_x: int, exp_rate: int) -> None:
        for idx, galaxy in enumerate(self.galaxies):
            g_x, g_y = galaxy

            if g_x > min_x:
                self.galaxies[idx] = (g_x + exp_rate - 1, g_y)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve_part_1(lines)}")  # 9329143
        print(f"Part 2: {solve_part_2(lines)}")  # 710674907809
