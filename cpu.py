import random
from collections import Counter, defaultdict
from copy import deepcopy
from unittest.case import addModuleCleanup
from player import Player
from card import Card
from CommonFunctions import calculate_points, is_meld, is_run, powerset 

class CPU(Player):
    def __init__(self, cards_in_hand = [], cards_on_table = [], method = "suit", points = 0):
        Player.__init__(self, cards_in_hand, cards_on_table, method, points)
        self.pickup_map = {0: self.determine_best_pickup_greedy}
        self.points_map = {0: self.choose_cards_strategy_greedy}
        
    # greedy. Pick as many high card combinations as possible wihtout regard to points in other player's hand
    def pickup_options(self, tabled_cards, all_melds, all_runs, pickup_stratgety = 0): 
        if not tabled_cards:
            return "pile"
        # find best card(s) based on hand to pick from table
        # check if any cards on table can be added to tabled cards and cards in hand
        point_hands = []
        # try to make meld or run with potential hand and tabled cards to cards in hand
        potential_hand = self.cards_in_hand + tabled_cards
        all_hands = powerset(potential_hand)
        all_runs_in_hand = []
        for subset_hand in all_hands:
            if any(card in tabled_cards for card in subset_hand):
                if is_meld(subset_hand):
                    point_hands.append(subset_hand)
                elif is_run(subset_hand):
                    all_runs_in_hand.append(subset_hand)
                    point_hands.append(subset_hand)
        # try to make a meld with potential hand and tabled cards to cards on table
        all_melds = deepcopy(all_melds)
        for meld in all_melds:
            if len(meld) == 3:
                for card in tabled_cards:
                    temp_meld = deepcopy(meld)
                    temp_meld.append(card)
                    if is_meld(temp_meld):
                        point_hands.append(temp_meld)
        # try to make a run with potential hand and cards on table
        all_runs = deepcopy(all_runs)
        for run in all_runs:
            run += potential_hand
            all_possible_runs = powerset(run)
            for subset_hand in all_possible_runs:
                if any(card in subset_hand for card in tabled_cards):
                    if is_run(subset_hand):
                        point_hands.append(subset_hand)
        # check if cards on table already contains meld or run
        all_tabled_cards = powerset(tabled_cards)                       
        for subset_hand in all_tabled_cards:
            if is_meld(subset_hand) or is_run(subset_hand):
                point_hands.append(subset_hand)
        # remove duplicates while preserving order
        unique_best = list(set(tuple(hand) for hand in point_hands))
        strategy = self.pickup_map[pickup_stratgety]
        return "pile" if not unique_best else strategy(unique_best, tabled_cards)
    
    def determine_best_pickup_greedy(self, hand, cards_on_table):
        cards_on_table = deepcopy(cards_on_table)
        # reversed_cards_on_table = cards_on_table[::-1]
        flat_hand = [card for sub in hand for card in sub if card in cards_on_table]
        # get first instance of card on table from hand
        for card in cards_on_table:
            if card in flat_hand:
                return card
        return "pile"
        # options = list(flat_pick_from.intersection(cards_on_table))
        # if len(hand) == 1:
        #     new_card = options[0]
        #     return new_card
        # elif len(hand) > 1:
        #     # creates 2d list of cards on table to pick up
        #     new_pick_from = []
        #     for sub in hand:
        #         new_sub = tuple(card for card in sub if card in reversed_cards_on_table)
        #         new_pick_from.append(new_sub)
        #     # choose cards which require fewest cards picked up over all
        #     sub_count_d = {}
        #     for sub in new_pick_from:
        #         count = find = 0
        #         for card in reversed_cards_on_table:
        #             if card not in sub:
        #                 count += 1
        #             else:
        #                 find += 1
        #             if find >= len(sub):
        #                 sub_count_d[sub] = count
        #     best_sub = min(sub_count_d.keys(), key=(lambda k: sub_count_d[k]))
        #     for card in cards_on_table:
        #         if card in best_sub:
        #             return card
        # return "pile"
    
    # put down all points immediately with highest values
    def table_cards_strategy(self, hand, all_melds, all_runs, required_card = None, stratgey = 0):
        options = defaultdict(list) # points : identifier
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
                if is_run(subset_hand) and any(card in hand for card in temp_run):
                    options[subset_hand].append(run)
        if not options:
            return
        options_keys = list(options.keys())
        strategy = self.points_map[stratgey]
        # list of all point sets of cards to put down
        valid_options = strategy(options_keys, hand, required_card)
        options = {k:v for k, v in options.items() if k in valid_options}
        return options
    
    # chose highest. If tie choose randomly.
    def choose_cards_strategy_greedy(self, options, hand, required_card = None):
        # get powerset of indeces
        idx_list = [i for i in range(len(options))]
        idx_tups = powerset(idx_list)
        # get all options (but not necesarily the best or even possible ones)
        all_options = []
        for tup in idx_tups:
            option = [options[idx] for idx in tup]
            all_options.append(option)
        s = [str(card) for card in hand]
        # remove all impossible options (using same card multiple times) or doesn't contain required card
        options_after_removing_duplicates_or_no_required_card = []
        for option in all_options:
            s = [[str(card) for card in sub] for sub in option]
            flat = [num for comb in option for num in comb]
            if required_card and required_card not in flat:
                continue
            if len(set(flat)) == len(flat):
                options_after_removing_duplicates_or_no_required_card.append(option)
        # remove points involving cards not in hand
        options = options_after_removing_duplicates_or_no_required_card
        options_after_removing_joint_runs = []
        for option in options:
            sub_is_valid = True
            for sub in option:
                if not any(card in hand for card in sub):
                    sub_is_valid = False
            if sub_is_valid:
                options_after_removing_joint_runs.append(option)
        options = options_after_removing_joint_runs
        # maximize points
        best = []
        high = 0
        for option in options:
            points = 0
            for subset_hand in option:
                points += calculate_points(subset_hand)
            if points > high:
                high = points
                best = [option]
            elif points == high:
                best.append(option)         
        return None if not best else random.choice(best)
    
    # discard worst card based on number of similar cards
    def discard_strategy_greedy(self, cards_on_table, all_melds, all_runs):
        all_cards = cards_on_table + self.cards_in_hand
        for meld in all_melds:
            for card in meld:
                all_cards.append(card)
        for run in all_runs:
            for card in run:
                all_cards.append(card)
        all_cards = sorted(all_cards, reverse=True)
        all_suits = [card.suit for card in all_cards]
        all_ranks = [card.rank for card in all_cards]
        least_common_suits = [suit for suit, count in Counter(all_suits).most_common()[::-1]]
        least_common_ranks = [rank for rank, count in Counter(all_ranks).most_common()[::-1]]
        to_discard = []
        for rank in least_common_ranks:
            for suit in least_common_suits:
                to_discard.append(Card(rank, suit))
        for card in to_discard:
            if card in self.cards_in_hand:
                return card
        raise ValueError("No card was discarded!")