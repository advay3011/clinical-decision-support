# Strands Architecture & Flow Diagrams

## How Strands Works - The Complete Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                               │
│                   "I have chicken and garlic"                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STRANDS AGENT                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Receive user input                                    │  │
│  │ 2. Add to conversation history                           │  │
│  │ 3. Send to LLM with:                                     │  │
│  │    - System prompt (agent personality)                   │  │
│  │    - Conversation history                               │  │
│  │    - Available tools (with docstrings)                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM (Claude, GPT, etc)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Analyzes:                                                │  │
│  │ - What is the user asking?                              │  │
│  │ - Do I need to use any tools?                           │  │
│  │ - Which tool should I use?                              │  │
│  │ - What parameters should I pass?                        │  │
│  │                                                          │  │
│  │ Decision: "Use search_recipes tool"                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL EXECUTION                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ search_recipes(                                          │  │
│  │   ingredients="chicken, garlic",                         │  │
│  │   cuisine="any"                                          │  │
│  │ )                                                        │  │
│  │                                                          │  │
│  │ Returns:                                                 │  │
│  │ "Found recipes for chicken, garlic:                     │  │
│  │  • Garlic Butter Chicken                                │  │
│  │  • Roasted Garlic Chicken"                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM GENERATES RESPONSE                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ LLM now has:                                             │  │
│  │ - Original user input                                    │  │
│  │ - Tool result                                            │  │
│  │ - System prompt                                          │  │
│  │                                                          │  │
│  │ Generates natural response:                             │  │
│  │ "Great! With chicken and garlic, you can make..."       │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RETURN TO USER                               │
│              "Great! With chicken and garlic..."                │
│                                                                 │
│  Conversation history is saved for next turn                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Recipe Bot Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      RECIPE BOT SYSTEM                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              SYSTEM PROMPT                              │   │
│  │  "You are RecipeBot, a helpful cooking assistant..."   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              AGENT                                      │   │
│  │  - Receives user input                                 │   │
│  │  - Maintains conversation history                      │   │
│  │  - Decides which tools to use                          │   │
│  │  - Generates responses                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│          ┌────────────────┼────────────────┐                   │
│          ▼                ▼                ▼                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   TOOL 1     │  │   TOOL 2     │  │   TOOL N     │         │
│  │              │  │              │  │              │         │
│  │ websearch()  │  │ get_weather()│  │ other_tool() │         │
│  │              │  │              │  │              │         │
│  │ Returns:     │  │ Returns:     │  │ Returns:     │         │
│  │ Search       │  │ Weather      │  │ Data         │         │
│  │ results      │  │ info         │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│          │                │                │                   │
│          └────────────────┼────────────────┘                   │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              LLM (Claude, GPT, etc)                     │   │
│  │  - Processes tool results                              │   │
│  │  - Generates natural response                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           │                                     │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              RESPONSE TO USER                           │   │
│  │  "Here are some great recipes you can make..."         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Tool Definition & Execution

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL DEFINITION                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  @tool                                                          │
│  def search_recipes(ingredients: str, cuisine: str) -> str:   │
│      """Search for recipes based on ingredients.              │
│                                                                 │
│      Args:                                                      │
│          ingredients: Comma-separated ingredients              │
│          cuisine: Type of cuisine                              │
│                                                                 │
│      Returns:                                                   │
│          Recipe suggestions as string                          │
│      """                                                        │
│      # Implementation                                           │
│      return recipes                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              WHAT LLM SEES (Tool Description)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Tool Name: search_recipes                                      │
│  Description: Search for recipes based on ingredients          │
│                                                                 │
│  Parameters:                                                    │
│    - ingredients (string): Comma-separated ingredients         │
│    - cuisine (string): Type of cuisine                         │
│                                                                 │
│  Returns: Recipe suggestions as string                         │
│                                                                 │
│  When to use: When user asks about recipes or cooking ideas   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              LLM DECIDES TO USE TOOL                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User: "I have chicken and garlic"                             │
│                                                                 │
│  LLM thinks:                                                    │
│  "User is asking about recipes with specific ingredients.      │
│   I should use search_recipes tool with:                       │
│   - ingredients='chicken, garlic'                              │
│   - cuisine='any'"                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              TOOL EXECUTION                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  search_recipes(                                                │
│      ingredients="chicken, garlic",                             │
│      cuisine="any"                                              │
│  )                                                              │
│                                                                 │
│  ↓ (function runs)                                              │
│                                                                 │
│  Returns:                                                       │
│  "Found recipes for chicken, garlic:                           │
│   • Garlic Butter Chicken                                      │
│   • Roasted Garlic Chicken                                     │
│   • Chicken Scampi"                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              LLM USES RESULT TO GENERATE RESPONSE               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LLM now has:                                                   │
│  1. Original user input                                         │
│  2. Tool result (recipes)                                       │
│  3. System prompt (be helpful, friendly)                        │
│                                                                 │
│  Generates response:                                            │
│  "Great! With chicken and garlic, you can make some           │
│   delicious dishes. Here are my top suggestions:               │
│   • Garlic Butter Chicken - Pan-sear with butter...           │
│   • Roasted Garlic Chicken - Roast with whole cloves...       │
│   • Chicken Scampi - Sauté with white wine and lemon..."      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Conversation History (Multi-turn)

