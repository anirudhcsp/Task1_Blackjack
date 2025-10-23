"""
GAME FLOW - VERSION
==============================
Orchestrates the Blackjack game with WORKING card drawing.

Instead of relying on LLM to call tools, we:
1. Use LLM for decision-making (hit or stand)
2. Call the tool directly when needed
3. Update game state properly
"""

from crewai import Agent, Task, Crew, Process
from config import OPENAI_MODEL
from agents import player1_agent, player2_agent, player3_agent
from game_state import get_player_state, get_all_states, set_player_standing
from tools import draw_card_tool


def ask_player_decision(player_agent: Agent, player_name: str) -> str:
    """
    Ask an AI player to decide: hit or stand.
    Uses LLM for decision-making.
    
    Args:
        player_agent: The AI agent making the decision
        player_name: Name of the player
    
    Returns:
        str: The player's decision
    """
    state = get_player_state(player_name)
    
    task = Task(
        description=f"""
You are {player_name} playing Blackjack.

Your current status:
- Cards: {state['cards']}
- Score: {state['score']}
- Cards drawn: {len(state['cards'])} out of 3 maximum

Based on your strategy, decide:
- If you want another card, say: "HIT"
- If you want to stop, say: "STAND"

Just respond with one word: HIT or STAND
""",
        agent=player_agent,
        expected_output=f"{player_name}'s decision: HIT or STAND"
    )
    
    crew = Crew(
        agents=[player_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False  # Less verbose for cleaner output
    )
    
    try:
        result = crew.kickoff()
        decision = str(result).upper()
        
        # Parse decision
        if "HIT" in decision or "DRAW" in decision or "CARD" in decision:
            return "HIT"
        else:
            return "STAND"
    except Exception as e:
        print(f"⚠️  Error getting decision from {player_name}: {e}")
        return "STAND"  # Default to standing on error


def play_ai_turn(player_agent: Agent, player_name: str):
    """
    Executes one AI player's complete turn.
    Actually draws cards using the tool!
    
    Args:
        player_agent: The AI agent for this player
        player_name: Name of the player (Player1, Player2, Player3)
    """
    print(f"\n{'='*70}")
    print(f"🎮 {player_name.upper()}'S TURN")
    print(f"{'='*70}")
    
    # Player can draw up to 3 cards
    while True:
        state = get_player_state(player_name)
        
        # Check if player is done
        if len(state["cards"]) >= 3:
            print(f"\n✅ {player_name} has reached maximum 3 cards.")
            break
        
        if state["busted"]:
            print(f"\n💥 {player_name} is busted!")
            break
        
        if state.get("standing", False):
            print(f"\n✅ {player_name} is standing.")
            break
        
        # Display current status
        print(f"\n📊 Current Status:")
        print(f"   Cards: {state['cards']}")
        print(f"   Score: {state['score']}")
        
        # Ask player for decision (using LLM)
        print(f"\n🤔 {player_name} is deciding...")
        decision = ask_player_decision(player_agent, player_name)
        
        if decision == "HIT":
            print(f"💭 {player_name} says: I want to HIT!")
            
            # ACTUALLY CALL THE TOOL DIRECTLY!
            print(f"🎴 Dealer drawing card for {player_name}...")
            result = draw_card_tool.func(player_name)  # Call tool function directly!
            print(f"   {result}")
            
            # Check if busted
            updated_state = get_player_state(player_name)
            if updated_state["busted"]:
                break
        else:
            print(f"💭 {player_name} says: I'll STAND!")
            set_player_standing(player_name)
            break
    
    # Show final state
    final_state = get_player_state(player_name)
    print(f"\n📊 {player_name} Final:")
    print(f"   Cards: {final_state['cards']}")
    print(f"   Score: {final_state['score']}")
    if final_state['busted']:
        print(f"   Status: 💥 BUSTED")
    else:
        print(f"   Status: ✓ Active")


def play_human_turn():
    """
    Handles the human player's turn.
    Human types requests and dealer draws cards.
    """
    print(f"\n{'='*70}")
    print(f"🎮 YOUR TURN (HUMAN PLAYER)")
    print(f"{'='*70}")
    
    while True:
        state = get_player_state("Human")
        
        # Display current status
        print(f"\n📊 Your Status:")
        print(f"   Cards: {state['cards']}")
        print(f"   Score: {state['score']}")
        print(f"   Cards Drawn: {len(state['cards'])} / 3")
        
        # Check if done
        if len(state["cards"]) >= 3:
            print("\n✅ You've reached maximum 3 cards.")
            break
        
        if state["busted"]:
            print("\n💥 YOU BUSTED!")
            break
        
        if state.get("standing", False):
            print("\n✅ You're standing.")
            break
        
        # Get human input
        print("\n" + "-"*70)
        print("Options:")
        print("  • Type 'hit' or 'h' to draw a card")
        print("  • Type 'stand' or 's' to stop")
        print("-"*70)
        user_input = input("👉 Your decision: ").strip().lower()
        
        if not user_input:
            print("⚠️  Please enter a decision.")
            continue
        
        # Check if player wants to stand
        if any(word in user_input for word in ['stand', 'stay', 'stop', 's']):
            set_player_standing("Human")
            print(f"\n✅ You chose to STAND with {state['score']}")
            break
        
        # Player wants a card - CALL THE TOOL DIRECTLY!
        print(f"\n🎴 Dealer drawing card for you...")
        result = draw_card_tool.func("Human")  # Call tool function directly!
        print(f"   {result}")
        
        # Check updated state
        updated_state = get_player_state("Human")
        if updated_state["busted"]:
            print(f"\n💥 YOU BUSTED!")
            break
        elif len(updated_state["cards"]) >= 3:
            print(f"\n✅ Maximum 3 cards reached.")
            break
    
    # Show final state
    final_state = get_player_state("Human")
    print(f"\n📊 Your Final:")
    print(f"   Cards: {final_state['cards']}")
    print(f"   Score: {final_state['score']}")
    if final_state['busted']:
        print(f"   Status: 💥 BUSTED")
    else:
        print(f"   Status: ✓ Active")


def determine_winner() -> str:
    """
    Determines the winner based on final scores.
    
    Returns:
        str: Name of the winning player
    """
    all_states = get_all_states()
    
    # Get valid players (not busted)
    valid_players = {
        name: state["score"]
        for name, state in all_states.items()
        if not state["busted"]
    }
    
    if not valid_players:
        return "No Winner - Everyone Busted! 💥"
    
    # Find highest score
    winner = max(valid_players, key=valid_players.get)
    return winner


def display_final_results():
    """
    Displays final game results and announces winner.
    """
    print("\n" + "="*70)
    print("🏆 FINAL RESULTS")
    print("="*70)
    
    all_states = get_all_states()
    
    print("\n📊 Final Scores:")
    print("-"*70)
    for player, state in all_states.items():
        status = "💥 BUSTED" if state["busted"] else "✓ Active"
        print(f"{player:10} | Cards: {str(state['cards']):20} | Score: {state['score']:2} | {status}")
    print("-"*70)
    
    # Determine winner
    winner = determine_winner()
    
    print("\n" + "="*70)
    print(f"🎊 WINNER: {winner} 🎊")
    print("="*70)
    
    if winner in all_states:
        winner_state = all_states[winner]
        print(f"\n🏆 Winning Score: {winner_state['score']}")
        print(f"🎴 Winning Cards: {winner_state['cards']}")
    
    print("\n" + "="*70)


def run_complete_game():
    """
    Runs the complete Blackjack game sequence.
    """
    print("\n" + "="*70)
    print("🎰 AI BLACKJACK GAME - POWERED BY CREWAI & OPENAI 🎰")
    print("="*70)
    print("\n📜 GAME RULES:")
    print("  • Each player can draw up to 3 cards")
    print("  • Goal: Get closest to 21 without going over")
    print("  • Over 21 = BUST (automatic loss)")
    print("  • AI agents use LLM to make decisions")
    print("\n👥 PLAYERS:")
    print("  • Player1 (Conservative AI - prefers to stand at 15+)")
    print("  • Player2 (Moderate AI - prefers to stand at 17+)")
    print("  • Player3 (Aggressive AI - prefers to stand at 18+)")
    print("  • You (Human Player)")
    print("="*70)
    
    input("\n🎯 Press ENTER to start the game...")
    
    # Play AI players' turns
    play_ai_turn(player1_agent, "Player1")
    play_ai_turn(player2_agent, "Player2")
    play_ai_turn(player3_agent, "Player3")
    
    # Play human player's turn
    play_human_turn()
    
    # Display results
    display_final_results()


# Export
__all__ = ['run_complete_game']
