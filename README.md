# 🎰 AI Blackjack Game with CrewAI

A command-line Blackjack game powered by AI agents using CrewAI and OpenAI's LLM.

## 📋 Features

- **Multi-Agent System**: 3 AI players + 1 Dealer agent + 1 Human player
- **True Agent Communication**: Players ASK the Dealer for cards (agent-to-agent)
- **LLM-Powered Decisions**: AI agents use OpenAI's GPT-4o-mini for decision-making
- **Tool-Based Access Control**: Only the Dealer can draw cards (using CrewAI tools)
- **Natural Language**: Human player interacts using natural language
- **Different Strategies**: Conservative, Moderate, and Aggressive AI players

## 🏗️ Architecture

### Agent Roles

| Agent | Role | Tool Access | Strategy |
|-------|------|-------------|----------|
| **Dealer** | Manages game, draws cards | `draw_card_tool` ✅ | N/A |
| **Player1** | Conservative player | None ❌ | Stands at 15+ |
| **Player2** | Moderate player | None ❌ | Stands at 17+ |
| **Player3** | Aggressive player | None ❌ | Stands at 18+ |
| **Human** | You! | None ❌ | Your choice |

### Key Requirement: Tool-Based Card Drawing

✅ **CORRECT**: Players ASK Dealer → Dealer uses `draw_card_tool()`
❌ **WRONG**: Players directly call `draw_card()`

This enforces the requirement: *"The players cannot call the card-drawing function directly. Instead, they must ask the AI dealer to draw cards on their behalf."*

## 📁 File Structure

```
task1-blackjack/
├── main.py              # Entry point - run this!
├── config.py            # Loads API key and configuration
├── card_manager.py      # Contains draw_card() function
├── game_state.py        # Manages player scores and game state
├── tools.py             # Dealer's draw_card_tool (CrewAI tool)
├── agents.py            # Defines all AI agents
├── tasks.py             # Creates CrewAI tasks for turns
├── game_flow.py         # Orchestrates game using Crew
├── requirements.txt     # Python dependencies
├── .env                 # Your OpenAI API key (create this!)
└── README.md            # This file provides instructions and summary about the overall game!
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `crewai` - AI agent framework
- `crewai-tools` - Tools for agents
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management

### 2. Create .env File

Create a file named `.env` in the project root:

```bash
# .env file
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### 3. Run the Game!

```bash
python main.py
```

## 🎮 How to Play

1. **AI Players Go First**: Player1, Player2, and Player3 take turns
   - Each AI agent uses LLM to decide whether to hit or stand
   - AI agents ASK the Dealer for cards
   - Dealer uses `draw_card_tool()` to draw cards

2. **Your Turn**: 
   - Type natural language commands:
     - "Dealer, give me a card"
     - "Hit me"
     - "I'll stand"
     - "Stand"
   - Dealer draws cards for you using the tool

3. **Winner Declared**: Highest score ≤ 21 wins!

## 🔧 How It Works (Technical)

### Agent Communication Flow

```
Player Agent (LLM decides)
    ↓
    "Dealer, please draw a card for me"
    ↓
Dealer Agent receives request
    ↓
Dealer calls draw_card_tool("Player1")
    ↓
Tool calls draw_card() → returns 7
    ↓
Tool updates game_state
    ↓
Dealer responds: "Player1 drew a 7. Score: 7"
```

### CrewAI Task Execution

```python
# Player decides
player_task = Task(description="Decide: hit or stand?", agent=player1_agent)

# Dealer responds
dealer_task = Task(
    description="Draw card for player", 
    agent=dealer_agent,
    context=[player_task]  # Sees player's decision
)

# Execute both tasks
crew = Crew(agents=[player1_agent, dealer_agent], tasks=[player_task, dealer_task])
crew.kickoff()  # LLM calls happen here!
```

## 💰 Cost Estimate

Using `gpt-4o-mini` (cheapest model):
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- **Cost per game: ~$0.01 - $0.05** (very cheap!)

## 🎯 Assignment Requirements Met

✅ **Python 3.12+** - Modern Python  
✅ **At least 3 AI agent players** - Player1, Player2, Player3  
✅ **One AI dealer agent** - Dealer with tool access  
✅ **Local card-drawing function** - `draw_card()` in card_manager.py  
✅ **Up to 3 cards per player** - Enforced in game logic  
✅ **Players ask Dealer** - Players have NO direct tool access  
✅ **LLM decision-making** - All agents use gpt-4o-mini  
✅ **Terminal-based** - Pure command-line  
✅ **Natural language** - Human types natural requests  
✅ **Winner declared** - Displayed at end  

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY not found"
- Make sure `.env` file exists in project root
- Verify format: `OPENAI_API_KEY=sk-proj-xxxxx` (no spaces around `=`)

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Game is slow
- Normal! Each decision requires an LLM API call (1-3 seconds)
- This demonstrates TRUE AI reasoning, not hardcoded logic

### Agents making weird decisions
- This is LLM behavior - decisions may vary!
- Strategies are guidelines in the agent's backstory
- Shows authentic AI decision-making

## 📝 Notes

- **Model Used**: `gpt-4o-mini` (fastest & cheapest)
- **Agent Framework**: CrewAI 0.80.0
- **Key Innovation**: Tool-based access control (only Dealer can draw)
- **Decision Making**: True LLM reasoning (not if/else logic)

## 🎓 Learning Points

This project demonstrates:
1. **Multi-agent orchestration** with CrewAI
2. **Tool-based access control** (security/permissions)
3. **Agent-to-agent communication** via tasks
4. **LLM integration** for decision-making
5. **Natural language interaction** with AI systems

---

Built using CrewAI, OpenAI, and Python
