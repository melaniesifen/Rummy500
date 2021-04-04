class Card(object):
    
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    
    SUITS = ('C', 'D', 'H', 'S')
    
    def __init__(self, rank = 12, suit = 'S'):
        if (rank in Card.RANKS):
            self.rank = rank
        else:
            self.rank = 12
        if (suit in Card.SUITS):
            self.suit = suit
        else:
            self.suit = 'S'

    # string representation of a Card object
    def __str__(self):
        if (self.rank == 14):
            rank = 'A'
        elif (self.rank == 13):
            rank = 'K'
        elif (self.rank == 12):
            rank = 'Q'
        elif (self.rank == 11):
            rank = 'J'
        else:
            rank = str(self.rank)
        return rank + self.suit

    # equality tests
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        return self.rank != other.rank or self.suit != other.suit

    def __lt__(self, other):
        return self.rank < other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __ge__(self, other):
        return self.rank >= other.rank
