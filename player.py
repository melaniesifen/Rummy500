from card import Card
from CommonFunctions import _sort_by, str_to_card

class Player(object):
    
    def __init__(self, cards_in_hand, cards_on_table, method = "suit", points = 0):
        self.cards_in_hand = cards_in_hand
        self.cards_on_table = cards_on_table
        self.method = method
        self.points = points
        self.winner = False
     
    def set_winner(self):
        # switch
        winner = self.winner
        self.winner = not winner
        
    def get_method(self):
        return self.method
    
    def set_method(self, method):
        self.method = method
        
    def get_cards_in_hand(self):
        paths = []
        for card in self.cards_in_hand:
            paths.append(card.image_path())
        return paths
    
    def get_cards_on_table(self):
        paths = []
        for card_list in self.cards_on_table:
            path_list = []
            for card in card_list:
                path_list.append(card.small_image_path())
            paths.append(path_list)
        return paths
        
        
    def pick(self, card):
        self.cards_in_hand.append(card)
    
    def discard(self, card):
        self.cards_in_hand.remove(card)
        
    def calculate_points(self, hand):
        count = 0
        for card in hand:
            if card.rank < 10:
                count += 5
            elif card.rank < 14:
                count += 10
            else: # Ace
                count += 15
        return count
                
    def end_points(self):
        cards_on_table = [card for points in self.cards_on_table for card in points]
        new_points = self.calculate_points(cards_on_table) - self.calculate_points(self.cards_in_hand)
        if self.winner:
            new_points += 25 # 25 points for winning the round
        self.points += new_points
        return new_points
    
    def round_winner(self):
        if len(self.cards_in_hand) == 0:
            self.winner = True
            return True
        return False
    
    def game_winner(self):
        if self.round_winner():
            cards_on_table = [card for points in self.cards_on_table for card in points]
            new_points = self.calculate_points(cards_on_table) + self.points + 25
            if new_points >= 500:
                return True
        return False
    
    def __str__(self):
        cards_in_hand = ' '.join(str(card) for card in self.cards_in_hand)
        return "Cards in hand: " + cards_in_hand
    
    def sort_by(self, hand, method):
        _sort_by(self, self.cards_in_hand, self.method)