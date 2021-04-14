from math import floor
import random
import itertools
from copy import deepcopy
import time
import gc
from tkinter import *
import tkinter.messagebox
from CommonFunctions import _sort_by, is_run, is_meld, str_to_card
from card import Card
from deck import Deck
from player import Player
from cpu import CPU
from table import Table

global immortals
immortals = {}   
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
        
        self.player_frame = Frame(gui, width=1000, height=300)
        self.player_frame.pack(side="bottom", fill="x")
        self.player_frame.configure(bg='SpringGreen3')
        
        self.other_frame = Frame(gui, width=1000, height=500)
        self.other_frame.pack(side="top", fill="x", expand=True)
        self.other_frame.configure(bg='SpringGreen3')  
        
        self.sort_method = Button(self.player_frame, state="disable", text="suit", command=lambda:set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = True, player = self.players[0]), highlightbackground = "red4", bg="red2", bd=4, font=("Courier", 12))
        self.sort_method.place(relx=0.1, rely=0.9, anchor=CENTER)
        
        self.deck_image = PhotoImage(file="images/deck.png")
        self.deck_image.image = self.deck_image
        immortals[self.deck_image] = self.deck_image
        
        self.deck_button = Button(self.other_frame, image=self.deck_image, state="disable", highlightthickness = 0, bd = 0,\
            command=lambda:[self.deck_button.configure(state="disable"), \
            self.deck_label.place(relx=0.1, rely=0.85, anchor=CENTER), \
            change_state_on_table(self.other_frame, self.table), \
            self.pickup(self.players[0], "pile"), \
            self.change_state_in_hand(), \
            self.select_button.place(relx=0.07, rely=0.72), \
            self.discard_button.place(relx=0.07, rely=0.60)])
        self.deck_button.place(relx=0.1, rely=0.85, anchor=CENTER)
      
        self.deck_label = Label(self.other_frame, image=self.deck_image, highlightthickness = 0, bd = 0)
        self.deck_label.place(relx=0.1, rely=0.85, anchor=CENTER)
        
        self.back_card = PhotoImage(file="images/card_back.png")
        self.back_card.image = self.back_card
        
        self.select_button = Button(self.player_frame, text="select", highlightbackground = "red4", bg="red2", font=("Courier", 12), state="disabled", bd=4)
        self.discard_button = Button(self.player_frame, text="discard", highlightbackground = "red4", bg="red2", font=("Courier", 12), state="disabled", bd=4)
        
        # add players to game if there aren't any
        if self.round_number == 1:
            if self.num_players == 0:
                self.num_players == 2
                cpu1 = CPU([], [], method = "suit")
                self.players.append(cpu1)
                cpu2 = CPU([], [], method = "suit")
                self.players.append(cpu2)
            elif self.num_players == 1:
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
         
        self.sort_method.configure(state = "normal")       
        self.back_card_labels = []        
        #sort the hands of each player and print
        for i, player in enumerate(self.players):
            if type(player) == Player:
                set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = False, player = player)
            else:
                num_cards = len(player.cards_in_hand)
                for i, card in enumerate(player.cards_in_hand):
                    x = 0.2 + (i + 1)/(num_cards * 2.3)
                    label = Label(self.other_frame, image=self.back_card, highlightbackground = "black")
                    self.back_card_labels.append(label)
                    label.place(relx=x, rely=0.2, anchor=CENTER)
                    
                    
        # show first card of the deck  
        self.table = Table(self.deck, [])
        global first_card
        first_card = self.table.cards_in_pile.deal()
        self.table.place_card_on_table(first_card)
        first_card_path = first_card.image_path()
        first_card = PhotoImage(file=first_card_path)
        first_card.image = first_card
        first_card_button = Button(self.other_frame, image=first_card, state="disable", highlightthickness = 0, bd = 0, command=lambda:pickup(self.players[0], "table")).place(relx=0.2, rely=0.85, anchor=CENTER)
        first_card_label = Label(self.other_frame, image=first_card, highlightthickness = 0, bd = 0).place(relx=0.2, rely=0.85, anchor=CENTER)
        
            
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
                
    def pickup(self, player, pick_from=None):
        is_valid_pick = False
        must_put_down_points = False
        # pick card
        if type(player) == CPU:
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
            if type(player) == Player:
                set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked=False, player=player)
            is_valid_pick = True
            return (is_valid_pick, must_put_down_points)
            
        elif pick_from == "table":
            if type(player) == CPU:
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
                set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked=False, player=player)
                return

            for L in range(0, len(potential_hand) + 1):
                for subset_hand in itertools.combinations(potential_hand, L):
                    if first_card in subset_hand:
                        if is_valid(subset_hand):
                            is_valid_pick = True
                            player.cards_in_hand = potential_hand
                            player.sort_by(player.cards_in_hand, player.method)
                            must_put_down_points = True
                            set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked=False, player=player)
                            return
                    
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
            else:
                must_put_down_points = True
                # sort new hand
                player.cards_in_hand = potential_hand
                player.sort_by(player.cards_in_hand, player.method)
                set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked=False, player=player)
                return
        
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
            # pick card
            if type(player) == Player:
                # enable button
                self.deck_button.configure(state="normal")
                # remove label
                self.deck_label.place_forget()
            else:
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
            
            #     # get points
            #     is_winner = self.get_points(player, must_put_down_points, required_card)
            #     if is_winner:
            #         winner = i + 1
            #         return winner
                
            #     print(player.get_cards_in_hand())
            #     print(player.get_cards_on_table())
            #     print(str(self.table))
            #     print()
                
            #     # discard
            #     self.discard(player)
            #     if player.win_round():
            #         winner = i + 1
            #         return winner

            #     print(player.get_cards_in_hand())
            #     print(player.get_cards_on_table())
            #     print()
            
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
            
            
    def events(self):
        """
        # current:
        # deck disabled with label on top
        # cards in hand disabled with label on top
        # cards on table disabled with label on top
        
        # player picks card:
        # only enable deck button and cards on table
        """
        keep = self.back_card_labels
        for widget in self.other_frame.winfo_children():
            if type(widget).__name__ == "Button":
                keep.append(widget)
                widget.configure(state = "normal")
        clear_frame(self.other_frame, keep = keep)
        """
        # deck button:
        # disable deck button and replace label
        # disable cards on table buttons and replace labels
        # put card in hand
        # enable cards in hand as buttons to put down points
        """
        #   cards in hands button:
        #   have a select button appear
        
        #       select (point down points?) button:
        #       trigger to check which cards and see if valid placement
        #       if cards are valid then place on point space, else pop up invalid selection     

        #       drag card to table to discard
        #       forget select button
        #       disable cards in hand buttons
        #       replace labels
        #       check for winners
        #       if no winners then do cpu turn
        #       check for winners
        #       if no winners then enable deck button and card buttons (rinse, wash, repeat)
        
        # card on table button:
        # check if card is valid for pickup
        # if valid for pickup then:
        # disable deck button and repleace label
        # disable cards on table buttons and replace labels
        # enable cards in hand as buttons to put down points
        # allow drag and drop
        
        #   cards in hands button:
        #   have a select button appear
        
        #       select (point down points?) button:
        #       if card must be used then keep it selected until it is on the table
        #       trigger to check which cards and see if valid placement
        #       if cards are valid then place on point space, else pop up invalid selection 
        
        #       drag card to table to discard
        #       forget select button
        #       disable cards in hand buttons
        #       replace labels
        #       check for winners
        #       if no winners then do cpu turn
        #       check for winners
        #       if no winners then enable deck button and card buttons (rinse, wash, repeat)
    def change_state_in_hand(self):
        for widget in self.player_frame.winfo_children():
            if type(widget).__name__ == "Label":
                widget.lower()
            if type(widget).__name__ == "Button":
                widget.configure(state = "normal")


