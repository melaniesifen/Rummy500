from card import Card

class Player(object):
    
    def __init__(self, cards_in_hand, cards_on_table, method = "suit", points = 0):
        self.cards_in_hand = cards_in_hand
        self.cards_on_table = cards_on_table
        self.method = method
        self.points = points
        
    def get_method(self):
        return self.method
    
    def set_method(self, method):
        self.method = method
        
    def get_cards_in_hand(self):
        card_string = ' '.join(str(card) for card in self.cards_in_hand)
        return "Hand : " + card_string
    
    def get_cards_on_table(self):
        all_cards_on_table = []
        for points in self.cards_on_table:
            points_s = ', '.join(str(card) for card in points)
            all_cards_on_table.append(points_s)
        
        return "Point cards on table: " + ' | '.join(s for s in all_cards_on_table)
        
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
        self.points = self.calculate_points(cards_on_table) - self.calculate_points(self.cards_in_hand)
        return self.points
    
    def win_round(self):
        if len(self.cards_in_hand) == 0:
            return True
        return False
    
    def __str__(self):
        cards_in_hand = ' '.join(str(card) for card in self.cards_in_hand)
        return "Cards in hand: " + cards_in_hand
    
    def sort_by(self, hand, method):
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
            self.cards_in_hand = sorted_hand
        else:
            sorted_hand = sorted(hand)
            self.cards_in_hand = sorted_hand