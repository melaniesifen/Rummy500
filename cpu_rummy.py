# command line application for ML purposes
import random
import itertools
import time
import mysql.connector
import sys
import gc
from rummy import Rummy
from math import floor
from copy import deepcopy
from CommonFunctions import _sort_by, is_run, is_meld, str_to_card
from card import Card
from deck import Deck
from cpu import CPU
from table import Table

gc.enable()
class CPURummy(Rummy):
    def __init__(self, players = [], round_number = 1):
        self.deck = Deck()
        self.deck.shuffle()
        self.num_players = 2
        self.num_cards_in_hand = 10
        self.players = players
        self.all_tabled_cards = []
        self.round_number = round_number
        self.joint_runs = []
        self.all_melds = []
        self.cards_on_table = []
        
        # add players for first round
        if self.round_number == 1:
            cpu1 = CPU([], [], method = "suit")
            self.players.append(cpu1)
            cpu2 = CPU([], [], method = "suit")
            self.players.append(cpu2)
        
        # deal the cards to the players
        for i in range(self.num_cards_in_hand):
            for player in self.players:
                player.cards_in_hand.append(self.deck.deal())
        for player in self.players:
            player.sort_by(player.cards_in_hand, player.method)
            
        # show first card of the deck and allow for selection
        self.table = Table(self.deck, [])
        first_card = self.table.cards_in_pile.deal()
        self.table.place_card_on_table(first_card)
    
    # Screen to end game            
    def game_over(self):
        for player in self.players:
            player.end_points()
            print(player.points)
        p1 = self.players[0].points
        p2 = self.players[1].points
        if p1 == p2:
            print("Tie")
        elif p1 > p2:
            print("player 1 wins")
        else:
            # p2 wins
            print("player 2 wins")
        print("--- %s seconds ---" % (time.time() - start_time))  
        sys.exit()
            
            
    def check_winner(self, player, default_loss=False):
        if player.game_winner():
            self.game_over()
        elif player.round_winner() or default_loss:              
            return True
        return False
        
    def cpu_play(self, player):    
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
                return True
        if self.check_winner(player):
            return True
            
        # discard
        self.discard(player)  
        if self.check_winner(player):
            return True
        return False
    
    def next_round(self):
        for player in self.players:
            np = player.end_points()
        round_number = self.round_number + 1
        print("starting round: ", round_number)
        players = [CPU([], [], player.method, player.points) for player in self.players]
        self = CPURummy(players, round_number)
        self.play_round()
        
    def play_round(self):
        round_winner = False
        while not round_winner:
            for player in self.players:
                round_winner = self.cpu_play(player)
                if round_winner:
                    break
        self.next_round()
        
        
def main():
    my_cpu_game = CPURummy()
    my_cpu_game.play_round()
    
start_time = time.time()
main()                  
                        
                
        
        
        
        
        
        
        
    
    