def create_cpu_game(num_players):
    tkinter.messagebox.showinfo("", "This feature is not yet available")
    
def create_game(num_players):
    game = Rummy(num_players)
    #game.play_to_win()
    game.events()

def destroy_frame(frame):
    # destroy all widgets from frame
    for widget in frame.winfo_children():
       widget.destroy()
    
    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    frame.pack_forget()
    
def clear_frame(frame, keep = []):
    for widget in frame.winfo_children():
        if widget in keep:
            continue
        widget.place_forget()

def change_state_on_table(frame, table):
    for widget in frame.winfo_children():
        if type(widget).__name__ == "Button":
            widget.configure(state = "disable")
    paths = table.get_cards_on_table() # list of image paths
    for i, card in enumerate(table.cards_on_table):
        path = paths[i]
        card_image = PhotoImage(file=path)
        card_image.image = card_image
        x = 0.2 + (i)/(len(paths) * 2)
        label = Label(frame, image=card_image, highlightthickness = 0, bd = 0)
        label.place(relx=x, rely=0.85, anchor=CENTER)

def set_sorting_method(bn, frame, clicked = True, player = None):
    gc.disable()
    sort_method = bn[0]
    if clicked:
        if sort_method["text"] == "suit":
            sort_method.configure(text="rank")
            player.set_method("rank")
            player.sort_by(player.cards_in_hand, player.method)
        else:
            sort_method.configure(text="suit")
            player.set_method("suit")
            player.sort_by(player.cards_in_hand, player.method)
        
    paths = player.get_cards_in_hand() # list of image paths
    clear_frame(frame, keep = bn)
    for i, card in enumerate(player.cards_in_hand):
        path = paths[i]
        card_image = PhotoImage(file=path)
        card_image.image = card_image
        x = 0.2 + (i + 1)/(len(paths) * 2)
        button = Button(frame, image=card_image, highlightthickness = 0, bd = 0, state="disable").place(relx=x, rely=0.8, anchor=CENTER)
        label = Label(frame, image=card_image, highlightthickness = 0, bd = 0).place(relx=x, rely=0.8, anchor=CENTER)
    gc.enable()
        
