from math import floor
import random
import itertools
from copy import deepcopy
import time
import gc
from tkinter import *
import tkinter.messagebox
from collections import OrderedDict
from CommonFunctions import _sort_by, is_run, is_meld, str_to_card
from card import Card
from deck import Deck
from player import Player
from cpu import CPU
from table import Table


class Rummy(object):
    # constructor
    def __init__(self, num_players = 2, players = [], round_number = 1, round_points_list = [(" ", "You", "CPU")]):
        self.deck = Deck()
        self.deck.shuffle()
        self.num_players = num_players
        self.num_cards_in_hand = 10
        self.players = players
        self.all_tabled_cards = []
        self.round_number = round_number
        self.joint_runs = []
        self.all_melds = []
        self.cards_on_table = []
        self.round_points_list = round_points_list
        
        # set up frames
        self.player_frame = Frame(gui, width=1000, height=105)
        self.player_frame.pack(side="bottom", fill="x")
        self.player_frame.configure(bg='SpringGreen3')
        
        self.other_frame = Frame(gui, width=1000, height=400)
        self.other_frame.pack(side="top", fill="x", expand=True)
        self.other_frame.configure(bg='SpringGreen3')  
        
        self.points_frame = Frame(gui, width=1000, height=150)
        self.points_frame.pack(fill="x")
        self.points_frame.configure(bg='SpringGreen3')
        
        # set up buttons and labels
        self.sort_method = Button(self.player_frame, state="disable", text="suit", command=lambda:set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = True, player = self.players[0], button_label_both="both"), highlightbackground = "red4", bg="red2", bd=4, font=("Courier", 12))
        self.sort_method.place(relx=0.1, rely=0.7, anchor=CENTER)
        
        self.deck_image = PhotoImage(file="images/deck.png")
        self.deck_image.image = self.deck_image
        
        self.deck_button = Button(self.other_frame, image=self.deck_image, state="disable", highlightthickness = 0, bd = 0,\
            command=lambda:[self.deck_button.configure(state="disable"), \
            self.deck_label.place(relx=0.1, rely=0.83, anchor=CENTER), \
            self.change_state_on_table(first_card = True), \
            self.sort_method.configure(command = lambda:set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = True, player = self.players[0], button_label_both="button")), \
            self.pickup(self.players[0], "pile"), \
            self.change_state_in_hand(), \
            self.select_button.place(relx=0.0251, rely=0.05), \
            self.discard_button.place(relx=0.105, rely=0.05), \
            set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = False, player = self.players[0], button_label_both="button"), \
            self.select_button.configure(state = "normal"), \
            self.discard_button.configure(state="normal")])
        self.deck_button.place(relx=0.1, rely=0.83, anchor=CENTER)
      
        self.deck_label = Label(self.other_frame, image=self.deck_image, highlightthickness = 0, bd = 0)
        self.deck_label.place(relx=0.1, rely=0.85, anchor=CENTER)
        
        self.select_button = Button(self.player_frame, text="select", highlightbackground = "red4", bg="red2", font=("Courier", 12), state="disabled", bd=4, command=lambda:self.table_cards(player = self.players[0], required_card=self.required_card, index=None))
        self.discard_button = Button(self.player_frame, text="discard", highlightbackground = "red4", bg="red2", font=("Courier", 12), state="disabled", bd=4, command=lambda:self.discard(player = self.players[0], required_card=self.required_card))
        
        self.back_card = PhotoImage(file="images/card_back.png")
        self.back_card.image = self.back_card
        
        # add players to game if first round
        if self.round_number == 1:
            # CPU v CPU
            if self.num_players == 0:
                self.num_players == 2
                cpu1 = CPU([], [], method = "suit")
                self.players.append(cpu1)
                cpu2 = CPU([], [], method = "suit")
                self.players.append(cpu2)
            # CPU v Player
            elif self.num_players == 1:
                self.num_players = 2
                player = Player([], [], method = "suit")
                cpu = CPU([], [], method = "suit")
                self.players.append(player)
                self.players.append(cpu)
            # Player v Player
            else:
                for i in range(self.num_players):
                    player = Player([], [], method = "suit")
                    self.players.append(player)
        
        # deal the cards to the players
        for i in range(self.num_cards_in_hand):
            for player in self.players:
                player.cards_in_hand.append(self.deck.deal())
        for player in self.players:
            player.sort_by(player.cards_in_hand, player.method)
        # # test scenario
        # for player in self.players:
        #     if type(player) == Player:
        #         cards = [Card(7, 'S'), Card(7, 'D'), Card(7, 'C'), Card(7, 'H')]
        #         player.cards_in_hand = cards
        #     else:
        #         cards = [Card(3, 'D'), Card(4, 'H'), Card(6, 'S'), Card(5, 'S'), Card(4, 'S'), Card(8, 'S'), Card(9, 'S'), Card(10, 'S')]
        #         player.cards_in_hand = cards  
        # # test scenario 2
        # for player in self.players:
        #     if type(player) == Player:
        #         cards = [Card(12, 'S'), Card(12, 'D'), Card(12, 'C'), Card(12, 'H'), Card(14, 'S'), Card(14, 'D'), Card(14, 'C'), Card(14, 'H')]
        #         player.cards_in_hand = cards
        #     else:
        #         cards = [Card(3, 'D'), Card(4, 'H'), Card(6, 'S'), Card(5, 'S'), Card(4, 'S'), Card(8, 'S'), Card(9, 'S'), Card(10, 'S')]
        #         player.cards_in_hand = cards
        
        self.sort_method.configure(state = "normal")       
        self.back_card_labels = []     
        # sort the hands of each player and print
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
        
        # init card selected by player
        self.selected_table_card = None
          
        # show first card of the deck and allow for selection
        self.table = Table(self.deck, [])
        first_card = self.table.cards_in_pile.deal()
        self.table.place_card_on_table(first_card)
        paths = self.table.get_cards_on_table()   
        for i, card in enumerate(self.table.cards_on_table):
            path = paths[i]
            card_image = PhotoImage(file=path)
            card_image.image = card_image
            first_card_button = Button(self.other_frame, image=card_image, highlightthickness = 0, bd = 0, state="disable",\
                command=lambda:[self.deck_button.configure(state="disable"), \
                self.deck_label.place(relx=0.1, rely=0.83, anchor=CENTER), \
                self.change_state_on_table(), \
                first_card_button.destroy(), \
                self.sort_method.configure(command = lambda:set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = True, player = self.players[0], button_label_both="button")), \
                set_selected_table_card(self, first_card), \
                self.pickup(self.players[0], "table"), \
                self.change_state_in_hand(), \
                self.select_button.place(relx=0.0251, rely=0.05), \
                self.discard_button.place(relx=0.105, rely=0.05), \
                set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = False, player = self.players[0], button_label_both="button"), \
                self.select_button.configure(state = "normal"), \
                self.discard_button.configure(state="normal")])
            first_card_button.place(relx=0.2, rely=0.85, anchor=CENTER)
            
        # init required card
        self.required_card = None
    
    # Trigger events to start game    
    def trigger_events(self):
        keep = self.back_card_labels
        for widget in self.other_frame.winfo_children():
            if type(widget).__name__ == "Button":
                keep.append(widget)
                widget.configure(state = "normal")
        clear_frame(self.other_frame, keep = keep)
    
    ##############################################
    # Functions for getting point options
    ##############################################
    
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
    
    ##############################################
    # Game simulation functions
    ############################################## \
              
    def pickup(self, player, pick_from=None):
        is_valid_pick = False
        must_put_down_points = False
        # pick card
        if type(player) == CPU:
            pick_from = player.pickup_strategy1(self.table.cards_on_table, self.all_melds, self.joint_runs)
            new_card = None
            if type(pick_from) == list:
                cards_on_table = deepcopy(self.table.cards_on_table)[::-1]
                flat_pick_from = [card for sub in pick_from for card in sub]
                for card in cards_on_table:
                    if card in flat_pick_from:
                        new_card = card
                        break
            if not new_card:
                pick_from = "pile"
            else:
                pick_from = "table"
                        
        if pick_from == "pile":
            # take card from table
            new_card = self.table.pickup_card_from_pile()
            
            # if pile is empty, end the round
            if not new_card:
                self.check_winner(player=player, default_loss=True)
            # put card in player's hand
            player.pick(new_card)
            # sort new hand
            player.sort_by(player.cards_in_hand, player.method)
            if type(player) == Player:
                set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked=False, player=player)
            is_valid_pick = True
            return (is_valid_pick, must_put_down_points)
            
        elif pick_from == "table":
            # check that card is valid to pick up            
            def is_valid(subset_hand_objects):
                if is_meld(subset_hand_objects) or is_run(subset_hand_objects):
                    return True
                return False

            if type(player) == Player:
                # take cards from table
                new_card = self.selected_table_card
            else:
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
                return True

            for L in range(0, len(potential_hand) + 1):
                for subset_hand in itertools.combinations(potential_hand, L):
                    if first_card in subset_hand:
                        if is_valid(subset_hand):
                            is_valid_pick = True
                            player.cards_in_hand = potential_hand
                            player.sort_by(player.cards_in_hand, player.method)
                            must_put_down_points = True
                            self.required_card = first_card
                            set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked=False, player=player)
                            return True
                    
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
                return False
            else:
                must_put_down_points = True
                self.required_card = first_card
                # sort new hand
                player.cards_in_hand = potential_hand
                player.sort_by(player.cards_in_hand, player.method)
                set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked=False, player=player)
                return True
            
    def table_cards(self, player, required_card, index):
        if type(player) == CPU:
            combinations = player.table_cards_strategy1()
            if len(combinations) <= 0 or len(combinations) <= index:
                return "no"
            cards_objects = combinations[index]
            cards_objects = [card for card in cards_objects] # tuple to list
            cards = [str(card) for card in cards_objects]
        else:
            cards_objects = []
            for i, bn in enumerate(button_list):
                if bn["bd"] == 4:
                    card = player.cards_in_hand[i]
                    cards_objects.append(card)
            if not cards_objects:
                return
            if required_card and required_card not in cards_objects:
                return
            cards = [str(card) for card in cards_objects]
                    
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
                # print("Invalid. Cards cannot be repeated")
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
                path_options = [[card.small_image_path()[21:-13] for card in sublist] for sublist in options]
                options_list_str = [[str(card) for card in sublist] for sublist in options]
                options_dict = OrderedDict()
                count = 1
                if type(player) == CPU:
                    # strategy1
                    choice = player.choose_cards_strategy1(potential_points)
                    self.valid_table_cards(player, options, potential_points, cards_objects, choice)   
                elif type(player) == Player:
                    if len(options) > 1:
                        for i in range(len(path_options)):
                            for j, widget in enumerate(self.points_frame.winfo_children()):
                                if widget["text"] in path_options[i]:
                                    options_dict[count] = [self.points_frame, options[i]]
                                    count += 1
                                    break
                            for widget in self.other_frame.winfo_children():
                                if widget["text"] in path_options[i]:
                                    options_dict[count] = [self.other_frame, options[i]]
                                    count += 1
                                    break
                        self.show_options(options_dict, options, potential_points, cards_objects)
                    else:
                        choice = 1
                        self.valid_table_cards(player, options, potential_points, cards_objects, choice)
                        
            else:
                choice = 1
                self.valid_table_cards(player, None, None, cards_objects, choice)
                    
    def valid_table_cards(self, player, options, potential_points, cards_objects, choice = 1):
        if potential_points:
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
        # update cards in hand graphics
        if type(player) == Player:
            set_sorting_method(bn=[self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = False, player = player, button_label_both="button")
            # update cards on table graphics
            clear_frame(self.points_frame)
            self.show_player_cards_on_table(player)
        # check for winner
        if self.check_winner(player):
            return True
        else:
            self.required_card = None
            return False
     
    def get_points(self, player, must_put_down_points, required_card):
        index = 0
        ask = "yes" # cpu strategy1
            
        if ask == "yes": 
            multiple = True
            while multiple:
                # table cards
                cards_tabled = self.table_cards(player, required_card, index)
                if cards_tabled == True and player.round_winner():
                    multiple = False
                    return True
                if cards_tabled == False and must_put_down_points == False: # cards chosen incorrectly
                    index += 1
                    ask = "yes" # strategy1
                elif cards_tabled == False and must_put_down_points: # cards chosen incorrectly but must point down points
                    index += 1
                elif cards_tabled == "no":
                    multiple = False
                else:
                    required_card = None
                    index += 1
        return False

    # Validate option chosen
    def return_option(self, options, potential_points, cards_objects, option_number):
        for bn in option_buttons:
            print("option button: ", bn["text"])
            bn.destroy()
        self.valid_table_cards(self.players[0], options, potential_points, cards_objects, option_number)
    
    # Show options for tabling cards    
    def show_options(self, options_dict, options, potential_points, cards_objects):
        global option_buttons
        option_buttons = []
        option_number = 1
        points_frame_options = []
        for count, frame_cards in options_dict.items():
            if frame_cards[0] == self.points_frame:
                points_frame_options.append(frame_cards[1])
        if points_frame_options:
            clear_frame(self.points_frame)
            player = self.players[0]
            paths = player.get_cards_on_table() # list of image paths
            num_cards = sum(len(path_list) for path_list in paths)
            y = 0.45
            cards_on_table = deepcopy(player.cards_on_table)
            for i, card_list in enumerate(cards_on_table):
                if card_list in points_frame_options:
                    option_button = Button(self.points_frame, text=str(option_number), highlightbackground = "red4", bg="red2", font=("Courier", 8), bd=4)
                    option_buttons.append(option_button)
                    card_list.insert(0, option_button)
                    option_number += 1
                change_index = False
                for j, card in enumerate(card_list):
                    if type(card_list[j]) == Card:
                        if change_index:
                            j-=1
                        path = paths[i][j]
                        card_image = PhotoImage(file=path)
                        card_image.image = card_image
                        x = (i + 1)/10 + (j + 1)/(num_cards * 12)
                        label = Label(self.points_frame, image=card_image, highlightthickness = 0, bd = 0, text=path[21:-13])
                        label.place(relx=x, rely=y, anchor=CENTER)
                    else:
                        x = ((i + 1)/10 + (j + 1)/(num_cards * 12)) - 0.03
                        card_list[j].place(relx=x, rely=y, anchor=CENTER)
                        change_index = True
                        
        other_frame_options = []
        for count, frame_cards in options_dict.items():
            if frame_cards[0] == self.other_frame:
                other_frame_options.append(frame_cards[1])
        if other_frame_options:
            keep = self.back_card_labels + [self.deck_button] + [self.deck_label]
            clear_frame(self.other_frame, keep)
            player = self.players[1]
            paths = player.get_cards_on_table() # list of image paths
            num_cards = sum(len(path_list) for path_list in paths)
            y = 0.5
            cards_on_table = deepcopy(player.cards_on_table)
            for i, card_list in enumerate(cards_on_table):
                if card_list in other_frame_options:
                    option_button = Button(self.other_frame, text=str(option_number), highlightbackground = "red4", bg="red2", font=("Courier", 8), bd=4)
                    option_buttons.append(option_button)
                    card_list.insert(0, option_button)
                    option_number += 1
                change_index = False
                for j, card in enumerate(card_list):
                    if type(card_list[j]) == Card:
                        if change_index:
                            j -= 1
                        path = paths[i][j]
                        card_image = PhotoImage(file=path)
                        card_image.image = card_image
                        x = (i + 1)/10 + (j + 1)/(num_cards * 12)
                        label = Label(self.other_frame, image=card_image, highlightthickness = 0, bd = 0, text=path[21:-13])
                        label.place(relx=x, rely=y, anchor=CENTER)
                    else:
                        if num_cards >= 8:
                            x = (i + 1)/12 + j/(num_cards * 12) - 0.03
                        else:
                            x = ((i + 1)/10 + j/(num_cards * 12)) - 0.03
                        card_list[j].place(relx=x, rely=y, anchor=CENTER)
                        change_index = True
                        
            for i, bn in enumerate(option_buttons):
                bn.configure(command=lambda i = i:self.return_option(options, potential_points, cards_objects, i+1))  
            # show card on table
            paths = self.table.get_cards_on_table()
            for i, card in enumerate(self.table.cards_on_table):
                path = paths[i]
                card_image = PhotoImage(file=path)
                card_image.image = card_image
                x = 0.2 + i/35
                label = Label(self.other_frame, image=card_image, highlightthickness = 0, bd = 0)
                label.place(relx=x, rely=0.85, anchor=CENTER)
          
    def discard(self, player, required_card=None):
        # have players discard
        if type(player) == Player:
            if self.required_card:
                return
            cards_objects = []
            for i, bn in enumerate(button_list):
                if bn["bd"] == 4:
                    card = player.cards_in_hand[i]
                    cards_objects.append(card)
            
            if len(cards_objects) == 1:
                # add card to table
                self.table.place_card_on_table(card)
                for widget in self.other_frame.winfo_children():
                    if type(widget).__name__ == "Button":
                        widget.place_forget()
                # show card on table
                paths = self.table.get_cards_on_table()
                for i, card in enumerate(self.table.cards_on_table):
                    path = paths[i]
                    card_image = PhotoImage(file=path)
                    card_image.image = card_image
                    x = 0.2 + i/35
                    label = Label(self.other_frame, image=card_image, highlightthickness = 0, bd = 0)
                    label.place(relx=x, rely=0.85, anchor=CENTER)
                # remove card from player's hand
                player.discard(card)
                player.sort_by(player.cards_in_hand, player.method)
                # show player's hand
                set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked=False, player=player, button_label_both="label")
                # show cards on table
                clear_frame(self.points_frame)
                self.show_player_cards_on_table(player)
                # turn on gc
                self.select_button.place_forget()
                self.discard_button.place_forget()
            else:
                return    
            
            if self.check_winner(player):
                return
            # cpu's turn
            self.cpu_play()
            
        else:
            card = player.discard_strategy1(self.table.cards_on_table)
            # add card to table
            self.table.place_card_on_table(card)
            card = str_to_card(card)
            player.discard(card)
            player.sort_by(player.cards_in_hand, player.method)
            
    ##############################################
    # simulate the play of rummy
    ##############################################
    
    def cpu_play(self):
        i = 1
        player = self.players[1]
        
        # pick up card
        pickup = self.pickup(player)
        valid_pickup = pickup[0]
        must_put_down_points = pickup[1]
        required_card = None
        if len(pickup) == 3:
            required_card = pickup[2]
        while not valid_pickup:
            valid_pickup = self.pickup(player)
            
        # get points
        is_winner = self.get_points(player, must_put_down_points, required_card)
        if is_winner:
            if self.check_winner(player):
                return
            
        # discard
        self.discard(player)  
        if self.check_winner(player):
            return
          
        # remove cards from table
        for widget in self.other_frame.winfo_children():
            if widget != self.deck_label:
                widget.place_forget()
        paths = self.table.get_cards_on_table()
        for i, card in enumerate(self.table.cards_on_table):
            path = paths[i]
            card_image = PhotoImage(file=path)
            card_image.image = card_image
            x = 0.2 + i/35
            button = Button(self.other_frame, image=card_image, highlightthickness = 0, bd = 0)
            button.place(relx=x, rely=0.85, anchor=CENTER)
            
        # show new card in hand
        self.back_card_labels = []
        num_cards = len(player.cards_in_hand)
        for i, card in enumerate(player.cards_in_hand):
            x = 0.2 + (i + 1)/(num_cards * 2.3)
            label = Label(self.other_frame, image=self.back_card, highlightbackground = "black")
            self.back_card_labels.append(label)
            label.place(relx=x, rely=0.2, anchor=CENTER) 
            
        # show point cards on table
        self.show_player_cards_on_table(player)
        
        # set up player's turn
        self.deck_button.configure(state="normal")
        self.deck_button.place(relx=0.1, rely=0.83, anchor=CENTER)
        self.deck_label.place_forget()
        
        paths = self.table.get_cards_on_table() 
        
        global card_buttons
        card_buttons = [] 
        for i, card in enumerate(self.table.cards_on_table):
            path = paths[i]
            card_image = PhotoImage(file=path)
            card_image.image = card_image
            card_button = Button(self.other_frame, image=card_image, text=str(card), highlightthickness = 0, bd = 0, state="disable", command=lambda i = i:config_border_and_pickup(i, self))
            x = 0.2 + i/35
            card_buttons.append(card_button)
            card_button.place(relx=x, rely=0.85, anchor=CENTER)
            
            for bn in card_buttons:
                bn.configure(state="normal")
                
    ##############################################
    # State changes on table for GUI
    ##############################################
        
    # lower labels and change button states to normal
    def change_state_in_hand(self):
        for widget in self.player_frame.winfo_children():
            if type(widget).__name__ == "Label":
                widget.lower()
            if type(widget).__name__ == "Button":
                widget.configure(state = "normal")
    
    # show updated player cards on table            
    def show_player_cards_on_table(self, player):
        if type(player) == Player:
            frame = self.points_frame
            y = 0.45
        else:
            frame = self.other_frame
            y = 0.5
        paths = player.get_cards_on_table() # list of image paths
        num_cards = sum(len(path_list) for path_list in paths)
        for i, card_list in enumerate(player.cards_on_table):
            for j, card in enumerate(card_list):
                path = paths[i][j]
                card_image = PhotoImage(file=path)
                card_image.image = card_image
                if num_cards >= 8:
                    x = (i + 1)/12 + j/(num_cards * 12)
                else:
                    x = (i + 1)/10 + j/(num_cards * 10)
                label = Label(frame, image=card_image, highlightthickness = 0, bd = 0, text=path[21:-13])
                label.place(relx=x, rely=y, anchor=CENTER)
    
    # Remove buttons and update cards            
    def change_state_on_table(self, reset_cards_on_table = False, first_card = False):
        for widget in self.other_frame.winfo_children():
            if type(widget).__name__ == "Button":
                widget.place_forget()
        paths = self.table.get_cards_on_table() # list of image paths
        for i, card in enumerate(self.table.cards_on_table):
            path = paths[i]
            card_image = PhotoImage(file=path)
            card_image.image = card_image
            x = 0.2 + (i)/(len(paths) * 2)
            label = Label(self.player_frame, image=card_image, highlightthickness = 0, bd = 0)
            label.place(relx=x, rely=0.85, anchor=CENTER)
        if reset_cards_on_table:
            # cpu
            keep = self.back_card_labels + [self.deck_button] + [self.deck_label]
            clear_frame(self.other_frame, keep)
            player = self.players[1]
            self.show_player_cards_on_table(player)
            
            # player
            keep = [self.select_button] + [self.discard_button] + [self.sort_method]
            clear_frame(self.player_frame, keep)
            player = self.players[0]
            #self.show_player_cards_on_table(player)
        if first_card:
            for i, card in enumerate(self.table.cards_on_table):
                path = paths[i]
                card_image = PhotoImage(file=path)
                card_image.image = card_image
                x = 0.2 + i/35
                label = Label(self.other_frame, image=card_image, highlightthickness = 0, bd = 0)
                label.place(relx=x, rely=0.85, anchor=CENTER)
    
    ##############################################
    # Endgame
    ##############################################
    
    def check_winner(self, player, default_loss=False):
        if player.game_winner():
            self.game_over()
        elif player.round_winner() or default_loss:
            destroy_frame(self.player_frame)
            destroy_frame(self.other_frame)
            destroy_frame(self.points_frame)

            if self.round_number > 1:
                self.round_points_list = self.round_points_list[:-1]
            self.round_points_list.append((" ", self.players[0].end_points(), self.players[1].end_points()))
            self.round_points_list.append(("Total: ", self.players[0].points, self.players[1].points))
            last_pos = [0, 0]
            # code for creating table
            for i in range(self.round_number + 2):
                for j in range(len(self.players) + 1):
                    e = Entry(gui, width=10, bg='red4', fg='white', font=('Courier',16,'bold'))
                    x = j/10 + 0.4
                    y = i/25 + 0.5
                    e.place(relx=x, rely=y, anchor=CENTER)
                    e.insert(END, self.round_points_list[i][j])
                    last_pos = [x, y]
                
            next_round_button = Button(gui, text="Go", highlightbackground = "red4", bg="red2", font=("Courier", 12), bd=4, command=lambda:self.next_round())
            next_round_button.place(relx=last_pos[0]+0.1, rely=last_pos[1]+0.1, anchor=CENTER)
            return True
        
    def next_round(self):
        round_number = self.round_number + 1
        players = []
        for i, p in enumerate(self.players):
            if type(p) == Player:
                players.append(Player([], [], p.method, p.points))
            else:
                players.append(CPU([], [], p.method, p.points))
        
        clear_frame(gui)        
        self = Rummy(self.num_players, players, round_number, self.round_points_list)
        self.trigger_events()    
    
    # Screen to end game            
    def game_over(self):
        p1 = self.players[0].points
        p2 = self.players[1].points
        if p1 == p2:
            # tie screen
            gui.configure(bg='Black')
            tie = Label(gui, text="Tie", font=("Courier", 40))
            tie.place(relx=0.4, rely=0.5, anchor=CENTER)
        elif p1 > p2:
            # you win
            gui.configure(bg='Black')
            gui.configure(bg='Black')
            win = Label(gui, text="You \n Win!", font=("Courier", 40))
            win.place(relx=0.4, rely=0.5, anchor=CENTER)
        else:
            # you lose
            gui.configure(bg='Black')
            gui.configure(bg='Black')
            lose = Label(gui, text="You \n Lose", font=("Courier", 40))
            lose.place(relx=0.4, rely=0.5, anchor=CENTER)
                

