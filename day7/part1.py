from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Tuple, NewType
from pprint import pprint
from functools import cmp_to_key

camel_cards = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

hand_types = {'Five of a Kind': 7,
                  'Four of a Kind': 6, 
                  'Full House': 5,
                  'Three of a Kind': 4,
                  'Two Pair': 3,
                  'One Pair': 2,
                  'High Card': 1}


@dataclass
class Hand:
    cards: str
    bid: int
    hand_type: str
    
    @property
    def hand_type_sort_value(self) -> int:
        return hand_types[self.hand_type]
    
    @property
    def sort_key(self) -> Tuple[int, List[int]]:
        return (self.hand_type_sort_value, [camel_cards[card] for card in self.cards])

def read_input(input_file: Path) -> List[str]:
    with input_file.open("r") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]

def parse_hand(line: str) -> Hand:
    cards_text, bid_text = (line.lstrip()).split(" ")
    hand = Hand(cards=cards_text, bid=int(bid_text), hand_type='')
    return hand

def is_type(hand: Hand) -> Hand:
    cards = hand.cards
    if count_unique(cards) == 5:
        hand.hand_type = 'High Card'
    elif count_unique(cards) == 4:
        hand.hand_type = 'One Pair'
    elif count_unique(cards) == 3:
        # Can be: 'Two Pair' or 'Three of a Kind'
        hand_three_of_kind = is_three_cards_unique(cards)
        if hand_three_of_kind is False:
            hand.hand_type = 'Two Pair'
        else:
            hand.hand_type = 'Three of a Kind'
    elif count_unique(cards) == 2:
        # Can be: 'Full House' or 'Four of a Kind'
        hand_full_house = is_three_cards_unique(cards)
        if hand_full_house:
            hand.hand_type = 'Full House'
        else:
            hand.hand_type = 'Four of a Kind'
    else:
        hand.hand_type = 'Five of a Kind'
    return hand

def count_unique(cards: str) -> int:
    card_holder = [c for c in cards]
    return len(set(card_holder))

def is_three_cards_unique(cards: str) -> bool:
    card_holder = [c for c in cards]
    cards_set = {}
    for c in set(card_holder):
        cards_set[c] = 0
    for card in cards:
        cards_set[card] = cards_set[card] + 1
    if 3 in cards_set.values():
        return True
    else:
        return False
    
def determine_rank(hands: List[Hand]) -> List[Hand]:
    return hands

if __name__ == "__main__":
    lines = read_input(Path("inputs/test_input_yields_6440.txt"))
    hands = [parse_hand(line) for line in lines]
    hands = [is_type(hand) for hand in hands]
    # pprint(hands)
    # print()
    hands_sorted = sorted(hands, key=lambda hand: hand.sort_key)
    total_winnings = 0
    for index, hand in enumerate(hands_sorted):
        total_winnings += (index + 1) * hand.bid

    pprint(total_winnings)