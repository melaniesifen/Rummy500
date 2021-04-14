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
    
    def image_path(self):
        if self.rank == 2:
            if self.suit == "C":
                return "images/PNG-cards-1.3/2_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/2_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/2_of_hearts.png"
            return "images/PNG-cards-1.3/2_of_spades.png"
        if self.rank == 3:
            if self.suit == "C":
                return "images/PNG-cards-1.3/3_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/3_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/3_of_hearts.png"
            return "images/PNG-cards-1.3/3_of_spades.png"
        if self.rank == 4:
            if self.suit == "C":
                return "images/PNG-cards-1.3/4_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/4_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/4_of_hearts.png"
            return "images/PNG-cards-1.3/4_of_spades.png"
        if self.rank == 5:
            if self.suit == "C":
                return "images/PNG-cards-1.3/5_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/5_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/5_of_hearts.png"
            return "images/PNG-cards-1.3/5_of_spades.png"
        if self.rank == 6:
            if self.suit == "C":
                return "images/PNG-cards-1.3/6_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/6_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/6_of_hearts.png"
            return "images/PNG-cards-1.3/6_of_spades.png"
        if self.rank == 7:
            if self.suit == "C":
                return "images/PNG-cards-1.3/7_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/7_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/7_of_hearts.png"
            return "images/PNG-cards-1.3/7_of_spades.png"
        if self.rank == 8:
            if self.suit == "C":
                return "images/PNG-cards-1.3/8_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/8_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/8_of_hearts.png"
            return "images/PNG-cards-1.3/8_of_spades.png"
        if self.rank == 9:
            if self.suit == "C":
                return "images/PNG-cards-1.3/9_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/9_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/9_of_hearts.png"
            return "images/PNG-cards-1.3/9_of_spades.png"
        if self.rank == 10:
            if self.suit == "C":
                return "images/PNG-cards-1.3/10_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/10_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/10_of_hearts.png"
            return "images/PNG-cards-1.3/10_of_spades.png"
        if self.rank == 11:
            if self.suit == "C":
                return "images/PNG-cards-1.3/jack_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/jack_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/jack_of_hearts.png"
            return "images/PNG-cards-1.3/jack_of_spades.png"
        if self.rank == 12:
            if self.suit == "C":
                return "images/PNG-cards-1.3/queen_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/queen_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/queen_of_hearts.png"
            return "images/PNG-cards-1.3/queen_of_spades.png"
        if self.rank == 13:
            if self.suit == "C":
                return "images/PNG-cards-1.3/king_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/king_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/king_of_hearts.png"
            return "images/PNG-cards-1.3/king_of_spades.png"
        if self.rank == 14:
            if self.suit == "C":
                return "images/PNG-cards-1.3/ace_of_clubs.png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/ace_of_diamonds.png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/ace_of_hearts.png"
            return "images/PNG-cards-1.3/ace_of_spades.png"
