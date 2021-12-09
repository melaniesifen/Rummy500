from unittest import main, TestCase
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CommonFunctions import *
from card import Card
from table import Table

class TestTableModel(TestCase):
    
    # ----------------------------------------------
    # place card on table --------------------------
    # ----------------------------------------------
    
    def test_place_card_on_table(self):
        table = Table()
        card = Card(2, "S")
        table.place_card_on_table(card)
        self.assertEqual(table.cards_on_table, [card])
    
    # ----------------------------------------------
    # test pick card methods -----------------------
    # ---------------------------------------------- 
    
    def test_pickup_card_from_table(self):
        cards_on_table = [Card(2, "C"), Card(3, "C"), Card(5, "D"), Card(4, "S")]
        table = Table(cards_in_pile=[], cards_on_table=cards_on_table)
        card = Card(3, "C")
        table.pickup_cards_on_table(card)
        self.assertEqual(table.cards_on_table, [Card(2, "C")])
        
    def test_pickup_card_from_pile(self):
        cards_in_pile = [Card(2, "S")]
        table = Table(cards_in_pile=cards_in_pile)
        card = table.pickup_card_from_pile()
        self.assertEqual(card, Card(2, "S"))
        self.assertEqual(table.cards_in_pile, [])
        
    def test_pickup_card_from_empty_pile(self):
        table = Table()
        card = table.pickup_card_from_pile()
        self.assertIsNone(card)
     
    
if __name__ == "__main__":
    main()