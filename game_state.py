"""
GAME STATE MANAGER
==================
Manages all player states, scores, and game data.
This is the central "database" for the game.
"""

# Global game state - stores all player information
game_state = {
    "Player1": {"score": 0, "cards": [], "busted": False, "standing": False},
    "Player2": {"score": 0, "cards": [], "busted": False, "standing": False},
    "Player3": {"score": 0, "cards": [], "busted": False, "standing": False},
    "Human": {"score": 0, "cards": [], "busted": False, "standing": False}
}


def add_card_to_player(player_name: str, card: int) -> dict:
    """
    Adds a card to a player's hand and updates their score.
    
    Args:
        player_name: Name of player (Player1, Player2, Player3, Human)
        card: The card value (2-11)
    
    Returns:
        dict: Updated player information
    """
    # Add card to player's hand
    game_state[player_name]["cards"].append(card)
    
    # Calculate new total score
    game_state[player_name]["score"] = sum(game_state[player_name]["cards"])
    
    # Check if player busted (went over 21)
    if game_state[player_name]["score"] > 21:
        game_state[player_name]["busted"] = True
    
    # Return updated player info
    return {
        "player": player_name,
        "card": card,
        "cards": game_state[player_name]["cards"],
        "score": game_state[player_name]["score"],
        "busted": game_state[player_name]["busted"]
    }


def get_player_state(player_name: str) -> dict:
    """
    Gets the current state of a specific player.
    
    Args:
        player_name: Name of the player
    
    Returns:
        dict: Player's current state
    """
    return game_state[player_name].copy()


def set_player_standing(player_name: str):
    """
    Marks a player as standing (no more cards).
    
    Args:
        player_name: Name of the player
    """
    game_state[player_name]["standing"] = True


def get_all_states() -> dict:
    """
    Gets the state of all players.
    
    Returns:
        dict: Complete game state
    """
    return game_state.copy()


def reset_game():
    """
    Resets the game state for a new game.
    """
    for player in game_state:
        game_state[player] = {"score": 0, "cards": [], "busted": False, "standing": False}


# Test if this file is run directly
if __name__ == "__main__":
    print("🧪 Testing game state management:")
    print(f"Initial state: {game_state['Player1']}")
    
    result = add_card_to_player("Player1", 7)
    print(f"After drawing 7: {result}")
    
    result = add_card_to_player("Player1", 9)
    print(f"After drawing 9: {result}")