import itertools
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
        cards_on_table = deepcopy(self.cards_on_table)
        cards_in_hand += table_cards
        for L in range(0, len(cards_in_hand) + 1):
            for subset_hand in itertools.combinations(cards_in_hand, L):
                for card in subset_hand:
                    if card in table_cards and (is_meld(subset_hand) or is_run(subset_hand)):
                        # count points
                        points = self.calculate_points(subset_hand)
                        if points > high:
                            high = points
                            best = subset_hand
                        elif points == high:
                            best.append(subset_hand)
        
        if len(all_melds) != 0:
            all_melds = deepcopy(all_melds)
            for meld in all_melds:
                for card in table_cards:
                    meld += card
                    if is_meld(meld):
                        points = self.calculate_points(meld)
                        if point > high:
                            high = points
                            best = meld
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
                                    best = subset_hand
                                elif points == high:
                                    best.append(subset_hand)
                                
        if len(best) > 0:
            return best
        return "pile"
        
            
            
            
            
        
        
        