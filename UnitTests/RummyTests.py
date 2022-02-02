from unittest import main, TestCase
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from card import Card
from cpu import CPU
from player import Player
from temp_rummy import Rummy

class TestRummy(TestCase):
    
    # ----------------------------------------------
    # test global frame ----------------------------
    # ----------------------------------------------
    
    # should not throw error on init
    def test_init(self):
        game = Rummy()
        
        
if __name__ == "__main__":
    main()