##############################################
# Init game and global functions
##############################################

def create_cpu_game(num_players):
    tkinter.messagebox.showinfo("", "This feature is not yet available")
    
def create_game(num_players):
    game = Rummy(num_players)
    #game.play_to_win()
    game.trigger_events()

def destroy_frame(frame):
    # destroy all widgets from frame
    for widget in frame.winfo_children():
       widget.destroy()
    frame.destroy()
    
def clear_frame(frame, keep = []):
    for widget in frame.winfo_children():
        if widget in keep:
            continue
        widget.place_forget()

def set_sorting_method(bn, frame, clicked, player = None, button_label_both = "both"):
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
    keep_gc_on = False   
    paths = player.get_cards_in_hand() # list of image paths
    clear_frame(frame, keep = bn)
    global button_list
    button_list = []
    for i, card in enumerate(player.cards_in_hand):
        path = paths[i]
        card_image = PhotoImage(file=path)
        card_image.image = card_image
        x = 0.2 + (i + 1)/(len(paths) * 2)
        if button_label_both == "button":
            button = Button(frame, image=card_image, highlightthickness = 0, bd = 0, command=lambda i = i:config_border(i))
            button.place(relx=x, rely=0.5, anchor=CENTER)
            button_list.append(button)
            keep_gc_on = True
        elif button_label_both == "label":
            label = Label(frame, image=card_image, highlightthickness = 0, bd = 0).place(relx=x, rely=0.5, anchor=CENTER)
        else:
            button = Button(frame, image=card_image, highlightthickness = 0, bd = 0, state="disable").place(relx=x, rely=0.5, anchor=CENTER)
            label = Label(frame, image=card_image, highlightthickness = 0, bd = 0).place(relx=x, rely=0.5, anchor=CENTER)
    #gc.enable()
    
