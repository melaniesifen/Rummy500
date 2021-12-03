from unittest import main, TestCase
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from player import Player
from cpu import CPU
from card import Card

class TestCPUModel(TestCase):
    
    # ----------------------------------------------
    # determine best pickup greedy tests -----------
    # ----------------------------------------------
    
    # should always maximize points and minimize excess where possible
    def test_determine_best_pickup_meld1(self):
        cards_on_table = [Card(2, "D"), Card(13, "S"), Card(11, "H"), Card(2, "H"), Card(2, "C")]
        cards_in_hand = [Card(2, "S")]
        hand = [(Card(2, "D"), Card(2, "H"), Card(2, "S")), (Card(2, "D"), Card(2, "C"), Card(2, "S")), \
            (Card(2, "H"), Card(2, "C"), Card(2, "S")), (Card(2, "D"), Card(2, "H"), Card(2, "S"), Card(2, "C"))]
        best_pickup = CPU().determine_best_pickup_greedy(hand, cards_on_table)
        # should pick up all to make meld
        self.assertEqual(best_pickup, Card(2, "D"))
        
    # should always maximize points and minimize excess where possible
    def test_determine_best_pickup_meld2(self):
        cards_on_table = [Card(2, "D"), Card(13, "S"), Card(11, "H"), Card(2, "C")]
        cards_in_hand = [Card(2, "S")]
        hand = [(Card(2, "D"), Card(2, "C"), Card(2, "S"))]
        best_pickup = CPU().determine_best_pickup_greedy(hand, cards_on_table)
        # should pick up all to make meld
        self.assertEqual(best_pickup, Card(2, "D"))
        
    # should always maximize points and minimize excess where possible
    def test_determine_best_pickup_meld3(self):
        cards_on_table = [Card(13, "S"), Card(11, "H"), Card(2, "C")]
        # cards_in_hand = [Card(2, "S"), Card(2, "D")]
        hand = [(Card(2, "D"), Card(2, "C"), Card(2, "S"))]
        best_pickup = CPU().determine_best_pickup_greedy(hand, cards_on_table)
        # should pick up all to make meld
        self.assertEqual(best_pickup, Card(2, "C"))
        
    def test_determine_best_pickup_meld4(self):
        cards_on_table = [Card(2, "H"), Card(10, "D"), Card(11, "H"), Card(7, "C"), \
            Card(14, "S"), Card(14, "C"), Card(12, "C"), \
            Card(11, "D"), Card(3, "S"), Card(2, "D")]
        # cards_in_hand = [Card(2, "S"), Card(14, "D")]
        hand = [(Card(2, "D"), Card(2, "H"), Card(2, "S")), \
            (Card(14, "C"), Card(14, "S"), Card(14,"D"))]
        best_pickup = CPU().determine_best_pickup_greedy(hand, cards_on_table)
        self.assertTrue(best_pickup == Card(2, "H"))
        
    def test_determine_best_pickup_run(self):
        cards_on_table = [Card(2, "H"), Card(10, "D"), Card(11, "D"), Card(7, "C"), \
            Card(14, "S"), Card(14, "C"), Card(12, "C"), \
            Card(11, "D"), Card(3, "S"), Card(2, "D")]
        # cards_in_hand = [Card(12, "D"), Card(13, "D")]
        hand = [(Card(10, "D"), Card(11, "D"), Card(12, "D"), Card(13, "D"))]
        best_pickup = CPU().determine_best_pickup_greedy(hand, cards_on_table)
        self.assertTrue(best_pickup == Card(10, "D"))
        
    def test_determine_best_pickup_meld_and_run(self):
        cards_on_table = [Card(2, "H"), Card(10, "D"), Card(11, "D"), Card(7, "C"), \
            Card(14, "S"), Card(14, "C"), Card(12, "C"), \
            Card(11, "D"), Card(3, "S"), Card(2, "D")]
        # cards_in_hand = [Card(12, "D"), Card(13, "D"), Card(2, "C")]
        hand = [(Card(10, "D"), Card(11, "D"), Card(12, "D"), Card(13, "D")), \
            (Card(2, "H"), Card(2, "D"), Card(2, "C"))]
        best_pickup = CPU().determine_best_pickup_greedy(hand, cards_on_table)
        self.assertTrue(best_pickup == Card(2, "H"))
        
    # ----------------------------------------------
    # pickup options tests -------------------------
    # ----------------------------------------------

    def test_greedy_pickup_should_be_pile_if_no_cards_to_pickup(self):
        tabled_cards, all_melds, all_runs = [], [], []
        cpu = CPU()
        result = cpu.pickup_options(tabled_cards, all_melds, all_runs)
        self.assertEqual(result, "pile")
  
    def test_greedy_pickup_add_to_cards_in_hand(self):
        all_melds, all_runs = [], []
        tabled_cards = [Card(12, "S"), Card(14, "D"), Card(5, "S")]
        cards_in_hand = [Card(14, "S"), Card(14, "C"), Card(2, "D"), Card(4, "D")]
        cpu = CPU(cards_in_hand=cards_in_hand)
        result = cpu.pickup_options(tabled_cards, all_melds, all_runs)
        self.assertEqual(result, Card(14, "D"))
    
    def test_greedy_pickup_add_to_cards_in_all_melds(self):
        all_melds, all_runs = [[Card(12, "C"), Card(12, "H"), Card(12, "D")]], []
        tabled_cards = [Card(12, "S"), Card(14, "D"), Card(5, "S")]
        cards_in_hand = [Card(14, "S"), Card(2, "D"), Card(4, "D")]
        cpu = CPU(cards_in_hand=cards_in_hand)
        result = cpu.pickup_options(tabled_cards, all_melds, all_runs)
        self.assertEqual(result, Card(12, "S"))
    
    def test_greedy_pickup_add_to_cards_in_all_runs(self):
        all_melds, all_runs = [], [[Card(11, "C"), Card(12, "C"), Card(13, "C")]]
        tabled_cards = [Card(10, "C"), Card(14, "C"), Card(5, "S")]
        cards_in_hand = [Card(14, "S"), Card(2, "D"), Card(4, "D")]
        cpu = CPU(cards_in_hand=cards_in_hand)
        result = cpu.pickup_options(tabled_cards, all_melds, all_runs)
        self.assertEqual(result, Card(10, "C"))
        
    def test_greedy_pickup_add_to_cards_in_all_runs_and_hand(self):
        all_melds, all_runs = [], [[Card(11, "C"), Card(12, "C"), Card(13, "C")]]
        tabled_cards = [Card(9, "C")]
        cards_in_hand = [Card(10, "C")]
        cpu = CPU(cards_in_hand=cards_in_hand)
        result = cpu.pickup_options(tabled_cards, all_melds, all_runs)
        self.assertEqual(result, Card(9, "C"))
        
    def test_greedy_pickup_add_to_cards_from_tabled_cards(self):
        all_melds, all_runs = [], []
        tabled_cards = [Card(10, "C"), Card(11, "C"), Card(12, "C")]
        cards_in_hand = [Card(2, "D")]
        cpu = CPU(cards_in_hand=cards_in_hand)
        result = cpu.pickup_options(tabled_cards, all_melds, all_runs)
        self.assertEqual(result, Card(10, "C"))
    
    # ----------------------------------------------
    # table cards tests ----------------------------
    # ----------------------------------------------
    
    def test_should_choose_best_possible_cards(self):
        options = [[Card(10, "C"), Card(11, "C"), Card(12, "C")], \
            [Card(10, "D"), Card(10, "H"), Card(10, "C")], \
            [Card(2, "C"), Card(2, "D"), Card(2, "H")], \
            [Card(2, "C"), Card(3, "C"), Card(4, "C")], [Card(2, "D")]]
        result_options = CPU().choose_cards_strategy_greedy(options)
        expected_outcome = [
            [[Card(10, "C"), Card(11, "C"), Card(12, "C")], [Card(2, "C"), Card(3, "C"), Card(4, "C")], [Card(2, "D")]],
            [[Card(10, "D"), Card(10, "H"), Card(10, "C")], [Card(2, "C"), Card(3, "C"), Card(4, "C")], [Card(2, "D")]]
            ]
        self.assertTrue(result_options in expected_outcome)
        
    def test_choose_best_options_should_return_null_if_no_options(self):
        options = []
        result_options = CPU().choose_cards_strategy_greedy(options)
        self.assertIsNone(result_options)
        
    
        
    
if __name__ == "__main__":
    main()

