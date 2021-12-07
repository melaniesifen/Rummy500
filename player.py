from collections import defaultdict
from copy import deepcopy
from card import Card
from CommonFunctions import calculate_points, powerset, is_meld, is_run, sort_by
from CommonFunctions import sort_by as sort_by_module

class Player(object):
    
    def __init__(self, cards_in_hand = [], cards_on_table = [], method = "suit", points = 0):
        self.cards_in_hand = cards_in_hand
        self.cards_on_table = cards_on_table
        self.method = method
        self.points = points
        self.winner = False
     
    def set_winner(self):
        # switch
        self.winner = not self.winner
        
    def get_method(self):
        return self.method
    
    def set_method(self, method):
        if method == "suit" or method == "rank":
            self.method = method
        
    def get_cards_in_hand(self):
        paths = []
        for card in self.cards_in_hand:
            paths.append(card.image_path())
        return paths
    
    def get_cards_on_table(self):
        paths = []
        for card_list in self.cards_on_table:
            path_list = [card.small_image_path() for card in card_list]
            paths.append(path_list)
        return paths
        
    def pick(self, card):
        self.cards_in_hand.append(card)
    
    def discard(self, card):
        self.cards_in_hand.remove(card)
                
    def end_points(self):
        # cards_on_table = [card for points in self.cards_on_table for card in points]
        new_points = calculate_points(self.cards_on_table) - calculate_points(self.cards_in_hand)
        if self.winner:
            new_points += 25 # 25 points for winning the round
        self.points += new_points
        return new_points
    
    def round_winner(self):
        if not self.cards_in_hand:
            self.winner = True
        return self.winner
    
    def game_winner(self):
        if self.round_winner():
            cards_on_table = [card for points in self.cards_on_table for card in points]
            new_points = calculate_points(cards_on_table) + self.points + 25
            if new_points >= 500:
                return True
        return False
    
    def __str__(self):
        cards_in_hand = ' '.join(str(card) for card in self.cards_in_hand)
        return "Cards in hand: " + cards_in_hand
        
    def sort_by(self):
        self.cards_in_hand = sort_by_module(self.cards_in_hand, self.method)
        
    # put down all points immediately with highest values
    def all_valid_table_card_options(self, hand, all_melds, all_runs):
        options = defaultdict(list)
        hand = deepcopy(hand)
        all_hands = powerset(hand)
        # run or meld within hand
        all_runs_in_hand = []
        for subset_hand in all_hands:
            if is_meld(subset_hand):
                options[subset_hand].append(None)
            elif is_run(subset_hand):
                all_runs_in_hand.append(subset_hand)
                options[subset_hand].append(None)
        # points for all melds
        all_melds = deepcopy(all_melds)
        for meld in all_melds:
            if len(meld) == 3:
                for card in hand:
                    temp_meld = deepcopy(meld)
                    temp_meld.append(card)
                    if is_meld(temp_meld):
                        options[tuple(temp_meld)].append(meld)
        # points for all runs
        all_runs = deepcopy(all_runs)
        for run in all_runs:
            temp_run = run + hand
            all_possible_runs = powerset(temp_run)
            for subset_hand in all_possible_runs:
                if is_run(subset_hand):
                    options[subset_hand].append(run)
        return options