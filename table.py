from card import Card
from deck import Deck

class Table(object):
    
    def __init__(self, cards_in_pile, cards_on_table):
        self.cards_in_pile = cards_in_pile
        self.cards_on_table = []
        first_card = self.cards_in_pile.deal()
        self.cards_on_table.append(first_card)
        
    def place_card_on_table(self, card):
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
        self.cards_on_table.append(card)
    
    def pickup_cards_on_table(self, card):
        # put cards in hand
        to_pickup = []
        reversed_cards_on_table = self.cards_on_table[::-1]
        for c in reversed_cards_on_table:
            to_pickup.append(c)
            if c == card:
                break
        
        # remove cards from table
        to_keep = []
        for c in self.cards_on_table:
            if c != card:
                to_keep.append(c)
            else:
                break
        self.cards_on_table = to_keep
        return to_pickup
                
        
    def pickup_card_from_pile(self):
        if len(self.cards_in_pile) == 0:
            return None
        else:
            new_card = self.cards_in_pile.deal()
            return new_card
            
            
    def __str__(self):
        cards_on_table = ' '.join(str(card) for card in self.cards_on_table)
        return "Cards on table: " + cards_on_table