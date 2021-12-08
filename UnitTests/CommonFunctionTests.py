from collections import defaultdict
from unittest import main, TestCase
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CommonFunctions import *
from card import Card

class TestCPUModel(TestCase):
    
    # ----------------------------------------------
    # melds and run tests --------------------------
    # ----------------------------------------------
    
    # should always maximize points and minimize excess where possible
    def test_is_meld_should_return_false_if_not_enough_cards(self):
        cards = [Card(2, "H"), Card(2, "C")]
        self.assertFalse(is_meld(cards))
    
    def test_is_meld_should_return_false_if_too_many_cards(self):
        cards = [Card(2, "H"), Card(2, "C"), Card(2, "S"), Card(2, "D"), Card(2, "H")]
        self.assertFalse(is_meld(cards))
    
    def test_is_meld_should_return_true_for_meld(self):
        cards = [Card(2, "H"), Card(2, "C"), Card(2, "S"), Card(2, "D")]
        self.assertTrue(is_meld(cards))
        
    def test_is_run_should_return_false_if_not_enough_cards(self):
        cards = [Card(2, "H"), Card(3, "H")]
        self.assertFalse(is_run(cards))
        
    def test_is_run_should_return_false_if_not_matching_suits(self):
        cards = [Card(2, "H"), Card(3, "H"), Card(4, "H"), Card(5, "C")]
        self.assertFalse(is_run(cards))
        
    def test_is_run_should_return_false_if_not_run(self):
        cards = [Card(2, "H"), Card(4, "H"), Card(5, "H")]
        self.assertFalse(is_run(cards))
        
    def test_is_run_should_return_false_for_run_with_high_ace_and_wrapping_two(self):
        cards = [Card(12, "H"), Card(13, "H"), Card(14, "H"), Card(2, "H")]
        self.assertFalse(is_run(cards))
        
    def test_is_run_should_return_true_for_run_with_high_ace(self):
        cards = [Card(12, "H"), Card(13, "H"), Card(14, "H")]
        self.assertTrue(is_run(cards))
    
    def test_is_run_should_return_true_for_run_with_low_ace(self):
        cards = [Card(2, "H"), Card(3, "H"), Card(14, "H")]
        self.assertTrue(is_run(cards))
        
    def test_is_valid_should_return_true_if_run(self):
        cards = [Card(2, "H"), Card(3, "H"), Card(14, "H")]
        self.assertTrue(is_valid(cards))
    
    def test_is_valid_should_return_true_if_meld(self):
        cards = [Card(2, "H"), Card(2, "C"), Card(2, "S"), Card(2, "D")]
        self.assertTrue(is_valid(cards))
        
        
    # ----------------------------------------------
    # sorting cards tests --------------------------
    # ----------------------------------------------
    
    def test_sort_by_suit(self):
        cards = [Card(3, "S"), Card(5, "D"), Card(2, "S"), Card(10, "C"), Card(3, "C")]
        sorted_cards = sort_by(cards, "suit")
        expected_result = [Card(3, "C"), Card(10, "C"), Card(5, "D"), Card(2, "S"), Card(3, "S")]
        self.assertEqual(sorted_cards, expected_result)
    
    def test_sort_by_rank(self):
        cards = [Card(3, "S"), Card(5, "D"), Card(2, "S"), Card(10, "C"), Card(3, "C")]
        sorted_cards = sort_by(cards, "rank")
        expected_result = [Card(2, "S"), Card(3, "S"), Card(3, "C"), Card(5, "D"), Card(10, "C")]
        self.assertEqual(sorted_cards, expected_result)
        
    # ----------------------------------------------
    # str to card tests ----------------------------
    # ----------------------------------------------
        
    def test_str_to_card(self):
        two_of_spades = "2S"
        ten_of_diamonds = "10D"
        ace_of_clubs = "AC"
        queen_of_hearts = "QH"
        card_two_of_spades = str_to_card(two_of_spades)
        card_ten_of_diamonds = str_to_card(ten_of_diamonds)
        card_ace_of_clubs = str_to_card(ace_of_clubs)
        card_queen_of_hearts = str_to_card(queen_of_hearts)
        self.assertEqual(card_two_of_spades, Card(2, "S"))
        self.assertEqual(card_ten_of_diamonds, Card(10, "D"))
        self.assertEqual(card_ace_of_clubs, Card(14, "C"))
        self.assertEqual(card_queen_of_hearts, Card(12, "H"))
        
    # ----------------------------------------------
    # calculate points -----------------------------
    # ----------------------------------------------
        
    def test_calculate_points(self):
        cards = [Card(2, "S"), Card(10, "D"), Card(14, "H")]
        self.assertEqual(calculate_points(cards), 30)
        
if __name__ == "__main__":
    main()
        
    
        