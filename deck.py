from card import Card
import random

class Deck(object):
    def __init__(self):
        self.deck = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                card = Card(rank, suit)
                self.deck.append(card)
                
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        if len(self.deck) == 0:
            return None
        else:
            return self.deck.pop(0)
        
    def __len__(self):
        count = 0
        for card in self.deck:
            count += 1
        return count