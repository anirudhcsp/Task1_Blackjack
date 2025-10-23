"""
🎰 AI BLACKJACK GAME - MAIN ENTRY POINT
========================================

This is the entry point for the AI-powered Blackjack game.

To run the game:
    python main.py

What this file does:
    1. Loads configuration (API key from .env file)
    2. Runs the complete game
    3. Handles errors gracefully

Author: Anirudh
Date: 2025
Technology: CrewAI + OpenAI + Python
"""

# ============================================
# IMPORTS
# ============================================

# Load configuration (API key, model settings)
# This must be imported first to set up the environment
import config

# Import the main game orchestration function
from game_flow import run_complete_game


# ============================================
# MAIN FUNCTION
# ============================================

def main():
    """
    Main entry point for the Blackjack game.
    
    This function:
    1. Calls run_complete_game() which orchestrates the entire game
    2. Handles keyboard interrupts (Ctrl+C) gracefully
    3. Catches and displays any errors that occur
    
    Returns:
        None
    """
    
    try:
        # Run the complete Blackjack game
        # This function is in game_flow.py
        run_complete_game()
        
        # Game completed successfully
        print("\n" + "="*70)
        print("🎉 Thanks for playing AI Blackjack! 🎉")
        print("="*70)
        print()
        
    except KeyboardInterrupt:
        # User pressed Ctrl+C to quit
        print("\n\n" + "="*70)
        print("⚠️  Game interrupted by user.")
        print("Thanks for playing! Goodbye! 👋")
        print("="*70)
        print()
        
    except Exception as e:
        # Something went wrong
        print("\n" + "="*70)
        print("❌ AN ERROR OCCURRED")
        print("="*70)
        print(f"\nError details: {e}")
        print("\nPossible fixes:")
        print("  1. Check that your .env file exists")
        print("  2. Verify your OPENAI_API_KEY is correct")
        print("  3. Ensure all dependencies are installed:")
        print("     pip install -r requirements.txt")
        print("\n" + "="*70)
        print()


# ============================================
# RUN THE GAME
# ============================================

if __name__ == "__main__":
    """
    This block runs only when this file is executed directly.
    It does NOT run if this file is imported by another file.
    
    Example:
        python main.py  ← This runs the game
        import main     ← This does NOT run the game
    """
    main()