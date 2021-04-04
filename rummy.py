import random
import itertools
from card import Card
from deck import Deck
from player import Player
from table import Table
    
class Rummy(object):
    # constructor
    def __init__(self, num_players = 2):
        self.deck = Deck()
        self.deck.shuffle()
        self.num_players = num_players
        self.num_cards_in_hand = 10
        self.players = []
        
        # add players to game
        for i in range(self.num_players):
            player = Player([], [], method = "suit")
            self.players.append(player)
        
        # deal the cards to the players
        for i in range(self.num_cards_in_hand):
            for player in self.players:
                player.cards_in_hand.append(self.deck.deal())
        
        # sort the hands of each player and print
        for i, player in enumerate(self.players):
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
            
        # show first card of the deck  
        self.table = Table(self.deck, [])
            
        
    def pickup(self, player):
        
        is_valid_pick = False
        must_put_down_points = False
        # pick card
        pick_from = input("Pick from pile or pick from table? ")
        while pick_from != "pile" and pick_from != "table":
            print("Invalid entry. Please choose 'pile' or 'table'. \n")
            pick_from = input()
        
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
            # take card from table
            new_card = input("Choose a card from the table to pick up. ")
            cards_to_choose_from = [str(card) for card in self.table.cards_on_table]
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
            
            # check that card is valid to pick up
            def sort_subset(hand, method):
                if method == "suit":
                    sorted_hand = []
                    s = []
                    h = []
                    d = []
                    c = []
                    for card in hand:
                        if card.suit == 'S':
                            s.append(card)
                        elif card.suit == 'H':
                            h.append(card)
                        elif card.suit == 'D':
                            d.append(card)
                        else:
                            c.append(card)
                    sorted_s = sorted(s)
                    sorted_h = sorted(h)
                    sorted_d = sorted(d)
                    sorted_c = sorted(c)
                    sorted_hand = sorted_s + sorted_h + sorted_d + sorted_c
                    return sorted_hand
                else:
                    sorted_hand = sorted(hand)
                    return sorted_hand
            
            def is_run(subset_hand):
                if len(subset_hand) < 3:
                    return False
            
                same_suit = True
                for i in range(len(subset_hand) - 1):
                    same_suit = same_suit and (subset_hand[i].suit == subset_hand[i + 1].suit)
                if not same_suit:
                    return False

                sorted_subset_hand = sort_subset(subset_hand, method = "rank")
                rank_order = True
                for i in range(len(subset_hand) - 1):
                    if subset_hand[i].rank == 14:
                        if (rank_order and (subset_hand[i].rank == subset_hand[i + 1].rank - 1)) == False:
                            if (rank_order and (1 == subset_hand[i + 1].rank - 1)) == False:
                                rank_order = False
                    rank_order = rank_order and (subset_hand[i].rank == subset_hand[i + 1].rank - 1)
                if not rank_order:
                    return False
                return True
            
            def is_meld(subset_hand):
                if len(subset_hand) < 3 or len(subset_hand) > 4:
                    return False
                for i in range(len(subset_hand) - 1):
                    if subset_hand[i].rank != subset_hand[i + 1].rank:
                        return False
                return True
            
            def is_valid(subset_hand_objects):
                if is_meld(subset_hand_objects) or is_run(subset_hand_objects):
                    return True
                return False

            # take cards from table
            if type(new_card) == str:
                if new_card[0] == "J":
                    new_card = Card(rank = 11, suit = new_card[1])
                elif new_card[0] == "Q":
                    new_card = Card(rank = 12, suit = new_card[1])
                elif new_card[0] == "K":
                    new_card = Card(rank = 13, suit = new_card[1])
                elif new_card[0] == "A":
                    new_card = Card(rank = 14, suit = new_card[1])
                elif new_card[0] == "1" and new_card[1] == "0":
                    new_card = Card(rank = 10, suit = new_card[2])
                else:
                    new_card = Card(rank = int(new_card[0]), suit = new_card[1])
            # take cards off the table
            old_cards = self.table.cards_on_table[:]
            new_cards = self.table.pickup_cards_on_table(new_card)
            # put cards in player's hand
            old_hand = player.cards_in_hand[:]
            for card in new_cards:
                player.pick(card)
                first_card = card
                               
            # sort new hand
            player.cards_in_hand = sort_subset(player.cards_in_hand, player.method)            
        
            # check every combination of cards in the player's hand
            ## check every combination of cards on the table
            potential_hand = player.cards_in_hand
            if len(new_cards) == 1:
                is_valid_pick = True
                player.cards_in_hand = potential_hand
                player.sort_by(player.cards_in_hand, player.method)
                return (is_valid_pick, must_put_down_points)
            if len(new_cards) > 1:
                for L in range(0, len(potential_hand) + 1):
                    for subset_hand in itertools.combinations(potential_hand, L):
                        if first_card in subset_hand:
                            if is_valid(subset_hand):
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
        card = input("Choose a card in your hand to discard. ")
        cards_to_choose_from = [str(card) for card in player.cards_in_hand]
        while card not in cards_to_choose_from:
            print("Invalid entry. Please choose a card that is currently in your hand. \n")
            card = input()
            
        # add card to table
        self.table.place_card_on_table(card)
        
        # remove card from player's hand
        if type(card) == str:
            if card[0] == "J":
                card = Card(rank = 11, suit = card[1])
            elif card[0] == "Q":
                card = Card(rank = 12, suit = card[1])
            elif card[0] == "K":
                card = Card(rank = 13, suit = card[1])
            elif card[0] == "A":
                card = Card(rank = 14, suit = card[1])
            elif card[0] == "1" and card[1] == "0":
                card = Card(rank = 10, suit = card[2])
            else:
                card = Card(rank = int(card[0]), suit = card[1])
                
        player.discard(card)
        player.sort_by(player.cards_in_hand, player.method)
    
    
    def table_cards(self, player, required_card):
        cards = input("Choose cards to place on table for points. Separate by commas. ")
        cards = cards.strip()
        cards = cards.split(', ')
        cards_to_choose_from = [str(card) for card in player.cards_in_hand]
        # cards chosen must be in hand
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
                return
            cards = cards.strip()
            cards = cards.split(', ')
        
        # cards is list of str(cards), cards_objects is list of cards 
        cards_objects = []
        for card in cards:
            if type(card) == str:
                if card[0] == "J":
                    card = Card(rank = 11, suit = card[1])
                elif card[0] == "Q":
                    card = Card(rank = 12, suit = card[1])
                elif card[0] == "K":
                    card = Card(rank = 13, suit = card[1])
                elif card[0] == "A":
                    card = Card(rank = 14, suit = card[1])
                elif card[0] == "1" and card[1] == "0":
                    card = Card(rank = 10, suit = card[2])
                else:
                    card = Card(rank = int(card[0]), suit = card[1])
            cards_objects.append(card)
            
        def sort_subset(hand, method):
            if method == "suit":
                sorted_hand = []
                s = []
                h = []
                d = []
                c = []
                for card in hand:
                    if card.suit == 'S':
                        s.append(card)
                    elif card.suit == 'H':
                        h.append(card)
                    elif card.suit == 'D':
                        d.append(card)
                    else:
                        c.append(card)
                sorted_s = sorted(s)
                sorted_h = sorted(h)
                sorted_d = sorted(d)
                sorted_c = sorted(c)
                sorted_hand = sorted_s + sorted_h + sorted_d + sorted_c
                return sorted_hand
            else:
                sorted_hand = sorted(hand)
                return sorted_hand
            
        def is_run(subset_hand):
            if len(subset_hand) < 3:
                return False
            
            same_suit = True
            for i in range(len(subset_hand) - 1):
                same_suit = same_suit and (subset_hand[i].suit == subset_hand[i + 1].suit)
            if not same_suit:
                return False

            sorted_subset_hand = sort_subset(subset_hand, method = "rank")
            rank_order = True
            for i in range(len(subset_hand) - 1):
                if subset_hand[i].rank == 14:
                    if (rank_order and (subset_hand[i].rank == subset_hand[i + 1].rank - 1)) == False:
                        if (rank_order and (1 == subset_hand[i + 1].rank - 1)) == False:
                            rank_order = False
                rank_order = rank_order and (subset_hand[i].rank == subset_hand[i + 1].rank - 1)
            if not rank_order:
                return False
            return True
            
        def is_meld(subset_hand):
            if len(subset_hand) < 3 or len(subset_hand) > 4:
                return False
            for i in range(len(subset_hand) - 1):
                if subset_hand[i].rank != subset_hand[i + 1].rank:
                    return False
            return True
        
        def is_valid(subset_hand, subset_hand_objects):
            if len(set(subset_hand)) != len(subset_hand): # repeated card
                print("Invalid. Cards cannot be repeated")
                return False
            if is_meld(subset_hand_objects) or is_run(subset_hand_objects):
                return True
            return False
        
        if is_valid(cards, cards_objects):
            cards_to_keep = []
            # place cards into player's cards on table
            for card in cards_objects:
                player.cards_on_table.append(card)
            # remove cards from player's hand
            for card in player.cards_in_hand:
                if card not in cards_objects:
                    cards_to_keep.append(card)
            player.cards_in_hand = cards_to_keep
            player.sort_by(player.cards_in_hand, player.method)
            return True
        else:
            return False
                 
 
    # simulate the play of rummy
    def play(self):
        winner = 0
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
            if not must_put_down_points:
                ask = input("Do you want to put down point cards? ")
                while ask != "yes" and ask != "no":
                    print("Invalid entry. Please answer 'yes' or 'no'. \n")
                    ask = input()
            else:
                ask = "yes"
            if ask == "yes": 
                multiple = True
                while multiple:
                    # table cards
                    cards_tabled = self.table_cards(player, required_card)
                    if cards_tabled == True and player.win_round():
                        multiple = False
                        winner = i + 1
                        return winner
                    if cards_tabled == False and must_put_down_points == False: # cards chosen incorrectly
                        ask = input("Try again? ")
                        while ask != "yes" and ask != "no":
                            print("Invalid entry. Please answer 'yes' or 'no'. \n")
                            ask = input()
                        if ask == "no":
                            multiple = False
                    elif cards_tabled == False and must_put_down_points: # cards chosen incorrectly but must point down points
                        print("Try again.")
                    else:
                        ask = input("Do you have another set of cards to put down for points? \n")
                        while ask != "yes" and ask != "no":
                            print("Invalid entry. Please answer 'yes' or 'no'. \n")
                            ask = input()
                        if ask == "no":
                            multiple = False

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
            
        return 0
            
    def play_to_win(self):
        winner = 0
        while winner == 0:
            winner = self.play()
            if winner != 0:
                print("Winner is player ", winner, " !")
                winner = True
    
    
            
def main():
    # prompt the user to enter the number of plaers
    num_players = int (input ('Enter number of players: '))
    while ((num_players < 2) or (num_players > 4)):
        num_players = int (input ('Enter number of players: '))

    # create the Poker object
    game = Rummy(num_players)

    # play the game
    game.play_to_win()

main()