```
Turn 1:
┌──────────────────────────────────────────┐
│ User: "I have chicken and garlic"        │
│ Agent: "Here are recipes..."             │
│ History: [Turn 1]                        │
└──────────────────────────────────────────┘

Turn 2:
┌──────────────────────────────────────────┐
│ User: "How do I sauté the chicken?"      │
│ Agent reads history:                     │
│   - We were talking about chicken        │
│   - User asked about recipes             │
│ Agent: "To sauté chicken..."             │
│ History: [Turn 1, Turn 2]                │
└──────────────────────────────────────────┘

Turn 3:
┌──────────────────────────────────────────┐
│ User: "What's my favorite ingredient?"   │
│ Agent reads history:                     │
│   - User mentioned chicken and garlic    │
│   - User asked about sautéing            │
│ Agent: "Based on our conversation,      │
│         you seem to like garlic!"        │
│ History: [Turn 1, Turn 2, Turn 3]        │
└──────────────────────────────────────────┘
```

---

## Comparison: Recipe Bot vs Your Custom Agent

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECIPE BOT                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  System Prompt:                                                 │
│  "You are RecipeBot, a helpful cooking assistant..."           │
│                                                                 │
│  Tools:                                                         │
│  1. websearch() - Search the web for recipes                   │
│                                                                 │
│  Interaction:                                                   │
│  - Interactive loop (while True)                               │
│  - Continuous conversation                                     │
│  - User types questions, bot responds                          │
│                                                                 │
│  Use Case:                                                      │
│  - Chat interface                                              │
│  - Real-time web search                                        │
│  - User-driven conversation                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    CUSTOM WEATHER AGENT                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  System Prompt:                                                 │
│  "You are a weather assistant..."                              │
│                                                                 │
│  Tools:                                                         │
│  1. get_weather() - Get weather for a city                     │
│  2. convert_temperature() - Convert temperature units          │
│                                                                 │
│  Interaction:                                                   │
│  - Programmatic calls                                          │
│  - Single or multi-turn queries                                │
│  - Integrated into larger application                          │
│                                                                 │
│  Use Case:                                                      │
│  - API endpoint                                                │
│  - Embedded in application                                     │
│  - Programmatic use                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

### What Strands Does:
1. **Abstracts LLM complexity** - You don't need to manage API calls directly
2. **Handles tool calling** - LLM automatically decides which tools to use
3. **Maintains context** - Conversation history is automatic
4. **Supports multiple providers** - Switch LLMs with one line of code

### The Three Core Components:
1. **Agent** - Orchestrates everything
2. **Tools** - Functions the agent can call
3. **System Prompt** - Instructions for the agent

### The Flow:
```
User Input → Agent → LLM → Tool Decision → Tool Execution → Response Generation → User Output
```

### Why Docstrings Matter:
The LLM reads tool docstrings to understand:
- What the tool does
- What parameters it needs
- When to use it
- What to expect as output

### Best Practice Pattern:
```python
# 1. Define tools with @tool decorator
@tool
def my_tool(param: str) -> str:
    """Clear description of what this tool does.
    
    Args:
        param: Description of parameter
    
    Returns:
        Description of return value
    """
    # Implementation
    return result

# 2. Create agent with system prompt and tools
agent = Agent(
    system_prompt="Your instructions here",
    tools=[my_tool],
)

# 3. Use the agent
response = agent("User question")
```