def make_draggable(frame):
    for widget in frame.winfo_children():
        if type(widget).__name__ == "Button":
            widget.bind("<Button-1>", on_drag_start)
            widget.bind("<B1-Motion>", on_drag_motion)

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

def main():
    global gui
    gui = Tk(className='Python Examples - Window Size')# set window size and color
    gui.bind('<Escape>', lambda event: gui.state('normal'))
    gui.bind('<F11>', lambda event: gui.state('zoomed'))
    gui.configure(bg='SpringGreen3')
    gui.geometry("800x1000")
    
    # set up game
    frame1 = Frame(gui)
    frame1.pack(side="top", expand=True, fill="both")
    frame1.configure(bg='SpringGreen3')

    frame1.choice_label = Label(frame1, text="Choose your game:", font=("Courier", 30), bg="SpringGreen3").place(relx=0.5, rely=0.25, anchor=CENTER)
    frame1.cpu_button = Button(frame1, text="CPU v CPU", font=("Courier", 15), command=lambda:create_cpu_game(0)).place(relx=0.5, rely=0.6, anchor=CENTER)
    frame1.player_button = Button(frame1, text="Player v CPU", font=("Courier", 15), command=lambda:[destroy_frame(frame1), create_game(1)]).place(relx=0.5, rely=0.45, anchor=CENTER)
    frame1.players_button = Button(frame1, text="Multiplayer", font=("Courier", 15), command=lambda:create_cpu_game(3)).place(relx=0.5, rely=0.75, anchor=CENTER)
    
    #deck image/button
    # deck_image = PhotoImage(file="images/deck.png")
    # deck_button = Button(gui, image=deck_image, command=print_hello)
    # deck_button.place(relx=0.1, rely=0.5, anchor=CENTER)

    gui.mainloop() 
    
main()           
                
                
            
# def main():
#     # prompt the user to enter the number of plaers
#     num_players = int (input ('Enter number of players: '))
#     while (num_players > 4 or num_players < 0):
#         num_players = int (input ('Enter number of players: '))

#     # create the Poker object
#     game = Rummy(num_players)

#     # play the game
#     game.play_to_win()
    
# start_time = time.time()
# main()
#print("--- %s seconds ---" % (time.time() - start_time))

