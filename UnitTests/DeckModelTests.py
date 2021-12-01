from unittest import main, TestCase
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from deck import Deck
from card import Card

class TestDeckModel(TestCase):
        
    # ----------------------------------------------
    # deck dealing tests ---------------------------
    # ----------------------------------------------  
    
    def test_deal_should_return_card_object(self):
        deck = Deck()
        card = deck.deal()
        self.assertEqual(card, Card(2, "C"))
        
    def test_empty_deck_should_return_none(self):
        deck = Deck()
        for _ in range(52):
            deck.deal()
        card = deck.deal()
        self.assertIsNone(card)
        
if __name__ == "__main__":
    main()

