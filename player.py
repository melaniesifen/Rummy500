from card import Card
from CommonFunctions import sort_by, calculate_points

class Player(object):
    
    def __init__(self, cards_in_hand = [], cards_on_table = [], method = "suit", points = 0):
        self.cards_in_hand = cards_in_hand
        self.cards_on_table = cards_on_table
        self.method = method
        self.points = points
        self.winner = False
     
    def set_winner(self):
        # switch
        self.winner = not self.winner
        
    def get_method(self):
        return self.method
    
    def set_method(self, method):
        if method == "suit" or method == "rank":
            self.method = method
        
    def get_cards_in_hand(self):
        paths = []
        for card in self.cards_in_hand:
            paths.append(card.image_path())
        return paths
    
    def get_cards_on_table(self):
        paths = []
        for card_list in self.cards_on_table:
            path_list = [card.small_image_path() for card in card_list]
            paths.append(path_list)
        return paths
        
    def pick(self, card):
        self.cards_in_hand.append(card)
    
    def discard(self, card):
        self.cards_in_hand.remove(card)
                
    def end_points(self):
        # cards_on_table = [card for points in self.cards_on_table for card in points]
        new_points = calculate_points(self.cards_on_table) - calculate_points(self.cards_in_hand)
        if self.winner:
            new_points += 25 # 25 points for winning the round
        self.points += new_points
        return new_points
    
    def round_winner(self):
        if not self.cards_in_hand:
            self.winner = True
        return self.winner
    
    def game_winner(self):
        if self.round_winner():
            cards_on_table = [card for points in self.cards_on_table for card in points]
            new_points = calculate_points(cards_on_table) + self.points + 25
            if new_points >= 500:
                return True
        return False
    
    def __str__(self):
        cards_in_hand = ' '.join(str(card) for card in self.cards_in_hand)
        return "Cards in hand: " + cards_in_hand
    
    def sort_by(self, hand, method):
        self.cards_in_hand = sort_by(self.cards_in_hand, self.method)