from itertools import chain, combinations
from operator import attrgetter
from card import Card

# returns powerset of list of items
def powerset(items_list):
    return chain.from_iterable(combinations(items_list, r) for r in range(1, len(items_list) + 1))

# takes hand of cards object and return sorted with preferred method
def sort_by(hand, method):
    if method == "suit":
        return sorted(hand, key=attrgetter('suit', 'rank'))
    return sorted(hand)
    
# bool: cards list is a run            
def is_run(subset_hand):
    # len of subset must be at least 3
    if len(subset_hand) < 3:
        return False
    # matching suits
    the_suit = subset_hand[0].suit
    for i in range(1, len(subset_hand)):
        if subset_hand[i].suit != the_suit:
            return False
    # rank is in order
    rank_sorted_subset_hand = sort_by(subset_hand, "rank")
    next_rank = rank_sorted_subset_hand[0].rank
    for i in range(1, len(subset_hand)):
        if rank_sorted_subset_hand[i].rank != next_rank + 1: 
            return False
        next_rank += 1
    return True

def is_meld(subset_hand):
    # subset must have 3 or 4 cards
    if len(subset_hand) < 3 or len(subset_hand) > 4:
        return False
    the_suit = subset_hand[0].suit
    for i in range(1, len(subset_hand)):
        if subset_hand[i].suit != the_suit:
            return False
    return True

def str_to_card(card):
    if type(card) == str:
        if card[0] == "J":
            card = Card(rank = 11, suit = card[1])
        elif card[0] == "Q":
            card = Card(rank = 12, suit = card[1])
        elif card[0] == "K":
            card = Card(rank = 13, suit = card[1])
        elif card[0] == "A":
            card = Card(rank = 14, suit = card[1])
        elif card[0] == "1" and card[1] == "0":
            card = Card(rank = 10, suit = card[2])
        else:
            card = Card(rank = int(card[0]), suit = card[1])
    return card
