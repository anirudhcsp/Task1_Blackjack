"""
CONFIGURATION
=============
Loads environment variables and sets up OpenAI API for CrewAI.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Validate API key exists
if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not found in .env file!")
    print("Please create a .env file and add your OpenAI API key.")
    print("Example: OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx")
    exit(1)

# Set API key for OpenAI (required by CrewAI)
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Use cheapest and fastest OpenAI model
OPENAI_MODEL = "gpt-4o-mini"  # Fastest and cheapest model

print("✅ Configuration loaded successfully!")
print(f"📊 Using OpenAI model: {OPENAI_MODEL}")