def set_selected_table_card(self, card):
    self.selected_table_card = card
            
def config_border(i):
    bn = button_list[i]
    if bn["bd"] == 0:
        bn.configure(bd=4)
    else:
        bn.configure(bd=0)
    
def config_border_and_pickup(i, self):
    selected = card_buttons[i]
    if selected["bd"] == 0:
        selected.configure(bd=4)
    else:
        selected.configure(bd=0)
        return
        
    self.sort_method.configure(command = lambda:set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = True, player = self.players[0], button_label_both="button"))
    set_selected_table_card(self, str_to_card(selected["text"]))
    valid_pickup = self.pickup(self.players[0], "table")
    if valid_pickup:
        self.deck_button.configure(state="disable")
        self.deck_label.place(relx=0.1, rely=0.83, anchor=CENTER)
        self.change_state_on_table(reset_cards_on_table = True, first_card = True)
        self.change_state_in_hand()
        self.select_button.place(relx=0.0251, rely=0.05)
        self.discard_button.place(relx=0.105, rely=0.05)
        set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = False, player = self.players[0], button_label_both="button")
        self.select_button.configure(state = "normal")
        self.discard_button.configure(state="normal")
    else:
        return

def main():
    global gui
    gui = Tk(className='Rummy - Window Size')# set window size and color
    gui.bind('<Escape>', lambda event: gui.state('normal'))
    gui.bind('<F11>', lambda event: gui.state('zoomed'))
    gui.configure(bg='SpringGreen3')
    gui.geometry("1000x600")
    
    # set up game
    frame1 = Frame(gui)
    frame1.pack(side="top", expand=True, fill="both")
    frame1.configure(bg='SpringGreen3')

    frame1.choice_label = Label(frame1, text="Choose your game:", font=("Courier", 30), bg="SpringGreen3").place(relx=0.5, rely=0.25, anchor=CENTER)
    frame1.cpu_button = Button(frame1, text="CPU v CPU", font=("Courier", 15), command=lambda:create_cpu_game(0)).place(relx=0.5, rely=0.6, anchor=CENTER)
    frame1.player_button = Button(frame1, text="Player v CPU", font=("Courier", 15), command=lambda:[destroy_frame(frame1), create_game(1)]).place(relx=0.5, rely=0.45, anchor=CENTER)
    frame1.players_button = Button(frame1, text="Multiplayer", font=("Courier", 15), command=lambda:create_cpu_game(3)).place(relx=0.5, rely=0.75, anchor=CENTER)

    gui.mainloop() 
    
main()           


