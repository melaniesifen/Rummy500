import itertools
import random
from copy import deepcopy
from card import Card
from player import Player
from CommonFunctions import _sort_by, str_to_card, is_meld, is_run

class CPU(Player):
    # def __init__(self, cards_in_hand, cards_on_table, method = "suit", points = 0):
    #     self.cards_in_hand = cards_in_hand
    #     self.cards_on_table = cards_on_table
    #     self.method = method
    #     self.points = points
    #     self.winner = False
    
    # greedy. Pick as many high card combinations as possible wihtout regard to points in other player's hand
    def pickup_strategy1(self, table_cards, all_melds, all_runs): 
        if len(table_cards) == 0:
            return "pile"
        # find best card(s) based on hand to pick from table
        best = []
        high = 0
        cards_in_hand = deepcopy(self.cards_in_hand)
        cards_in_hand += table_cards
        for L in range(0, len(cards_in_hand) + 1):
            for subset_hand in itertools.combinations(cards_in_hand, L):
                for card in subset_hand:
                    if card in table_cards and (is_meld(subset_hand) or is_run(subset_hand)):
                        # count points
                        points = self.calculate_points(subset_hand)
                        if points > high:
                            high = points
                            subset_hand = list(subset_hand)
                            best = []
                            best.append(subset_hand)
                        elif points == high:
                            best.append(subset_hand)
        
        if len(all_melds) != 0:
            all_melds = deepcopy(all_melds)
            for meld in all_melds:
                for card in table_cards:
                    meld.append(card)
                    if is_meld(meld):
                        points = self.calculate_points(meld)
                        if points > high:
                            high = points
                            best = []
                            best.append(meld)
                        elif points == high:
                            best.append(meld)
                    meld.remove(card)
                            
        if len(all_runs) != 0:
            all_runs = deepcopy(all_runs)
            
            for run in all_runs:
                run += table_cards
                for L in range(0, len(run) + 1):
                    for subset_hand in itertools.combinations(run, L):
                        for card in subset_hand:
                            if card in table_cards and is_run(subset_hand):
                                # count points
                                points = self.calculate_points(subset_hand)
                                if points > high:
                                    high = points
                                    best = []
                                    best.append(subset_hand)
                                elif points == high:
                                    best.append(subset_hand)
        
        # check cards on table                            
        for L in range(0, len(table_cards) + 1):
            for subset_hand in itertools.combinations(table_cards, L):
                if is_meld(subset_hand) or is_run(subset_hand):
                    # count points
                    points = self.calculate_points(subset_hand)
                    if points > high:
                        high = points
                        subset_hand = list(subset_hand)
                        best = []
                        best.append(subset_hand)
                    elif points == high:
                        best.append(subset_hand)
                                
        if len(best) > 0:
            return best
        return "pile"
    
    # put down all points immediately with highest values
    def table_cards_strategy1(self):
        combinations = []
        for L in range(0, len(self.cards_in_hand) + 1):
            for subset_hand in itertools.combinations(self.cards_in_hand, L):
                if len(subset_hand) > 0:
                    combinations.append(subset_hand)

        return combinations
    
    # chose highest. If tie choose randomly.
    def choose_cards_strategy1(self, potential_hand):
        if len(potential_hand) == 1:
            return 1
        best = []
        high = 0
        for hand in potential_hand:
            points = self.calculate_points(hand)
            if points > high:
                high = points
                best = []
                best.append(hand)
            elif points == high:
                best.append(hand)
                
        choices = [i for i in range(1, len(best) + 1)]
        return random.choice(choices)
    
    # discard worst card based on number of similar cards
    # If tie then based on points
    # remove Aces if not good at the time
    def discard_strategy1(self, table_cards):
        # check in hand - there should be no point subsets
        worst_card = []
        
        ranks = [card.rank for card in self.cards_in_hand]
        count_dict = {rank:ranks.count(rank) for rank in ranks}
        min_rank_count = [rank for rank, count in count_dict.items() if count == 1]
        if len(min_rank_count) > 0:
            for rank in min_rank_count:
                if rank < 10:
                    for card in self.cards_in_hand:
                        if card.rank == rank:
                            worst_card.append(card)
                            break
                    break
                elif rank >= 10 and rank < 14 and len(worst_card) == 0:
                    for card in self.cards_in_hand:
                        if card.rank == rank:
                            worst_card.append(card)
                            break
                    break
                elif rank == 14 and len(worst_card) == 0:
                    for card in self.cards_in_hand:
                        if card.rank == rank:
                            worst_card.append(card)
                            break
                        
        worst_suits = []     
        suits = [card.suit for card in self.cards_in_hand]
        count_dict = {suit:suits.count(suit) for suit in suits}
        min_suit_count = [suit for suit, count in count_dict.items() if count == 1]
        if len(min_suit_count) > 0:
            for suit in min_suit_count:
                for card in self.cards_in_hand:
                    if card.suit == suit and card.rank < 10:
                        worst_suits.append(card)
                if len(worst_suits) == 0:
                    for card in self.cards_in_hand:
                        if card.suit == suit and card.rank < 14:
                            worst_suits.append(card)
                if len(worst_suits) == 0:
                    for card in self.cards_in_hand:
                        if card.suit == suit and card.rank == 14:
                            worst_suits.append(card)
            min_rank = 15
            for card in worst_suits:
                if card.rank < min_rank:
                    min_rank = card.rank
                elif card.rank == min_rank:
                    min_rank -= 1
            for card in worst_suits:
                if card.rank == min_rank:
                    worst_card.append(card)
            
        if len(worst_card) > 0:
            low = 10
            worst_card_rank_suit = [card for card in worst_card if card.rank < low]
            if len(worst_card_rank_suit) > 0:
                return random.choice(worst_card_rank_suit)
            else:
                low = 14
                worst_card_rank_suit = [card for card in worst_card if card.rank < low]
                if len(worst_card_rank_suit) > 0:
                    return random.choice(worst_card_rank_suit)
                else:
                    return worst_card[0]
                    
        # TODO: CHECK FOR ALMOST MELDS
        return random.choice(self.cards_in_hand)
                
                    
                
                
            
        
            
            
        
    
        
        
        
            
            
            
            
        
        
        