from card import Card

def _sort_by(self = None, hand = [], method = "suit"):
    if method == "suit":
        if not self:
            hand = [str_to_card(card) for card in hand]
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
        if self:
            self.cards_in_hand = sorted_hand
        else:
            sorted_hand = [str(card) for card in sorted_hand]
            return sorted_hand
    else:
        if not self:
            hand = [str_to_card(card) for card in hand]
            sorted_hand = sorted(hand)
            return sorted_hand
        else:
            sorted_hand = sorted(hand)
            self.cards_in_hand = sorted_hand

def is_run(subset_hand):
    if len(subset_hand) < 3:
        return False

    same_suit = True
    for i in range(len(subset_hand) - 1):
        same_suit = same_suit and (subset_hand[i].suit == subset_hand[i + 1].suit)
    if not same_suit:
        return False

    sorted_subset_hand = _sort_by(subset_hand, method = "rank")
    rank_order = True
    for i in range(len(subset_hand) - 1):
        if subset_hand[i].rank == 14:
            rank_order = False
        if subset_hand[i + 1].rank == 14:
            if (rank_order and (subset_hand[i].rank == subset_hand[i + 1].rank - 1)) == False:
                if (rank_order and (subset_hand[0].rank == 2)) == False:
                    rank_order = False
        rank_order = rank_order and (subset_hand[i].rank == subset_hand[i + 1].rank - 1)
    if not rank_order:
        return False
    return True

def is_meld(subset_hand):
    if len(subset_hand) < 3 or len(subset_hand) > 4:
        return False
    for i in range(len(subset_hand) - 1):
        if subset_hand[i].rank != subset_hand[i + 1].rank:
            return False
    return True

def str_to_card(card):
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
    return card
