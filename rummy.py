from copy import deepcopy
import gc
from tkinter import *
import tkinter.messagebox
from collections import OrderedDict
from CommonFunctions import sort_by, is_run, is_meld, str_to_card, is_valid, powerset
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
        self.player_picked_up = []
        
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
        
        self.select_button = Button(self.player_frame, text="select", highlightbackground = "red4", bg="red2", font=("Courier", 12), state="disabled", bd=4, command=lambda:self.table_cards(player = self.players[0], required_card=self.required_card))
        self.discard_button = Button(self.player_frame, text="discard", highlightbackground = "red4", bg="red2", font=("Courier", 12), state="disabled", bd=4, command=lambda:self.discard(player = self.players[0], required_card=self.required_card))
        
        self.back_card = PhotoImage(file="images/card_back.png")
        self.back_card.image = self.back_card
        
        # add players to game if first round
        if self.round_number == 1:
            player = Player([], [], method = "suit")
            cpu = CPU([], [], method = "suit")
            self.players.append(player)
            self.players.append(cpu)
        
        # deal the cards to the players
        for i in range(self.num_cards_in_hand):
            for player in self.players:
                player.cards_in_hand.append(self.deck.deal())
        for player in self.players:
            player.sort_by()
                
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
        self.all_tabled_cards = []
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
        # pick card
        if type(player) == CPU:
            pick_from = player.pickup_options(self.table.cards_on_table, self.all_melds, self.joint_runs)
            if type(pick_from) == Card:
                new_card, pick_from = pick_from, "table"
            else:
                pick_from = "pile"
        # else pick_from is given by user selection             
        if pick_from == "pile":
            return self.pick_from_pile(player)
        if pick_from == "table":
            return self.pick_from_table(player, new_card)
            
    def pick_from_pile(self, player):
        new_card = self.table.pickup_card_from_pile()
        # if pile is empty, end the round
        if not new_card:
            self.check_winner(player=player, default_loss=True)
            return
        # put card in player's hand
        player.pick(new_card)
        player.sort_by()
        if type(player) == Player:
            set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked=False, player=player)
        is_valid_pick, must_put_down_points = True, False
        return (is_valid_pick, must_put_down_points)
    
    def pick_from_table(self, player, new_card):
        is_valid_pick = must_put_down_points = False
        # check that card is valid to pick up                       
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
        player.cards_in_hand = sort_by(player.cards_in_hand, player.method)            
        if type(player) == CPU:
            is_valid_pick = True
            if len(new_cards) > 1:
                must_put_down_points = True
                return (is_valid_pick, must_put_down_points, first_card)
            return (is_valid_pick, must_put_down_points)
        # check valid pickup for player
        potential_hand = player.cards_in_hand
        is_valid_pick, must_put_down_points = self.check_valid_pickup_for_player(new_cards)
        if is_valid_pick:
            player.cards_in_hand = potential_hand
            player.sort_by()
            set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked=False, player=player)
            if must_put_down_points:
                self.required_card = first_card
            return True
        self.table.cards_on_table, player.cards_in_hand = old_cards, old_hand
        return False
        
    def check_valid_pickup_for_player(self, new_cards, potential_hand, first_card):
        if len(new_cards) == 1:
            return (True, False)
        hand_powerset = powerset(potential_hand)
        for subset_hand in hand_powerset:
            if first_card in subset_hand and is_valid(subset_hand):
                return (True, True)
        all_melds = deepcopy(self.get_all_melds())
        for points in all_melds:
            points.append(first_card)
            if is_valid(points):
                return (True, True)
        all_runs = deepcopy(self.get_all_joint_runs())
        for run in all_runs:
            run += potential_hand
            all_possible_runs = powerset(run)
            for subset_hand in all_possible_runs:
                if first_card in subset_hand and is_run(subset_hand):
                    return (True, True)
        return (False, False)
               
    def table_cards(self, player, required_card):
        if type(player) == CPU:
            # guaranteed to be highest combination of points and include required card if needed
            card_subs_to_put_down = player.table_cards_strategy(player.cards_in_hand, self.all_melds, self.joint_runs, required_card)
            if not card_subs_to_put_down:
                return
        else:
            # has all options but need to check required card
            valid_options = player.all_valid_table_card_options(player.cards_in_hand, self.all_melds, self.joint_runs)
            valid_option_keys = set(valid_options.keys())
            card_subs_to_put_down = set()
            for i, bn in enumerate(button_list):
                if bn["bd"] == 4:
                    card = player.cards_in_hand[i]
                    card_subs_to_put_down.add(card)
            if not card_subs_to_put_down:
                return
            if required_card and required_card not in card_subs_to_put_down:
                return
            for option in valid_option_keys:
                if option == card_subs_to_put_down:
                    card_subs_to_put_down = option
                    break
            else:
                return
        # identify where the card is going
        # add to all melds or all_runs          
        if type(player) == CPU:
            for option, identifier in card_subs_to_put_down.items():
                if len(identifier) == 1:
                    identifier = identifier[0]
                else:
                    identifier = identifier[1] # meld or run doesn't matter
                self.update_table_cards(player, option, identifier)
        else:
            options_dict = OrderedDict()
            count = 1
            key = valid_options[card_subs_to_put_down]
            num_options = len(key)
            paths = [[card.small_image_path()[21:-13] for card in identifier] for identifier in key]
            if num_options > 1:
                for i in range(len(paths)):
                    for j, widget in enumerate(self.points_frame.winfo_children()):
                        if widget["text"] in paths[i]:
                            options_dict[count] = [self.points_frame, key.get()[i]]
                            count += 1
                            break
                    for widget in self.other_frame.winfo_children():
                        if widget["text"] in paths[i]:
                            options_dict[count] = [self.other_frame, key.get()[i]]
                            count += 1
                            break
                self.show_options(options_dict)
            else:
                identifier = valid_options[card_subs_to_put_down][0]
                self.update_table_cards(player, card_subs_to_put_down, identifier)                
        return
                    
    def update_table_cards(self, player, subset_hand, identifier):
        # update all melds and runs
        if not identifier:
            if is_meld(subset_hand):
                self.all_melds.append(subset_hand)
            elif is_run(subset_hand):
                self.joint_runs.append(subset_hand)
            else:
                raise ValueError("Subset hand given was not a valid meld or run from hand")
        elif identifier in self.all_melds:
            self.all_melds.remove(identifier)
            self.all_melds.append(subset_hand)
        elif identifier in self.joint_runs:
            self.joint_runs.remove(identifier)
            self.joint_runs.append(subset_hand)
        else:
            raise ValueError("Subset hand given was not part of all melds or joint runs")
        # place cards into player's cards on table
        point_list = [card for card in subset_hand]
        # sort the cards before putting on table and remove from player's hand
        point_list = sorted(point_list)
        player.cards_on_table.append(point_list)
        cards_to_keep = [card for card in player.cards_in_hand if card not in subset_hand]
        player.cards_in_hand = cards_to_keep
        player.cards_in_hand = sort_by(player.cards_in_hand, player.method)
        # Update all cards on table
        self.set_all_tabled_cards()
        # update cards in hand graphics
        if type(player) == Player:
            set_sorting_method(bn=[self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = False, player = player, button_label_both="button")
            # update cards on table graphics
            clear_frame(self.points_frame)
            self.show_player_cards_on_table(player)
        return
    
    # Validate option chosen
    def return_option(self, options, potential_points, cards_objects, option_number):
        for bn in option_buttons:
            bn.destroy()
        self.valid_table_cards(self.players[0], options, potential_points, cards_objects, option_number)
    
    # Show options for tabling cards    
    def show_options(self, options_dict, cards_objects):
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
                        x = (i + 1)/10 + (j + 1)/(num_cards * 10)
                        label = Label(self.points_frame, image=card_image, highlightthickness = 0, bd = 0, text=path[21:-13])
                        label.place(relx=x, rely=y, anchor=CENTER)
                    else:
                        x = ((i + 1)/10 + (j + 1)/(num_cards * 10)) - 0.03
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
                player.sort_by()
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
            card = player.discard_strategy_greedy(self.table.cards_on_table, self.all_melds, self.joint_runs)
            # add card to table
            self.table.place_card_on_table(card)
            card = str_to_card(card)
            player.discard(card)
            player.sort_by()
            
    ##############################################
    # simulate the play of rummy
    ##############################################
    
    def cpu_play(self):
        i = 1
        player = self.players[1]
        
        # pick up card
        pickup = self.pickup(player)
        valid_pickup, must_put_down_points = pickup[0], pickup[1]
        required_card = None
        if must_put_down_points:
            required_card = pickup[2]
        while not valid_pickup:
            valid_pickup = self.pickup(player)
            
        # get points
        self.table_cards(player, must_put_down_points, required_card)
        if player.round_winner() and self.check_winner(player):
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
            player.sort_by()
        else:
            sort_method.configure(text="suit")
            player.set_method("suit")
            player.sort_by()
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

def global_frame_creation():
    global gui
    # set window size and color
    gui = Tk(className='Rummy - Window Size')
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
    frame1.player_button = Button(frame1, text="Player v CPU", font=("Courier", 15), command=lambda:[destroy_frame(frame1), create_game(2)]).place(relx=0.5, rely=0.45, anchor=CENTER)
    frame1.players_button = Button(frame1, text="Multiplayer", font=("Courier", 15), command=lambda:create_cpu_game(3)).place(relx=0.5, rely=0.75, anchor=CENTER)

    gui.mainloop() 
    
if __name__ == "__main__":
   global_frame_creation()         


