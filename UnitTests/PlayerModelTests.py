from unittest import main, TestCase
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from player import Player
from card import Card

class TestPlayerModel(TestCase):
    
    # ----------------------------------------------
    # setter method tests --------------------------
    # ----------------------------------------------
    
    def test_set_winner_should_switch(self):
        # not equal as equality implies same suit
        player = Player()
        player.set_winner()
        self.assertTrue(player.winner)
        player.set_winner()
        self.assertFalse(player.winner)
        
    def test_set_method_should_switch_only_valid_method(self):
        player = Player()
        player.set_method("rank")
        self.assertEqual(player.method, "rank")
        player.set_method("test")
        self.assertNotEqual(player.method, "test")
        
    # ----------------------------------------------
    # get cards in hand ----------------------------
    # ----------------------------------------------
    
    def test_card_paths_in_hand(self):
        player = Player([Card(2, "S")])
        self.assertEqual(player.get_cards_in_hand(), ["images/PNG-cards-1.3/2_of_spades.png"])
        
    def test_card_paths_on_table(self):
        player = Player([], cards_on_table=[[Card(2, "S")]])
        self.assertEqual(player.get_cards_on_table(), [["images/PNG-cards-1.3/2_of_spades (Custom).png"]])
    
    # ----------------------------------------------
    # point calculation tests ----------------------
    # ----------------------------------------------
    
    def test_end_points_should_calculate_and_set_points(self):
        player = Player(cards_in_hand = [Card(14, "S")], cards_on_table = [Card(10, "S")])
        player.end_points()
        self.assertEqual(player.points, -5)
        
    def test_end_points_should_calculate_and_set_points_and_extra_points_for_winner(self):
        player = Player(cards_in_hand = [Card(14, "S")], cards_on_table = [Card(10, "S")])
        player.set_winner()
        player.end_points()
        self.assertEqual(player.points, 20)
        
    def test_end_points_should_calculate_and_set_points_with_old_points(self):
        player = Player(cards_in_hand = [Card(14, "S")], cards_on_table = [Card(10, "S")], method="suit", points = 10)
        player.end_points()
        self.assertEqual(player.points, 5)
        
    # ----------------------------------------------
    # winner tests ---------------------------------
    # ----------------------------------------------
    
    def test_round_winner(self):
        player = Player()
        winner = player.round_winner()
        self.assertTrue(winner)
        
    def test_game_winner(self):
        player = Player(cards_in_hand=[], cards_on_table=[], method="suit", points=495)
        self.assertTrue(player.game_winner())
        
    # ----------------------------------------------
    # card sorting test ----------------------------
    # ----------------------------------------------
    
    def test_sort(self):
        player = Player()
        player.pick(Card(2, "S"))
        player.pick(Card(4, "C"))
        player.pick(Card(5, "S"))
        player.sort_by()
        self.assertEqual([Card(4, "C"), Card(2, "S"), Card(5, "S")], player.cards_in_hand)
        
if __name__ == "__main__":
    main()

