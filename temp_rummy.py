import gc
import tkinter.messagebox
import os, sys
from copy import deepcopy
from tkinter import *
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
        # set up deck and shuffle
        self.deck = Deck()
        self.deck.shuffle()
        
        # init players
        self.num_players = num_players
        self.players = players
        
        # init card attributes
        self.num_cards_in_hand = 10
        self.all_tabled_cards, self.joint_runs, self.all_melds, self.cards_on_table = [], [], [], []
        self.selected_table_card = self.required_card = None
        
        # init round attributes
        self.round_number = round_number
        self.round_points_list = round_points_list
        
        # init main frame
        self.gui = Tk(className='Rummy')
        self.gui.bind('<Escape>', lambda event: self.gui.state('normal'))
        self.gui.bind('<F11>', lambda event: self.gui.state('zoomed'))
        self.gui.configure(bg='SpringGreen3')
        self.gui.geometry("1000x600")
        
        # TODO: Modify frames for cpu v cpu type game
        # init first person or first CPU frame
        self.player_frame = Frame(self.gui, width=1000, height=105)
        self.player_frame.pack(side="bottom", fill="x")
        self.player_frame.configure(bg='SpringGreen3')
        
        # init second person or second CPU frame
        self.other_frame = Frame(self.gui, width=1000, height=400)
        self.other_frame.pack(side="top", fill="x", expand=True)
        self.other_frame.configure(bg='SpringGreen3')  
        
        # init points frame for first person
        self.points_frame = Frame(self.gui, width=1000, height=150)
        self.points_frame.pack(fill="x")
        self.points_frame.configure(bg='SpringGreen3')
        
        # set up buttons and labels
        self.rummy_game_path = os.path.dirname(os.path.abspath(__file__))
        self.back_card = PhotoImage(file=self.rummy_game_path + "/images/card_back.png")
        self.back_card.image = self.back_card
        
        self.sort_method = Button(self.player_frame, state="disable", text="suit", command=lambda:set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = True, player = self.players[0], button_label_both="both"), highlightbackground = "red4", bg="red2", bd=4, font=("Courier", 12))
        self.sort_method.place(relx=0.1, rely=0.7, anchor=CENTER)
        
        self.deck_image = PhotoImage(file=self.rummy_game_path + "/images/deck.png")
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

        # show first card in pile
        self.deck_label = Label(self.other_frame, image=self.deck_image, highlightthickness = 0, bd = 0)
        self.deck_label.place(relx=0.1, rely=0.85, anchor=CENTER)
        
        # place select and discard buttons for player
        self.select_button = Button(self.player_frame, text="select", highlightbackground = "red4", bg="red2", font=("Courier", 12), state="disabled", bd=4, command=lambda:self.table_cards(player = self.players[0], required_card=self.required_card))
        self.discard_button = Button(self.player_frame, text="discard", highlightbackground = "red4", bg="red2", font=("Courier", 12), state="disabled", bd=4, command=lambda:self.discard(player = self.players[0], required_card=self.required_card))
        
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
        
        # allow sort method button        
        self.sort_method.configure(state = "normal")       
        self.back_card_labels = []     
        # for each player, either sort the card images and show or show back of cards for cpu
        for i, player in enumerate(self.players):
            if type(player) == Player:
                set_sorting_method(bn = [self.sort_method, self.select_button, self.discard_button], frame=self.player_frame, clicked = False, player = player)
            else:
                num_cards = len(player.cards_in_hand)
                for i in range(len(player.cards_in_hand)):
                    x = 0.2 + (i + 1)/(num_cards * 2.3)
                    label = Label(self.other_frame, image=self.back_card, highlightbackground = "black")
                    self.back_card_labels.append(label)
                    label.place(relx=x, rely=0.2, anchor=CENTER)
          
        # show first card of the deck and allow for selection
        self.table = Table(self.deck, [])
        first_card = self.table.cards_in_pile.deal()
        self.table.place_card_on_table(first_card)
        paths = self.table.get_cards_on_table()   
        for i in range(len(self.table.cards_on_table)):
            path = paths[i]
            card_image = PhotoImage(file=self.rummy_game_path + "/" + path)
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
            
    # Trigger events to start game    
    def trigger_events(self):
        keep = self.back_card_labels
        for widget in self.other_frame.winfo_children():
            if type(widget).__name__ == "Button":
                keep.append(widget)
                widget.configure(state = "normal")
        clear_frame(self.other_frame, keep = keep)
    
    
def create_game(num_players):
    game = Rummy(num_players)
    #game.play_to_win()
    game.trigger_events()
    
# remove all widgets from a frame except widgets in keep list
def clear_frame(frame, keep = []):
    for widget in frame.winfo_children():
        if widget in keep:
            continue
        widget.place_forget()

# config board of button
def config_border(i):
    bn = button_list[i]
    bn.configure(bd = 4) if not bn["bd"] else bn.configure(bd = 0)
        
# set the sorting method for player                
def set_sorting_method(bn, frame, clicked, player = None, button_label_both = "both"):
    rummy_game_path = os.path.dirname(os.path.abspath(__file__))
    gc.disable()
    sort_method = bn[0]
    # if the method button was clicked then the order needs to be changed
    if clicked:
        if sort_method["text"] == "suit":
            sort_method.configure(text="rank")
            player.set_method("rank")
            player.sort_by()
        else:
            sort_method.configure(text="suit")
            player.set_method("suit")
            player.sort_by()
    # get list of image paths
    paths = player.get_cards_in_hand() # list of image paths
    # remove all widgets from frame except list widges in bn that need to stay
    clear_frame(frame, keep = bn)
    # create global list of new buttons
    global button_list
    button_list = []
    # create new button or label for earch card depending on button_label_both setting
    for i in range(len(player.cards_in_hand)):
        path = paths[i]
        card_image = PhotoImage(file=rummy_game_path + "/" + path)
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
            
# set the selected card from outside class
def set_selected_table_card(self, card):
    self.selected_table_card = card