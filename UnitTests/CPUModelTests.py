from collections import defaultdict
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
        # cards_in_hand = [Card(2, "S")]
        hand = [(Card(2, "D"), Card(2, "H"), Card(2, "S")), (Card(2, "D"), Card(2, "C"), Card(2, "S")), \
            (Card(2, "H"), Card(2, "C"), Card(2, "S")), (Card(2, "D"), Card(2, "H"), Card(2, "S"), Card(2, "C"))]
        best_pickup = CPU().determine_best_pickup_greedy(hand, cards_on_table)
        # should pick up all to make meld
        self.assertEqual(best_pickup, Card(2, "D"))
        
    # should always maximize points and minimize excess where possible
    def test_determine_best_pickup_meld2(self):
        cards_on_table = [Card(2, "D"), Card(13, "S"), Card(11, "H"), Card(2, "C")]
        # cards_in_hand = [Card(2, "S")]
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
        cpu = CPU(cards_in_hand = cards_in_hand)
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

    def test_should_choose_best_possible_cards(self):
        options = [[Card(10, "C"), Card(11, "C"), Card(12, "C")], \
            [Card(10, "D"), Card(10, "H"), Card(10, "C")], \
            [Card(2, "C"), Card(2, "D"), Card(2, "H")], \
            [Card(2, "C"), Card(3, "C"), Card(4, "C")], [Card(2, "D")]]
        hand = [Card(10, "C"), Card(11, "C"), Card(12, "C"),
                Card(10, "D"), Card(10, "H"),
                Card(2, "C"), Card(2, "D"), Card(2, "H"),
                Card(3, "C"), Card(4, "C")]
        result_options = CPU().choose_cards_strategy_greedy(options, hand)
        expected_outcome = [
            [[Card(10, "C"), Card(11, "C"), Card(12, "C")], [Card(2, "C"), Card(3, "C"), Card(4, "C")], [Card(2, "D")]],
            [[Card(10, "D"), Card(10, "H"), Card(10, "C")], [Card(2, "C"), Card(3, "C"), Card(4, "C")], [Card(2, "D")]]
            ]
        self.assertTrue(result_options in expected_outcome)
    
    def test_should_choose_best_possible_cards_with_required_card(self):
        options = [[Card(10, "C"), Card(11, "C"), Card(12, "C")], \
            [Card(10, "D"), Card(10, "H"), Card(10, "C")], \
            [Card(2, "C"), Card(2, "D"), Card(2, "H")], \
            [Card(2, "C"), Card(3, "C"), Card(4, "C")], [Card(2, "D")]]
        hand = [Card(10, "C"), Card(11, "C"), Card(12, "C"),
                Card(10, "D"), Card(10, "H"),
                Card(2, "C"), Card(2, "D"), Card(2, "H"),
                Card(3, "C"), Card(4, "C")]
        required_card = Card(10, "H")
        result_options = CPU().choose_cards_strategy_greedy(options, hand, required_card)
        expected_outcome = [[Card(10, "D"), Card(10, "H"), Card(10, "C")], [Card(2, "C"), Card(3, "C"), Card(4, "C")], [Card(2, "D")]]
        self.assertTrue(result_options == expected_outcome)
        
    def test_choose_best_options_should_return_null_if_no_options(self):
        options = []
        hand = [Card(2, "C")]
        result_options = CPU().choose_cards_strategy_greedy(options, hand)
        self.assertIsNone(result_options)
        
    def test_table_cards_strategy_should_give_all_valid_options(self):
        cards_in_hand = [Card(10, "C"), Card(2, "S"), Card(2, "H"), Card(2, "D")]
        all_melds = [[Card(10, "S"), Card(10, "H"), Card(10, "D")]]
        all_runs = [[Card(11, "C"), Card(12, "C"), Card(13, "C")]]
        cpu = CPU(cards_in_hand = cards_in_hand)
        options_dict = cpu.table_cards_strategy(cards_in_hand, all_melds, all_runs)
        expected_outcome = [
            {(Card(10, "S"), Card(10, "H"), Card(10, "D"), Card(10, "C")) : [[Card(10, "S"), Card(10, "H"), Card(10, "D")]],
             (Card(2, "S"), Card(2, "H"), Card(2, "D")) : [None]},
            {(Card(10, "C"), Card(11, "C"), Card(12, "C"), Card(13, "C")) : [[Card(11, "C"), Card(12, "C"), Card(13, "C")]],
             (Card(2, "S"), Card(2, "H"), Card(2, "D")) : [None]}
        ]
        options = defaultdict(list)
        for k, v in options_dict.items():
            k = sorted(list(k))
            options[tuple(k)] = v
        self.assertTrue(options in expected_outcome)
        
    def test_table_cards_strategy_should_give_all_valid_options_with_required_card(self):
        cards_in_hand = [Card(9, "C"), Card(10, "C"), Card(2, "S"), Card(2, "H"), Card(2, "D")]
        all_melds = [[Card(10, "S"), Card(10, "H"), Card(10, "D")]]
        all_runs = [[Card(11, "C"), Card(12, "C"), Card(13, "C")]]
        required_card = Card(9, "C")
        cpu = CPU(cards_in_hand = cards_in_hand)
        options_dict = cpu.table_cards_strategy(cards_in_hand, all_melds, all_runs, required_card = required_card)
        expected_outcome = {(Card(9, "C"), Card(10, "C"), Card(11, "C"), Card(12, "C"), Card(13, "C")) : [[Card(11, "C"), Card(12, "C"), Card(13, "C")]],
             (Card(2, "S"), Card(2, "H"), Card(2, "D")) : [None]}
        options = defaultdict(list)
        for k, v in options_dict.items():
            k = sorted(list(k))
            options[tuple(k)] = v
        self.assertTrue(options == expected_outcome)
        
    # ----------------------------------------------
    # discard tests --------------------------------
    # ----------------------------------------------
    
    def test_discard_greedy1(self):
        cards_on_table = [Card(10, "H")]
        all_melds = [[Card(2, "H"), Card(2, "C"), Card(2, "D")],
            [Card(5, "H"), Card(5, "C"), Card(5, "D")]]
        all_runs = [[Card(8, "C"), Card(9, "C"), Card(10, "C")]]
        cards_in_hand = [Card(2, "S"), Card(5, "S"), Card(12, "C"), Card(3, "D")]
        expected_discard = Card(3, "D")
        cpu = CPU(cards_in_hand=cards_in_hand)
        discard = cpu.discard_strategy_greedy(cards_on_table, all_melds, all_runs)
        self.assertEqual(discard, expected_discard)
    
    def test_discard_greedy2(self):
        cards_on_table = [Card(10, "H"), Card(3, "S")]
        all_melds = [[Card(2, "H"), Card(2, "C"), Card(2, "D")],
            [Card(5, "H"), Card(5, "C"), Card(5, "D")]]
        all_runs = [[Card(8, "C"), Card(9, "C"), Card(10, "C")]]
        cards_in_hand = [Card(2, "S"), Card(5, "S"), Card(12, "C"), Card(3, "D")]
        expected_discard = Card(12, "C")
        cpu = CPU(cards_in_hand=cards_in_hand)
        discard = cpu.discard_strategy_greedy(cards_on_table, all_melds, all_runs)
        self.assertEqual(discard, expected_discard)
        
    def test_discard_greedy3(self):
        cards_on_table = []
        all_melds = []
        all_runs = []
        cards_in_hand = [Card(2, "S"), Card(5, "C"), Card(12, "H"), Card(14, "D")]
        expected_discard = Card(2, "S")
        cpu = CPU(cards_in_hand=cards_in_hand)
        discard = cpu.discard_strategy_greedy(cards_on_table, all_melds, all_runs)
        self.assertEqual(discard, expected_discard)
        
if __name__ == "__main__":
    main()

