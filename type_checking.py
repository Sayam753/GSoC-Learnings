'''
Use function.__annotations__ to inspect all annotations

Tuples are immutable, typically stores fixed number of elements
of possibly different types. So use Tuple[t_1, t_2, t_3, ...]

Lists are mutable, typically stores unknown number of elements 
of same data types. So use List[type]
'''
from typing import Dict, List, Tuple

import random

SUITS = "P D H C".split()
RANKS = "2 3 4 5 6 7 8 9 10 J Q K A".split()


def deal_hands(deck):
    """Deal the cards in the deck into four hands"""
    return (deck[0::4], deck[1::4], deck[2::4], deck[3::4])


def play():
    """Play a 4-player card game"""
    deck = create_deck(shuffle=True)
    names = "P1 P2 P3 P4".split()
    hands = {n: h for n, h in zip(names, deal_hands(deck))}

    for name, cards in hands.items():
        card_str = " ".join(f"{s}{r}" for (s, r) in cards)
        print(f"{name}: {card_str}")


def create_deck(shuffle: bool = False) -> List[Tuple[str, str]]:
    """Create a new deck of 52 cards"""
    deck = [(s, r) for r in RANKS for s in SUITS]
    if shuffle:
        random.shuffle(deck)
    return deck


def merge(*args: list, **kwargs: dict):
    print(type(args))
    print(type(kwargs))
    for mappable in args:
        if set(mappable) & set(kwargs):  # Intersection of keys
            raise ValueError(
                "Found duplicate keys in merge: {}".format(
                    set(mappable) & set(kwargs))
            )
        kwargs.update(mappable)
    return kwargs


def headline(text: str, align: bool = True) -> str:
    if align:
        return f"{text.title()}\n{'-' * len(text)}"
    else:
        return f" {text.title()} ".center(50, "o")


if __name__ == "__main__":
    print(headline("Python type checking", align=True))
    # Still evaluates to True
    print(headline("Python type checking", align="left"))
    # These are only hints, not enforced
    print(headline("Python type checking", align="center"))

    a = {1: 2, 3: 4}
    b = {10: 20, 11: 22}
    merge(a, b)

    play()
