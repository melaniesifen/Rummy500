class Card(object):
    
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    SUITS = ('C', 'D', 'H', 'S')
        
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

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

    def __hash__(self):
        return hash(str(self))
    
    # equality tests
    def __eq__(self, other):
        if type(other) == str:
            raise TypeError(f"string type of {other} cannot be compared to card type")
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

    def small_image_path(self):
        if self.rank == 2:
            if self.suit == "C":
                return "images/PNG-cards-1.3/2_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/2_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/2_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/2_of_spades (Custom).png"
        if self.rank == 3:
            if self.suit == "C":
                return "images/PNG-cards-1.3/3_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/3_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/3_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/3_of_spades (Custom).png"
        if self.rank == 4:
            if self.suit == "C":
                return "images/PNG-cards-1.3/4_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/4_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/4_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/4_of_spades (Custom).png"
        if self.rank == 5:
            if self.suit == "C":
                return "images/PNG-cards-1.3/5_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/5_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/5_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/5_of_spades (Custom).png"
        if self.rank == 6:
            if self.suit == "C":
                return "images/PNG-cards-1.3/6_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/6_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/6_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/6_of_spades (Custom).png"
        if self.rank == 7:
            if self.suit == "C":
                return "images/PNG-cards-1.3/7_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/7_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/7_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/7_of_spades (Custom).png"
        if self.rank == 8:
            if self.suit == "C":
                return "images/PNG-cards-1.3/8_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/8_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/8_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/8_of_spades (Custom).png"
        if self.rank == 9:
            if self.suit == "C":
                return "images/PNG-cards-1.3/9_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/9_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/9_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/9_of_spades (Custom).png"
        if self.rank == 10:
            if self.suit == "C":
                return "images/PNG-cards-1.3/10_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/10_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/10_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/10_of_spades (Custom).png"
        if self.rank == 11:
            if self.suit == "C":
                return "images/PNG-cards-1.3/jack_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/jack_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/jack_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/jack_of_spades (Custom).png"
        if self.rank == 12:
            if self.suit == "C":
                return "images/PNG-cards-1.3/queen_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/queen_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/queen_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/queen_of_spades (Custom).png"
        if self.rank == 13:
            if self.suit == "C":
                return "images/PNG-cards-1.3/king_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/king_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/king_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/king_of_spades (Custom).png"
        if self.rank == 14:
            if self.suit == "C":
                return "images/PNG-cards-1.3/ace_of_clubs (Custom).png"
            if self.suit == "D":
                return "images/PNG-cards-1.3/ace_of_diamonds (Custom).png"
            if self.suit == "H":
                return "images/PNG-cards-1.3/ace_of_hearts (Custom).png"
            return "images/PNG-cards-1.3/ace_of_spades (Custom).png"
        
    def path_to_card(self, path):
        if path[0] == "a":
            self.rank = 14
        elif path[0] == "k":
            self.rank = 13
        elif path[0] == "q":
            self.rank = 12
        elif path[0] == "j":
            self.rank = 11
        elif path[0] == "1":
            self.rank = 10
        else:
            self.rank = int(path[0])
        if path[-2] == "e":
            self.suit = "S"
        elif path[-2] == "t":
            self.suit = "H"
        elif path[-2] == "d":
            self.suit = "D"
        else:
            self.suit = "C"
        return Card(self.rank, self.suit)
        
        