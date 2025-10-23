"""
CARD MANAGER
============
Contains the card drawing function.
This function can ONLY be called by the Dealer Agent via the tool.
"""

import random


def draw_card():
    """
    Simulates drawing a card in Blackjack.
    Returns a random number between 2 and 11.
    
    Returns:
        int: A random number between 2 and 11
        
    Card values:
        - 2-10: Number cards
        - 11: Ace (simplified to always be 11)
    
    IMPORTANT: This function should ONLY be called by the Dealer Agent
    via the draw_card_tool. Players cannot call this directly!
    """
    return random.randint(2, 11)


# Test the function if this file is run directly
if __name__ == "__main__":
    print("🎴 Testing card drawing function:")
    for i in range(5):
        card = draw_card()
        print(f"  Card {i+1}: {card}")