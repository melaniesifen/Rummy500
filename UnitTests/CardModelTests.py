from unittest import main, TestCase
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from card import Card

class TestCardModel(TestCase):
    
    # ----------------------------------------------
    # card equality tests --------------------------
    # ----------------------------------------------
    
    def test_suits_should_be_lt_equal(self):
        # not equal as equality implies same suit
        ace_of_spades = Card(14, "S")
        ace_of_clubs = Card(14, "C")
        ace_of_diamonds = Card(14, "D")
        ace_of_hearts = Card(14, "H")
        self.assertTrue(ace_of_spades <= ace_of_clubs <= ace_of_diamonds <= ace_of_hearts)
    
    def test_ranks_equality(self):
        two_of_spades = Card(2, "S")
        two_of_diamonds = Card(2, "D")
        three_of_spades = Card(3, "S")
        ten_of_spades = Card(10, "S")
        ace_of_spades = Card(14, "S")
        self.assertTrue(two_of_spades <= two_of_diamonds < three_of_spades < ten_of_spades < ace_of_spades)
        
    # ----------------------------------------------
    # card image path tests ------------------------
    # ----------------------------------------------  
    
    def test_card_image_retrieval_path(self):
        two_of_spades = Card(2, "S")
        ten_of_spades = Card(10, "S")
        jack_of_clubs = Card(11, "C")
        self.assertEqual(two_of_spades.image_path(), "images/PNG-cards-1.3/2_of_spades.png")
        self.assertEqual(ten_of_spades.image_path(), "images/PNG-cards-1.3/10_of_spades.png")
        self.assertEqual(jack_of_clubs.image_path(), "images/PNG-cards-1.3/jack_of_clubs.png")
        
    def test_small_card_image_retrieval_path(self):
        two_of_spades = Card(2, "S")
        ten_of_spades = Card(10, "S")
        jack_of_clubs = Card(11, "C")
        self.assertEqual(two_of_spades.small_image_path(), "images/PNG-cards-1.3/2_of_spades (Custom).png")
        self.assertEqual(ten_of_spades.small_image_path(), "images/PNG-cards-1.3/10_of_spades (Custom).png")
        self.assertEqual(jack_of_clubs.small_image_path(), "images/PNG-cards-1.3/jack_of_clubs (Custom).png")
        
if __name__ == "__main__":
    main()

