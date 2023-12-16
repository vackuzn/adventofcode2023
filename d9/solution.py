def solve_part_1(lines: list[str]) -> int:
    result = 0

    for line in lines:
        result += forecast_element([int(num_str) for num_str in line.split(" ")], True)

    return result


def solve_part_2(lines: list[str]) -> int:
    result = 0

    for line in lines:
        result += forecast_element([int(num_str) for num_str in line.split(" ")], False)

    return result


def forecast_element(numbers: list[int], forward: bool) -> int:
    pyramid = [numbers]

    while any([el for el in pyramid[-1] if el != 0]):
        pyramid.append(get_derivatives(pyramid[-1]))

    predicted_element = 0
    for row in pyramid[::-1]:
        predicted_element = row[-1] + predicted_element if forward else row[0] - predicted_element

    return predicted_element


def get_derivatives(numbers: list[int]) -> list[int]:
    result = []

    for idx in range(len(numbers) - 1):
        result.append(numbers[idx + 1] - numbers[idx])

    return result


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve_part_1(lines)}")  # 2075724761
        print(f"Part 2: {solve_part_2(lines)}")  # 1072
