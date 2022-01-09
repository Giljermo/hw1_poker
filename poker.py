#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------
import itertools
from copy import copy

int_ranks = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    return sorted([int_ranks[rank] for rank, _ in hand], reverse=True)


def flush(hand):
    """Возвращает True, если все карты одной масти"""
    return len({suit for _, suit in hand}) == 1


def straight(ranks):
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    min_rank = ranks[0]
    it_ranks = itertools.count(min_rank, step=-1)
    new_ranks = [it_ranks.__next__() for i in range(5)]
    return new_ranks == ranks


def kind(n, ranks):
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    for rank in ranks:
        if ranks.count(rank) == n:
            return rank


def two_pair(ranks):
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    ranks_copy = copy(ranks)
    rank1 = kind(2, ranks_copy)
    if rank1:
        ranks_copy.remove(rank1)
        rank2 = kind(2, ranks_copy)
        if rank2:
            return max(rank1, rank2), min(rank1, rank2)


def get_cards(suits):
    """получить возожные карты для замены джокера"""
    return [rank + suit for rank in int_ranks for suit in suits]


def get_replaced_hand(joker, suits, hand):
    """получить все возможные вариации руки после замены джокера"""
    hands = []
    if joker in hand:
        for card in get_cards(suits):
            if card not in hand:  # в колоде не может быть двух один. карт
                hand_copy = hand.copy()
                hand_copy.remove(joker)
                hand_copy.append(card)
                hands.append(hand_copy)
    return hands or [hand]


def get_combinations_without_joker(hand):
    """
    получить все вариации руки после замены всех джокеров,
    вернуть исходную руку если джокеры отсутсвут
    """
    hands_copy = get_replaced_hand('?B', 'SC', hand).copy()
    hands = []
    while hands_copy:
        hands += get_replaced_hand('?R', 'HD', hands_copy.pop())

    return hands or hand


def _best_hand(hands):
    best_scope = 0,
    best_hand_ = None
    for hand_ in hands:
        scope = hand_rank(hand_)
        if scope > best_scope:
            best_scope = scope
            best_hand_ = hand_
    return best_hand_


def best_hand(hand):
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    hands = itertools.combinations(hand, 5)
    return _best_hand(hands)


def best_wild_hand(hand):
    """best_hand но с джокерами"""
    hands = []
    for combination in get_combinations_without_joker(hand):
        hands += list(itertools.combinations(combination, 5))
    return _best_hand(hands)


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split())) == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split())) == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split())) == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split())) == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split())) == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split())) == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
