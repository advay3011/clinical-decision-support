# Strands Learning Summary

## What is Strands?

**Strands** is a Python framework for building AI agents that can:
- Use LLMs (Claude, GPT, Gemini, etc.)
- Call tools/functions to accomplish tasks
- Maintain conversation history automatically
- Handle complex multi-turn interactions

Think of it as a bridge between your code and AI models.

---

## The Three Core Components

### 1. Agent
The orchestrator that:
- Receives user input
- Decides which tools to use
- Generates responses
- Maintains conversation history

```python
agent = Agent(
    system_prompt="Your instructions",
    tools=[tool1, tool2],
)
```

### 2. Tools
Functions the agent can call:
- Marked with `@tool` decorator
- Have clear docstrings (LLM reads these)
- Return strings or easily convertible values
- Handle errors gracefully

```python
@tool
def my_tool(param: str) -> str:
    """Clear description.
    
    Args:
        param: Description
    
    Returns:
        Description
    """
    return result
```

### 3. System Prompt
Instructions that define the agent's personality and behavior:
- Tells the agent what it is
- Explains what it should do
- Guides decision-making

```python
system_prompt="""You are a helpful assistant.
Help users with X, Y, and Z.
Use tools when appropriate."""
```

---

## The Recipe Bot Explained

### What It Does:
- Helps users find recipes
- Answers cooking questions
- Uses web search to find real recipes

### How It Works:

```
User: "I want pasta carbonara"
  ↓
Agent receives input
  ↓
LLM thinks: "User wants a recipe, I should search the web"
  ↓
Agent calls: websearch(keywords="pasta carbonara recipe")
  ↓
DuckDuckGo returns search results
  ↓
LLM generates response: "Here's how to make pasta carbonara..."
  ↓
User sees response
  ↓
Conversation history saved for next turn
```

### Key Code:

```python
# 1. Define the tool
@tool
def websearch(keywords: str) -> str:
    """Search the web..."""
    results = DDGS().text(keywords)
    return results

# 2. Create the agent
recipe_agent = Agent(
    system_prompt="You are RecipeBot...",
    tools=[websearch],
)

# 3. Use it in a loop
while True:
    user_input = input("\nYou > ")
    response = recipe_agent(user_input)
    print(f"\nRecipeBot > {response}")
```

---

## How to Build Your Own Agent

### Step 1: Define Tools
```python
from strands import tool

@tool
def my_tool(param: str) -> str:
    """What this tool does.
    
    Args:
        param: What this parameter is for
    
    Returns:
        What this returns
    """
    # Your implementation
    return result
```

### Step 2: Create Agent
```python
from strands import Agent

agent = Agent(
    system_prompt="You are X. Do Y and Z.",
    tools=[my_tool],
)
```

### Step 3: Use It
```python
# Single query
response = agent("User question")

# Or interactive loop
while True:
    user_input = input("You > ")
    response = agent(user_input)
    print(f"Agent > {response}")
```

---

## Key Concepts

### Docstrings Are Critical
The LLM reads tool docstrings to understand:
- What the tool does
- What parameters it needs
- When to use it
- What to expect as output

**Bad docstring:**
```python
@tool
def search(q: str) -> str:
    """Search."""
    return results
```

**Good docstring:**
```python
@tool
def search(q: str) -> str:
    """Search the web for information.
    
    Args:
        q: Search query (e.g., "python tutorial")
    
    Returns:
        Search results with titles and snippets
    """
    return results
```

### Conversation History Is Automatic
```python
agent("My name is Alice")
response = agent("What's my name?")
# Agent remembers: "Alice"
```

### Error Handling Matters
```python
@tool
def my_tool(param: str) -> str:
    """Do something."""
    try:
        result = do_something(param)
        return result
    except Exception as e:
        return f"Error: {e}"
```

### System Prompt Guides Behavior
```python
# Vague
system_prompt="You are helpful"

# Better
system_prompt="""You are a customer support agent.
Help customers with order issues.
Be empathetic and professional.
Use the lookup_order tool to find order details.
Use the process_refund tool to handle refunds."""
```

---

## Common Patterns

### Pattern 1: Simple Query
```python
agent = Agent(system_prompt="...", tools=[tool1])
response = agent("Question")
```

### Pattern 2: Interactive Chat
```python
while True:
    user_input = input("You > ")
    response = agent(user_input)
    print(f"Agent > {response}")
```

### Pattern 3: Multi-turn with Context
```python
agent("My name is Alice")
agent("I like Python")
response = agent("What do I like?")
# Agent remembers both facts
```

### Pattern 4: Multiple Tools
```python
agent = Agent(
    system_prompt="...",
    tools=[tool1, tool2, tool3],
)
# Agent decides which tool to use
```

---

## Recipe Bot vs Your First Agent

| Aspect | First Agent | Recipe Bot |
|--------|-------------|-----------|
| Tools | Pre-built | Custom |
| Interaction | Single query | Interactive loop |
| Data | Local | Web search |
| Complexity | Simple | Intermediate |
| Use Case | Learning | Real-world |

---

## Best Practices

### ✅ DO:
1. Write clear docstrings
2. Include Args section
3. Handle errors gracefully
4. Use specific system prompts
5. Test tools independently
6. Use appropriate temperature (0.1-0.3 for factual, 0.7-0.9 for creative)

### ❌ DON'T:
1. Skip docstrings
2. Hardcode API keys
3. Make tools too complex
4. Forget error handling
5. Use vague system prompts
6. Ignore token limits

---

## The Flow (Simplified)

```
User Input
    ↓
Agent + LLM
    ↓
Decide: Use tools?
    ↓
If YES: Call tools → Get results
    ↓
Generate response
    ↓
Return to user
    ↓
Save conversation history
```

---

## What You Now Know

1. **What Strands is** - A framework for building AI agents
2. **How it works** - Agent + Tools + System Prompt
3. **How to create tools** - Use `@tool` decorator with clear docstrings
4. **How to create agents** - Combine tools + system_prompt
5. **How to use agents** - Single query or interactive loop
6. **How conversation works** - History is automatic
7. **How the recipe bot works** - Web search + interactive loop

---

## Next Steps

### To Deepen Your Knowledge:

1. **Read the documentation** - Check out the Strands docs
2. **Build your own agent** - Try creating a custom agent
3. **Experiment with tools** - Create different types of tools
4. **Try different LLMs** - Switch from Bedrock to OpenAI, Anthropic, etc.
5. **Build real applications** - Create a chatbot, automation tool, etc.

### Example Projects:

1. **Customer Support Bot** - Help customers with issues
2. **Research Assistant** - Search and summarize information
3. **Code Helper** - Answer programming questions
4. **Data Analyst** - Query databases and generate reports
5. **Personal Assistant** - Manage tasks, calendar, notes

---

## Quick Reference

### Create a Tool
```python
@tool
def my_tool(param: str) -> str:
    """Description.
    
    Args:
        param: Description
    
    Returns:
        Description
    """
    return result
```

### Create an Agent
```python
agent = Agent(
    system_prompt="You are X",
    tools=[my_tool],
)
```

### Use the Agent
```python
response = agent("Question")
print(response)
```

### Interactive Loop
```python
while True:
    user_input = input("You > ")
    response = agent(user_input)
    print(f"Agent > {response}")
```

---

## Key Takeaway

**Strands makes it simple to build intelligent agents:**

1. Define what your agent can do (tools)
2. Tell it how to behave (system_prompt)
3. Let it handle the rest (tool calling, conversation history)

That's it! The framework handles all the complexity of LLM integration, tool calling, and conversation management.
