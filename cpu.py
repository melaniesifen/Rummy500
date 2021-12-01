import itertools
import random
from collections import Counter
from copy import deepcopy
from player import Player
from CommonFunctions import is_meld, is_run, powerset

class CPU(Player):   
    # greedy. Pick as many high card combinations as possible wihtout regard to points in other player's hand
    def pickup_strategy1(self, tabled_cards, all_melds, all_runs): 
        if not tabled_cards:
            return "pile"
        # find best card(s) based on hand to pick from table
        # check if any cards on table can be added to tabled cards
        point_hands = []    
        all_melds = deepcopy(all_melds)
        for meld in all_melds:
            if len(meld) == 3:
                for card in tabled_cards:
                    meld.append(card)
                    if is_meld(meld):
                        point_hands.append(meld)
                    meld.pop()        
        all_runs = deepcopy(all_runs)
        for run in all_runs:
            run += tabled_cards
            all_subsets = powerset(run)
            for subset_hand in all_subsets:
                if any(card in subset_hand for card in tabled_cards):
                    if is_run(subset_hand):
                        point_hands.append(subset_hand)
        
        # check if cards on table already contains meld or run
        all_tabled_cards = powerset(tabled_cards)                          
        for subset_hand in all_tabled_cards:
            if is_meld(subset_hand) or is_run(subset_hand):
                point_hands.append(subset_hand)
        
        # remove duplicates while preserving order
        seen = set()
        for sublist in point_hands:
            seen.append(sublist)
        unique_best = [sublist for sublist in point_hands if sublist not in seen]
        if unique_best:
            return unique_best
        return "pile"
    
    # put down all points immediately with highest values
    def table_cards_strategy1(self):
        combinations = []
        for L in range(len(self.cards_in_hand) + 1):
            for subset_hand in itertools.combinations(self.cards_in_hand, L):
                if subset_hand:
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
                best = [hand]
            elif points == high:
                best.append(hand)
                
        choices = [i for i in range(1, len(best) + 1)]
        return random.choice(choices)
    
    # discard worst card based on number of similar cards
    # If tie then based on points
    # remove Aces if not good at the time
    def discard_strategy1(self, tabled_cards):
        tabled_cards = deepcopy(tabled_cards)
        suits = [card.suit for card in tabled_cards if card.rank < 10]
        if not suits:
            suits = [card.suit for card in tabled_cards if 10 <= card.rank < 14]
        if not suits:
            suits = [card.suit for card in tabled_cards if card.rank == 14]
        ranks = [card.rank for card in tabled_cards if card.rank < 10]
        if not ranks:
            ranks = [card.rank for card in tabled_cards if 10 <= card.rank < 14]
        if not ranks:
            ranks = [card.rank for card in tabled_cards if card.rank == 14]
        count_suits = Counter(suits)
        least_common_suit = count_suits.most_common()[-1]
        count_ranks = Counter(ranks)
        least_common_rank = count_ranks.most_common()[-1]
        while count_suits and count_ranks:
            for card in tabled_cards:
                if card.rank == least_common_rank and card.suit == least_common_suit:
                    return card
            
            
            
        # 2s, 3s, 5s, 6d, 8h, 8d, jc, jh
        # s = {s:3, d:2, h:1}
        # least_s = h
        # r = {2:1, 3:1, 5:1, 6:1, 8:2}
        # least_r = 5
        
        
        
        
        
        
        
    def discard_strategy1(self, table_cards):
        # check in hand - there should be no point subsets
        worst_ranks = []
        ranks = [card.rank for card in self.cards_in_hand]
        count_dict = {rank:ranks.count(rank) for rank in ranks}
        min_rank_count = [rank for rank, count in count_dict.items() if count == 1]
        min_rank_count.sort()
        for rank in min_rank_count:
            if rank < 10:
                worst_ranks += [card for card in self.cards_in_hand if card.rank == rank]
            elif 10 <= rank < 14 and not worst_ranks:
                worst_ranks += [card for card in self.cards_in_hand if card.rank == rank]
            elif rank == 14 and not worst_ranks:
                worst_ranks += [card for card in self.cards_in_hand if card.rank == rank]
                     
        worst_suits = []     
        suits = [card.suit for card in self.cards_in_hand]
        count_dict = {suit:suits.count(suit) for suit in suits}
        min_suit_count = [suit for suit, count in count_dict.items() if count == 1]
        for suit in min_suit_count:
            worst_suits += [card for card in self.cards_in_hand if card.suit == suit and card.rank < 10]
            if not worst_suits:
                worst_suits += [card for card in self.cards_in_hand if card.suit == suit and 10 <= card.rank < 14]
            if not worst_suits:
                worst_suits += [card for card in self.cards_in_hand if card.suit == suit and card.rank == 14]
                
        # 2s, 3s, 5s, 6d, 8h, 8d, jc, jh
        # worst rank = [2, 3, 4, 5, 6]
        # worst suit = [c]
        
            
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
                
                    
                
                
            
        
            
            
        
    
        
        
        
            
            
            
            
        
        
        