from CommonFunctions import str_to_card
from card import Card
from deck import Deck

class Table(object):
    
    def __init__(self, cards_in_pile = [], cards_on_table = []):
        self.cards_in_pile = cards_in_pile
        self.cards_on_table = cards_on_table
        
    def place_card_on_table(self, card):
        if type(card) == str:
            card = str_to_card(card)
        self.cards_on_table.append(card)
    
    def pickup_cards_on_table(self, card):
        # put cards in hand
        to_pickup = []
        for card_on_table in reversed(self.cards_on_table):
            to_pickup.append(card_on_table)
            if card_on_table == card:
                break
        # remove cards from table
        for _ in range(len(to_pickup)):
            self.cards_on_table.pop()
        return to_pickup
                
    def pickup_card_from_pile(self):
        return None if not self.cards_in_pile else self.cards_in_pile.pop()            
            
    def __str__(self):
        cards_on_table = ' '.join(str(card) for card in self.cards_on_table)
        return "Cards on table: " + cards_on_table
    
    def get_cards_on_table(self):
        paths = [card.image_path() for card in self.cards_on_table]
        return paths