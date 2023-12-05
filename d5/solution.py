import re
from typing import Optional


def solve_part_1(lines: list[str]) -> int:
    seeds = parse_seeds(lines)
    maps = parse_maps(lines)

    return get_min_location_for_seeds(seeds, maps)


def solve_part_2(lines: list[str]) -> int:
    def seed_in_range(seed: int) -> bool:
        for start, rng in seed_ranges:
            if start <= seed < start + rng:
                return True

        return False

    seed_ranges = parse_seed_ranges(lines)
    maps = parse_maps(lines)

    # Seed to location function linearly grows except for range start points
    # Minimum can be either at seed range start or at range start in one of the maps
    seed_candidates = [s[0] for s in seed_ranges]

    for m in maps:
        for range_start in m.get_dst_range_starts():
            seed_for_range_start = m.backward_chain(range_start)
            seed_candidates.append(seed_for_range_start)

    return get_min_location_for_seeds(list(filter(seed_in_range, seed_candidates)), maps)


def get_min_location_for_seeds(seeds: list[int], maps: list["Map"]) -> int:
    start_map = maps[0]

    # using dict for easier debugging
    seed_locations = {}
    for seed in seeds:
        location = start_map.forward_chain(seed)
        seed_locations[seed] = location

    result = min(seed_locations.values())
    return result


class Map:
    def __init__(self, mappings: list):
        self.mappings = mappings
        self.prev: Optional["Map"] = None
        self.next: Optional["Map"] = None

    def forward_chain(self, src: int) -> int:
        res = self.forward(src)
        if self.next is not None:
            return self.next.forward_chain(res)
        return res

    def forward(self, src: int) -> int:
        for dst_start, src_start, rng in self.mappings:
            if src_start <= src < src_start + rng:
                return src - src_start + dst_start

        return src

    def backward_chain(self, dst: int) -> int:
        res = self.backward(dst)
        if self.prev is not None:
            return self.prev.backward_chain(res)

        return res

    def backward(self, dst: int) -> int:
        for dst_start, src_start, rng in self.mappings:
            if dst_start <= dst < dst_start + rng:
                return dst - dst_start + src_start

        return dst

    def get_dst_range_starts(self) -> list[int]:
        return [dst_start for dst_start, _, _ in self.mappings]


def parse_maps(lines: list[str]) -> list[Map]:
    maps = []

    mappings = []

    for line in lines:
        if line.strip() == "":
            continue

        if line.startswith("seeds:"):
            continue

        if "map:" in line:
            if len(mappings) > 0:
                maps.append(Map(mappings=mappings))

            mappings = []
            continue

        match = re.search(r"(\d+) (\d+) (\d+)", line)
        dst_start = int(match.groups()[0])
        src_start = int(match.groups()[1])
        rng = int(match.groups()[2])

        mappings.append((dst_start, src_start, rng))

    maps.append(Map(mappings=mappings))

    for idx in range(len(maps)):
        maps[idx].prev = maps[idx - 1] if idx > 0 else None
        maps[idx].next = maps[idx + 1] if idx < len(maps) - 1 else None

    return maps


def parse_seeds(lines: list[str]) -> list[int]:
    for line in lines:
        if line.startswith("seeds:"):
            return [int(seed_num.strip()) for seed_num in line.replace("seeds:", "").split(" ") if seed_num.strip() != ""]

    raise Exception("No seeds found")


def parse_seed_ranges(lines: list[str]) -> list[tuple[int, int]]:
    seeds = parse_seeds(lines)

    return [(seeds[idx], seeds[idx+1]) for idx in range(0, len(seeds), 2)]


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve_part_1(lines)}")  # 1181555926
        print(f"Part 2: {solve_part_2(lines)}")  # 37806486
