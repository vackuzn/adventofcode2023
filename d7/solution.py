from collections import Counter
from enum import Enum


class HandType(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_KIND = 6
    FIVE_OF_KIND = 7


class Hand:
    def __init__(self, cards: str, bid: int, jocker_enabled: bool = False):
        self.jocker_enabled = jocker_enabled
        self.cards = cards
        self.bid = bid
        self.rank = 0

        self.hand_type = get_best_hand_type(cards) if jocker_enabled else get_hand_type(cards)
        self.score = self.hand_type.value * 16 ** 5 + self.get_card_score()

    def get_card_score(self) -> int:
        score = 0
        for idx, card in enumerate(self.cards[::-1]):
            score += get_card_value(card, self.jocker_enabled) * 16 ** idx

        return score

    def get_won_bid(self) -> int:
        return self.bid * self.rank


def get_best_hand_type(cards: str) -> HandType:
    cards_no_jocker = cards.replace("J", "")
    jocker_count = len(cards) - len(cards_no_jocker)

    if jocker_count == 0:
        return get_hand_type(cards)

    if jocker_count == 5:
        return get_hand_type("A" * 5)

    card = get_card_to_add(cards_no_jocker)
    return get_hand_type(cards_no_jocker + card * jocker_count)


def get_hand_type(cards: str) -> HandType:
    distinct = sorted(list(Counter(cards).values()), reverse=True)

    if distinct[0] == 5:
        return HandType.FIVE_OF_KIND

    if distinct[0] == 4:
        return HandType.FOUR_OF_KIND

    if distinct[0] == 3:
        if len(cards) == 5 and distinct[1] == 2:
            return HandType.FULL_HOUSE

        return HandType.THREE_OF_KIND

    if distinct[0] == 2:
        if len(cards) > 2 and distinct[1] == 2:
            return HandType.TWO_PAIR

        return HandType.ONE_PAIR

    return HandType.HIGH_CARD


def get_card_to_add(cards: str) -> str:
    best_card = ''
    card_count = 0

    for card, count in Counter(cards).items():
        if count == card_count:
            best_card_value = get_card_value(best_card, True)
            card_value = get_card_value(card, True)

            if card_value > best_card_value:
                best_card = card

        if count > card_count:
            card_count = count
            best_card = card

    return best_card


def get_card_value(card: str, jocker_enabled: bool) -> int:
    card_values = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 1 if jocker_enabled else 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    return card_values[card]


def solve_part_1(lines: list[str]) -> int:
    return solve(lines, jocker_enabled=False)


def solve_part_2(lines: list[str]) -> int:
    return solve(lines, jocker_enabled=True)


def solve(lines: list[str], jocker_enabled: bool) -> int:
    hands = []

    for line in lines:
        cards, bid_str = line.split(" ")
        bid = int(bid_str)

        hands.append(Hand(cards, bid, jocker_enabled))

    hands.sort(key=lambda h: h.score)

    for idx, hand in enumerate(hands):
        hand.rank = idx + 1

    result = sum([hand.get_won_bid() for hand in hands])
    return result


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        print(f"Part 1: {solve_part_1(lines)}")  # 250951660
        print(f"Part 2: {solve_part_2(lines)}")  # 251481660
