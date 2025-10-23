"""
GAME TASKS
==========
Defines CrewAI tasks for player decision-making and dealer actions.
Tasks enable agent-to-agent communication.
"""

from crewai import Task
from game_state import get_player_state


def create_player_decision_task(player_agent, player_name: str) -> Task:
    """
    Creates a task for a player to decide whether to hit or stand.
    
    Args:
        player_agent: The AI agent making the decision
        player_name: Name of the player (Player1, Player2, Player3)
    
    Returns:
        Task: A CrewAI task for the player's decision
    """
    state = get_player_state(player_name)
    
    description = f"""
It's your turn, {player_name}!

Your current status:
- Cards: {state['cards']}
- Score: {state['score']}
- Cards drawn: {len(state['cards'])} out of 3 maximum

Based on your strategy and current score, decide:
1. If you want another card, ASK the Dealer: "Dealer, please draw a card for me" (or similar)
2. If you want to stop, say: "I'll stand" (or similar)

Remember:
- You MUST ask the Dealer to draw cards - you can't draw yourself
- Goal: Get close to 21 without going over
- You bust (lose) if you go over 21
- Maximum 3 cards allowed

What is your decision?
"""
    
    return Task(
        description=description,
        agent=player_agent,
        expected_output=f"{player_name}'s decision: either request a card from dealer or stand"
    )


def create_dealer_draw_task(dealer_agent, player_name: str, player_request: str) -> Task:
    """
    Creates a task for the dealer to draw a card for a player.
    
    Args:
        dealer_agent: The dealer agent
        player_name: Name of the player requesting a card
        player_request: The player's request message
    
    Returns:
        Task: A CrewAI task for the dealer to execute
    """
    description = f"""
{player_name} has requested: "{player_request}"

Use your draw_card_tool to draw a card for {player_name}.
After drawing, tell {player_name} what card they got and their new score.

Example: "{player_name} drew a 7. Cards: [7]. Score: 7"

Draw the card now!
"""
    
    return Task(
        description=description,
        agent=dealer_agent,
        expected_output=f"Card drawn for {player_name} with updated score"
    )


def create_dealer_response_task(dealer_agent, player_name: str, decision: str) -> Task:
    """
    Creates a task for dealer to respond to a player's decision.
    
    Args:
        dealer_agent: The dealer agent
        player_name: Name of the player
        decision: The player's decision (from their task output)
    
    Returns:
        Task: A CrewAI task for the dealer
    """
    # Check if player wants to hit (draw) or stand
    decision_lower = decision.lower()
    wants_card = any(keyword in decision_lower for keyword in 
                     ['card', 'hit', 'draw', 'deal', 'another', 'more'])
    
    if wants_card:
        description = f"""
{player_name} wants another card. They said: "{decision}"

Use your draw_card_tool to draw a card for {player_name}.
Then announce what card they got and their new score.
"""
    else:
        description = f"""
{player_name} is standing. They said: "{decision}"

Acknowledge their decision.
Say: "{player_name} stands with [their current score]"
"""
    
    return Task(
        description=description,
        agent=dealer_agent,
        expected_output=f"Dealer's response to {player_name}'s decision"
    )


# Export functions
__all__ = ['create_player_decision_task', 'create_dealer_draw_task', 'create_dealer_response_task']