"""
DEALER TOOLS
============
Contains tools that ONLY the Dealer Agent can use.
This is how we enforce that players must ASK the dealer for cards.

Compatible with CrewAI 1.1.0+
"""

from crewai.tools import tool
from card_manager import draw_card
from game_state import add_card_to_player, get_player_state


@tool("Draw Card for Player")
def draw_card_tool(player_name: str) -> str:
    """
    Draws a card for a specific player in the Blackjack game.
    
    IMPORTANT: Only the Dealer Agent has access to this tool.
    Players CANNOT call this directly - they must ask the Dealer.
    
    Args:
        player_name: The name of the player to draw a card for
                    (Player1, Player2, Player3, or Human)
    
    Returns:
        str: A message describing the card drawn and the player's new score
    
    Example:
        Input: "Player1"
        Output: "🎴 Player1 drew a 7. Cards: [7]. Score: 7"
    """
    # Check if player exists
    valid_players = ["Player1", "Player2", "Player3", "Human"]
    if player_name not in valid_players:
        return f"Error: {player_name} is not a valid player. Valid players: {valid_players}"
    
    # Check if player already has 3 cards (max limit)
    current_state = get_player_state(player_name)
    if len(current_state["cards"]) >= 3:
        return f"{player_name} already has 3 cards (maximum limit). Cannot draw more cards."
    
    # Check if player is already busted
    if current_state["busted"]:
        return f"{player_name} is already busted (over 21). Cannot draw more cards."
    
    # Check if player is standing
    if current_state.get("standing", False):
        return f"{player_name} is standing. Cannot draw more cards."
    
    # Draw a card
    card = draw_card()
    
    # Add card to player's hand
    result = add_card_to_player(player_name, card)
    
    # Format response message
    if result["busted"]:
        return (f"🎴 {player_name} drew a {card}. "
                f"Cards: {result['cards']}. Score: {result['score']}. "
                f"💥 BUSTED! (Over 21)")
    else:
        return (f"🎴 {player_name} drew a {card}. "
                f"Cards: {result['cards']}. Score: {result['score']}")


# Export the tool
__all__ = ['draw_card_tool']