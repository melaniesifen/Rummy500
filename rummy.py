import random
import itertools
from copy import deepcopy
import time
from CommonFunctions import _sort_by, is_run, is_meld, str_to_card
from card import Card
from deck import Deck
from player import Player
from cpu import CPU
from table import Table
    
class Rummy(object):
    # constructor
    def __init__(self, num_players = 2, players = [], round_number = 1):
        self.deck = Deck()
        self.deck.shuffle()
        self.num_players = num_players
        self.num_cards_in_hand = 10
        self.players = players
        self.all_tabled_cards = []
        self.round_number = round_number
        self.joint_runs = []
        self.all_melds = []
        
        # add players to game if there aren't any
        if self.round_number == 1:
            if self.num_players == 0:
                self.num_players == 2
                cpu1 = CPU([], [], method = "suit")
                self.players.append(cpu1)
                cpu2 = CPU([], [], method = "suit")
                self.players.append(cpu2)
            if self.num_players == 1:
                self.num_players = 2
                player = Player([], [], method = "suit")
                cpu = CPU([], [], method = "suit")
                self.players.append(player)
                self.players.append(cpu)
            else:
                for i in range(self.num_players):
                    player = Player([], [], method = "suit")
                    self.players.append(player)
        
        # deal the cards to the players
        for i in range(self.num_cards_in_hand):
            for player in self.players:
                player.cards_in_hand.append(self.deck.deal())
        
        # sort the hands of each player and print
        for i, player in enumerate(self.players):
            if self.round_number == 1 and type(player) == Player:
                while True:
                    method = input("For player " + str(i + 1) + " sort hands by rank or suit? \n")
                    if method != "rank" and method != "suit":
                        print("Invalid entry. Please type 'rank' or 'suit'.")
                        continue
                    break
                player.set_method(method)
                player.sort_by(player.cards_in_hand, player.method)
                print("Player " + str(i + 1) + " " + player.get_cards_in_hand())
                print()
            else:
                player.sort_by(player.cards_in_hand, player.method)
            
        # show first card of the deck  
        self.table = Table(self.deck, [])
            
    def get_all_tabled_cards(self):
        tabled_cards = deepcopy(self.all_tabled_cards)
        return tabled_cards
    
    def set_all_tabled_cards(self):
        for player in self.players:
            self.all_tabled_cards.append(player.cards_on_table)
            
    def get_all_joint_runs(self):
        all_cards = deepcopy(self.all_tabled_cards)
        joint_runs = deepcopy(self.joint_runs)
        cards_in_joint_runs = [card for sublist in joint_runs for card in sublist]
        for player_cards in all_cards:
            for points in player_cards:
                if is_run(points) and points not in joint_runs:
                    for card in points:
                        if card not in cards_in_joint_runs:
                            joint_runs.append(points)
                            cards_in_joint_runs = [card for sublist in joint_runs for card in sublist]                         
        self.joint_runs = joint_runs
        return joint_runs
    
    def get_all_melds(self):
        all_cards = deepcopy(self.all_tabled_cards)
        all_melds = deepcopy(self.all_melds)
        for player_cards in all_cards:
            for points in player_cards:
                if is_meld(points) and points not in all_melds:
                    all_melds.append(points)        
        self.all_melds = all_melds
        return all_melds
                   
    def pickup(self, player):
        is_valid_pick = False
        must_put_down_points = False
        # pick card
        if type(player) == Player:
            pick_from = input("Pick from pile or pick from table? ")
            while pick_from != "pile" and pick_from != "table":
                print("Invalid entry. Please choose 'pile' or 'table'. \n")
                pick_from = input()
        else:
            pick_from = player.pickup_strategy1(self.table.cards_on_table, self.all_melds, self.joint_runs)
            if type(pick_from) == list:
                best_cards = pick_from
                for subset_cards in best_cards:
                    for card in subset_cards:
                        if card in self.table.cards_on_table:
                            new_card = card
                            break
                pick_from = "table"
        
        if pick_from == "pile":
            # take card from table
            new_card = self.table.pickup_card_from_pile()
            # put card in player's hand
            player.pick(new_card)
            # sort new hand
            player.sort_by(player.cards_in_hand, player.method)
            is_valid_pick = True
            return (is_valid_pick, must_put_down_points)
            
        elif pick_from == "table":
            if type(player) == Player:
            # take card from table
                new_card = input("Choose a card from the table to pick up. ")
                cards_to_choose_from = [str(card) for card in self.table.cards_on_table]
                while len(new_card) > 3: # multiple entries
                    print("Pick only one card. Any cards in front of that card will go into your hand.")
                    new_card = input()
                while new_card not in cards_to_choose_from:
                    print("Invalid entry. You must choose a card that is already on the table.")
                    print("To pick from the pile instead, type: pile")
                    print("Otherwise, pick a card that is already on the table.")
                    new_card = input()
                    if new_card == "pile":
                        # take card from pile
                        new_card = self.table.pickup_card_from_pile()
                        # put card in player's hand
                        player.pick(new_card)
                        break
            else:
                new_card 
                
            # check that card is valid to pick up            
            def is_valid(subset_hand_objects):
                if is_meld(subset_hand_objects) or is_run(subset_hand_objects):
                    return True
                return False

            # take cards from table
            new_card = str_to_card(new_card)
            # take cards off the table
            old_cards = deepcopy(self.table.cards_on_table)
            new_cards = self.table.pickup_cards_on_table(new_card)
            # put cards in player's hand
            old_hand = deepcopy(player.cards_in_hand)
            for card in new_cards:
                player.pick(card)
                first_card = card
                                           
            # sort new hand
            player.cards_in_hand = _sort_by(None, player.cards_in_hand, player.method)            
            
            if type(player) == CPU:
                is_valid_pick = True
                if len(new_cards) > 1:
                    must_put_down_points = True
                return (is_valid_pick, must_put_down_points, first_card)
            
            # check every combination of cards in the player's hand
            potential_hand = player.cards_in_hand
            if len(new_cards) == 1:
                is_valid_pick = True
                player.cards_in_hand = potential_hand
                player.sort_by(player.cards_in_hand, player.method)
                return (is_valid_pick, must_put_down_points)

            for L in range(0, len(potential_hand) + 1):
                for subset_hand in itertools.combinations(potential_hand, L):
                    if first_card in subset_hand:
                        if is_valid(subset_hand):
                            is_valid_pick = True
                            player.cards_in_hand = potential_hand
                            player.sort_by(player.cards_in_hand, player.method)
                            must_put_down_points = True
                            return (is_valid_pick, must_put_down_points, first_card)
                      
            if not is_valid_pick:     
                # check every combination of cards on the table
                all_melds = deepcopy(self.get_all_melds())
                for points in all_melds:
                    points.append(first_card)
                    if is_valid(points):
                        is_valid_pick = True
                        break
                    
            if not is_valid_pick:
                # check if it can be added to existing joint runs            
                all_joint_runs = deepcopy(self.get_all_joint_runs())
                for run in all_joint_runs:
                    run.append(first_card)
                    if is_run(run):
                        is_valid_pick = True
                        break
                    
            if not is_valid_pick: 
                # put cards back on table
                self.table.cards_on_table = old_cards
                # remove cards from hand
                player.cards_in_hand = old_hand        
                return (is_valid_pick, must_put_down_points)
            else:
                must_put_down_points = True
                # sort new hand
                player.cards_in_hand = potential_hand
                player.sort_by(player.cards_in_hand, player.method)
                return (is_valid_pick, must_put_down_points, first_card)
            
        
    def discard(self, player):
        # have players discard
        if type(player) == Player:
            card = input("Choose a card in your hand to discard. ")
            cards_to_choose_from = [str(card) for card in player.cards_in_hand]
            while card not in cards_to_choose_from:
                print("Invalid entry. Please choose a card that is currently in your hand. \n")
                card = input()
        else:
            card = player.discard_strategy1(self.table.cards_on_table)
        # add card to table
        self.table.place_card_on_table(card)
        
        # remove card from player's hand
        card = str_to_card(card)
        player.discard(card)
        player.sort_by(player.cards_in_hand, player.method)
    
    
    def table_cards(self, player, required_card, index):
        if type(player) == CPU:
            combinations = player.table_cards_strategy1()
            if len(combinations) <= 0 or len(combinations) <= index:
                return "no"
            cards_objects = combinations[index]
            cards_objects = [card for card in cards_objects] # tuple to list
            cards = [str(card) for card in cards_objects]
        else:
            cards = input("Choose cards to place on table for points. Separate by commas. ")
            cards = cards.strip()
            cards = cards.split(', ')
            cards_to_choose_from = [str(card) for card in player.cards_in_hand]
            # cards chosen must be in hand and must include required card if one exists
            while (not set(cards).issubset(set(cards_to_choose_from))) or (required_card and str(required_card) not in cards):
                if required_card and (str(required_card) not in cards):
                    print("You must use ", str(required_card), ". Try again \n")
                    cards = input()
                    continue
                print("Invalid entry. Please choose cards that are currently in your hand. \n")
                if not required_card:
                    print("If you don't have any cards to put down type 'no'.")
                cards = input()
                if cards == "no" and not required_card:
                    return "no"
                cards = cards.strip()
                cards = cards.split(', ')
        
            # cards is list of str(cards), cards_objects is list of cards 
            cards_objects = []
            for card in cards:
                card = str_to_card(card)
                cards_objects.append(card)
         
        def is_going_to_tabled_cards(subset_hand): 
            if len(subset_hand) > 2:
                return False
            # check every combination of cards on the table
            options = []
            potential_points = []
            
            all_melds = deepcopy(self.get_all_melds())
            for points in all_melds:
                old_points = deepcopy(points)
                points += subset_hand
                if is_meld(points):
                    options.append(old_points)
                    potential_points.append(points)
                        
            # check if it can be added to existing joint runs            
            all_joint_runs = deepcopy(self.get_all_joint_runs())
            for run in all_joint_runs:
                old_run = deepcopy(run)
                run += subset_hand
                if is_run(run):
                    options.append(old_run)
                    potential_points.append(run)
                    
            if len(options) > 0:
                return (options, potential_points)
            
            return False
        
        def is_valid(subset_hand, subset_hand_objects):
            if len(set(subset_hand)) != len(subset_hand): # repeated card
                print("Invalid. Cards cannot be repeated")
                return False
            if is_meld(subset_hand_objects) or is_run(subset_hand_objects):
                return True
            valid_options = is_going_to_tabled_cards(subset_hand_objects)
            if valid_options == False:
                return False
            else:
                options = valid_options[0]
                potential_points = valid_options[1]
                return (options, potential_points)
            
        check = is_valid(cards, cards_objects)
        if check != False:
            if type(check) == tuple:
                options = check[0]
                potential_points = check[1]
                options_list_str = [[str(card) for card in sublist] for sublist in options]
                if type(player) == Player:
                    if len(options_list_str) > 1:
                        print("Options to add points to: ")
                        for i, option in enumerate(options_list_str):
                            print(i + 1, ": ", option)
                        ask_again = True
                        while ask_again:
                            choice = input("Which set are you adding this point card to? Select the number. ")
                            try:
                                choice = int(choice)
                                check_potential_points_range = potential_points[choice - 1]
                                check_options_range = options[choice - 1]
                                if choice == 0:
                                    print("Invalid seletion. Try again.")
                                else:
                                    ask_again = False
                            except:
                                print("Select the number next to the option you would like to choose.")
                    else:
                        choice = 1
                else:
                    # strategy1
                    choice = player.choose_cards_strategy1(potential_points)
                # if run then add to all runs
                if is_run(potential_points[choice - 1]):
                    self.joint_runs.remove(options[choice - 1])
                    self.joint_runs.append(potential_points[choice - 1])
                # if meld then add to all melds
                elif is_meld(potential_points[choice - 1]):
                    self.all_melds.remove(options[choice - 1])
                    self.all_melds.append(potential_points[choice - 1])
            # place cards into player's cards on table
            cards_to_keep = []
            point_list = []
            for card in cards_objects:
                point_list.append(card)
            # sort the cards before putting on table
            point_list = sorted(point_list)
            player.cards_on_table.append(point_list)
            # remove cards from player's hand
            for card in player.cards_in_hand:
                if card not in cards_objects:
                    cards_to_keep.append(card)
            player.cards_in_hand = cards_to_keep
            player.sort_by(player.cards_in_hand, player.method)
            # Update all cards on table
            self.set_all_tabled_cards()
            return True
        else:
            return False
     
    def get_points(self, player, must_put_down_points, required_card):
        index = 0
        if not must_put_down_points and type(player) == Player:
            ask = input("Do you want to put down point cards? ")
            while ask != "yes" and ask != "no":
                print("Invalid entry. Please answer 'yes' or 'no'. \n")
                ask = input()
        elif type(player) == CPU:
            ask = "yes" # strategy1
        else:
            ask = "yes"
            
        if ask == "yes": 
            multiple = True
            while multiple:
                # table cards
                cards_tabled = self.table_cards(player, required_card, index)
                if cards_tabled == True and player.win_round():
                    multiple = False
                    return True
                if cards_tabled == False and must_put_down_points == False: # cards chosen incorrectly
                    if type(player) == CPU:
                        index += 1
                        ask = "yes" # strategy1
                    else:
                        ask = input("Invalid selection. Try again? ")
                        while ask != "yes" and ask != "no":
                            print("Invalid entry. Please answer 'yes' or 'no'. \n")
                            ask = input()
                        if ask == "no":
                            multiple = False
                elif cards_tabled == False and must_put_down_points: # cards chosen incorrectly but must point down points
                    if type(player) == Player:
                        print("Invalid selection. Try again.")
                    else:
                        index += 1
                elif cards_tabled == "no":
                    multiple = False
                else:
                    required_card = None
                    if type(player) == Player:
                        ask = input("Do you have another set of cards to put down for points? \n")
                        while ask != "yes" and ask != "no":
                            print("Invalid entry. Please answer 'yes' or 'no'. \n")
                            ask = input()
                        if ask == "no":
                            multiple = False
                    else:
                        index += 1
        return False
         
 
    # simulate the play of rummy
    def play(self):
        winner = None
        for i, player in enumerate(self.players):
            # show cards
            print("PLAYER", i + 1)
            print(player.get_cards_in_hand())
            print(player.get_cards_on_table())
            print(str(self.table))
            print()
            
            # pick card
            pickup = self.pickup(player)
            valid_pickup = pickup[0]
            must_put_down_points = pickup[1]
            required_card = None
            if len(pickup) == 3:
                required_card = pickup[2]
            while not valid_pickup:
                print("Invalid selection. Try again.")
                print()
                valid_pickup = self.pickup(player)
            print(player.get_cards_in_hand())
            print(player.get_cards_on_table())
            print()
            
            # get points
            is_winner = self.get_points(player, must_put_down_points, required_card)
            if is_winner:
                winner = i + 1
                return winner
            
            print(player.get_cards_in_hand())
            print(player.get_cards_on_table())
            print(str(self.table))
            print()
            
            # discard
            self.discard(player)
            if player.win_round():
                winner = i + 1
                return winner

            print(player.get_cards_in_hand())
            print(player.get_cards_on_table())
            print()
            
        return winner
    
    def get_all_points(self):
        player_points = {}
        for i, player in enumerate(self.players):
            player_points[i] = player.end_points()
        return player_points
    
    def is_game_winner(self, player_points):
        to_win = 500
        winners = [player for player, points in player_points.items() if points == max(player_points.values()) and points >= to_win]
        return winners
            
    def play_to_win(self):
        round_winner = None
        game_winner = None
        while not round_winner:
            round_winner = self.play()
            if round_winner:
                # set winning player as winner
                winning_player = self.players[round_winner - 1]
                winning_player.set_winner()
                # get each player's points
                player_points = self.get_all_points()
                # check if anyone has 500 points
                game_winner = self.is_game_winner(player_points)
                if not game_winner:
                    print()
                    print("Winner of round ", self.round_number, " is Player ", round_winner, " !")
                    for i, player in enumerate(self.players):
                        print("Player ", i + 1, "'s points: ", player.points)
                    print()
                    print()
                    print("Next round!")
                    print()
                    self.round_number += 1
                    round_winner = True
                    winning_player.set_winner() # reset winning status
                elif len(game_winner) == 1:
                    print("Winner is: player ", game_winner[0] + 1)
                    round_winner = True
                    game_winner = True
                else:
                    winner_s = ""
                    for player in game_winner:
                        player += 1
                        winner_s = ", ".join(str(player)) 
                    print("Winners are: ", winner_s, "!")
                    round_winner = True
                    game_winner = True
        if not game_winner:
            # set up next round
            num_players = self.num_players
            players = []
            for i, player in enumerate(self.players):
                if type(player) == Player:
                    players.append(Player([], [], player.method, player.points))
                else:
                    players.append(CPU([], [], player.method, player.points))
            self = Rummy(num_players, players, self.round_number)
            self.play_to_win()
                
                
                
            
def main():
    # prompt the user to enter the number of plaers
    num_players = int (input ('Enter number of players: '))
    while (num_players > 4 or num_players < 0):
        num_players = int (input ('Enter number of players: '))

    # create the Poker object
    game = Rummy(num_players)

    # play the game
    game.play_to_win()
    
start_time = time.time()
main()
#print("--- %s seconds ---" % (time.time() - start_time))

