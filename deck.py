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
        return None if not self.deck else self.deck.pop()
    
    def pop(self):
        return self.deal()
        
    def __len__(self):
        return len(self.deck)