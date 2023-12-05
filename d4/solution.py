def get_card_winning_numbers_count(line: str) -> int:
    _, scores = line.split(":")

    winning_numbers = set([int(c) for c in scores.split("|")[0].strip().split(" ") if c.isnumeric()])
    my_numbers = set([int(c) for c in scores.split("|")[1].strip().split(" ") if c.isnumeric()])

    my_winning_numbers = my_numbers.intersection(winning_numbers)

    return len(my_winning_numbers)


def solve_part_1(lines: list[str]) -> int:
    scores = 0

    for line in lines:
        winning_numbers_count = get_card_winning_numbers_count(line)

        if winning_numbers_count == 0:
            continue

        score = 2 ** (winning_numbers_count - 1)
        scores += score

    return scores


class Card:
    def __init__(self, winning_numbers_count: int):
        self.number_of_copies = 1
        self.winning_numbers_count = winning_numbers_count

    def add_copies(self, number_of_copies: int):
        self.number_of_copies += number_of_copies


def solve_part_2(lines: list[str]) -> int:
    cards = []

    for line in lines:
        winning_numbers_count = get_card_winning_numbers_count(line)
        cards.append(Card(winning_numbers_count))

    for idx in range(len(cards)):
        card = cards[idx]

        for i in range(card.winning_numbers_count):
            cards[idx + i + 1].add_copies(card.number_of_copies)

    number_of_cards = 0
    for card in cards:
        number_of_cards += card.number_of_copies

    return number_of_cards


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve_part_1(lines)}")
        print(f"Part 2: {solve_part_2(lines)}")
