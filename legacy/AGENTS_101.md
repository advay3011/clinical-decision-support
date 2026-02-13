# Agents 101 - Complete Beginner Guide

## What is an Agent?

An **agent** is a software program that can:
1. **Understand** what you ask it to do
2. **Decide** what actions to take
3. **Use tools** to accomplish tasks
4. **Think** about the results
5. **Respond** with answers

Think of it like hiring an intelligent assistant who can use various tools to help you.

### Real-World Analogy

Imagine you ask a human assistant: "What's the weather in New York and how should I dress?"

The assistant would:
1. **Understand** your question
2. **Decide** they need to check the weather
3. **Use a tool** (weather app) to get the information
4. **Think** about what clothes match that weather
5. **Respond** with advice

An AI agent does exactly this, but with software tools instead of physical ones.

---

## What is Strands?

**Strands** is a Python framework that makes it easy to build AI agents.

### Without Strands (Hard Way):
```python
# You have to manually:
# 1. Call the LLM API
# 2. Parse the response
# 3. Decide which tool to use
# 4. Call the tool
# 5. Send results back to LLM
# 6. Manage conversation history
# 7. Handle errors
# ... lots of complex code
```

### With Strands (Easy Way):
```python
from strands import Agent, tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return "Sunny, 72°F"

agent = Agent(
    system_prompt="You are a helpful assistant",
    tools=[get_weather],
)

response = agent("What's the weather in New York?")
```

**Strands handles all the complexity for you!**

---

## The Three Core Concepts

### 1. Tools
**What they are:** Functions your agent can call

**Example:**
```python
@tool
def calculator(expression: str) -> str:
    """Calculate a math expression.
    
    Args:
        expression: Math expression like "2 + 2"
    
    Returns:
        The result
    """
    return str(eval(expression))
```

**Why they matter:** Tools give your agent the ability to do things

### 2. System Prompt
**What it is:** Instructions that define the agent's personality and behavior

**Example:**
```python
system_prompt = """You are a helpful math tutor.
Help students solve math problems.
Explain your reasoning step by step.
Use the calculator tool when needed."""
```

**Why it matters:** It tells the agent how to behave

### 3. Agent
**What it is:** The orchestrator that combines tools + system prompt

**Example:**
```python
agent = Agent(
    system_prompt="You are a helpful math tutor",
    tools=[calculator],
)
```

**Why it matters:** It's the main object you interact with

---

## How an Agent Works (Step by Step)

### The Flow:

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: You ask the agent a question                   │
│ "What is 25 * 4?"                                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Step 2: Agent sends to LLM with:                        │
│ - Your question                                         │
│ - System prompt (instructions)                          │
│ - Available tools (with descriptions)                   │
│ - Conversation history                                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Step 3: LLM analyzes and decides                        │
│ "User wants to calculate 25 * 4"                        │
│ "I should use the calculator tool"                      │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Step 4: Agent calls the tool                            │
│ calculator(expression="25 * 4")                         │
│ Returns: "100"                                          │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Step 5: LLM generates response                          │
│ "The answer is 100"                                     │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Step 6: Response sent to you                            │
│ "The answer is 100"                                     │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Step 7: Conversation history saved                      │
│ For next turn, agent remembers this exchange            │
└─────────────────────────────────────────────────────────┘
```

---

## Building Your First Agent - Step by Step

### Step 1: Define a Tool

A tool is just a Python function with the `@tool` decorator:

```python
from strands import tool

@tool
def greet(name: str) -> str:
    """Greet someone by name.
    
    Args:
        name: The person's name
    
    Returns:
        A greeting message
    """
    return f"Hello, {name}! Nice to meet you."
```

**Key points:**
- `@tool` decorator marks it as a tool
- Docstring is **critical** - LLM reads this to understand the tool
- Include `Args` section describing parameters
- Return a string

### Step 2: Create the Agent

```python
from strands import Agent

agent = Agent(
    system_prompt="You are a friendly assistant",
    tools=[greet],
)
```

**Key points:**
- `system_prompt` tells the agent how to behave
- `tools` is a list of tools the agent can use

### Step 3: Use the Agent

```python
response = agent("Say hello to Alice")
print(response)
# Output: "Hello, Alice! Nice to meet you."
```

**That's it!** The agent:
1. Understood your request
2. Decided to use the `greet` tool
3. Called it with "Alice"
4. Generated a response

---

## Complete Working Example

```python
from strands import Agent, tool

# Step 1: Define tools
@tool
def add(a: int, b: int) -> str:
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum
    """
    return str(a + b)

@tool
def multiply(a: int, b: int) -> str:
    """Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The product
    """
    return str(a * b)

# Step 2: Create the agent
math_agent = Agent(
    system_prompt="""You are a helpful math assistant.
    Help users with math calculations.
    Use the add and multiply tools when needed.""",
    tools=[add, multiply],
)

# Step 3: Use the agent
print(math_agent("What is 5 + 3?"))
# Output: "The sum of 5 and 3 is 8."

print(math_agent("What is 6 * 7?"))
# Output: "The product of 6 and 7 is 42."

# Step 4: Multi-turn conversation (agent remembers)
math_agent("My favorite number is 10")
print(math_agent("What is my favorite number times 5?"))
# Output: "Your favorite number is 10, so 10 * 5 = 50."
```

---

## Why Docstrings Matter

The LLM reads tool docstrings to understand:
- What the tool does
- What parameters it needs
- When to use it
- What to expect as output

### Bad Docstring:
```python
@tool
def search(q: str) -> str:
    """Search."""
    return results
```

**Problem:** LLM doesn't know what this tool does or when to use it

### Good Docstring:
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

**Benefit:** LLM understands exactly what this tool does and when to use it

---

## Real-World Example: Weather Assistant

```python
from strands import Agent, tool

# Define tools
@tool
def get_weather(city: str) -> str:
    """Get current weather for a city.
    
    Args:
        city: City name (e.g., "New York", "London")
    
    Returns:
        Weather information
    """
    # Simulated weather data
    weather = {
        "New York": "Sunny, 72°F",
        "London": "Rainy, 55°F",
        "Tokyo": "Cloudy, 68°F",
    }
    return weather.get(city, "City not found")

@tool
def convert_temperature(celsius: float) -> str:
    """Convert Celsius to Fahrenheit.
    
    Args:
        celsius: Temperature in Celsius
    
    Returns:
        Temperature in Fahrenheit
    """
    fahrenheit = (celsius * 9/5) + 32
    return f"{fahrenheit}°F"

# Create agent
weather_agent = Agent(
    system_prompt="""You are a helpful weather assistant.
    Help users check weather and convert temperatures.
    Be friendly and provide useful information.""",
    tools=[get_weather, convert_temperature],
)

# Use it
print(weather_agent("What's the weather in New York?"))
# Output: "The weather in New York is sunny with a temperature of 72°F."

print(weather_agent("Convert 25 Celsius to Fahrenheit"))
# Output: "25 Celsius is 77°F."

print(weather_agent("Should I bring an umbrella to London?"))
# Output: "Yes, it's rainy in London, so you should bring an umbrella."
```

---

## Key Concepts Explained

### Conversation History (Multi-turn)

Agents automatically remember previous messages:

```python
# Turn 1
weather_agent("My name is Alice")
# Agent remembers: User's name is Alice

# Turn 2
weather_agent("I'm planning a trip to New York")
# Agent remembers: User is Alice, planning trip to New York

# Turn 3
response = weather_agent("What should I pack?")
# Agent uses all previous context to answer
# Output: "Alice, for your trip to New York where it's sunny and 72°F,
#          I recommend packing light clothing and sunscreen."
```

### Tool Calling

The agent automatically decides which tool to use:

```python
# User asks about weather
weather_agent("What's the weather in London?")
# Agent thinks: "User wants weather, I should use get_weather tool"
# Agent calls: get_weather(city="London")
# Agent gets: "Rainy, 55°F"
# Agent responds: "It's rainy in London with a temperature of 55°F"

# User asks about temperature conversion
weather_agent("Convert 20 Celsius to Fahrenheit")
# Agent thinks: "User wants temperature conversion, I should use convert_temperature"
# Agent calls: convert_temperature(celsius=20)
# Agent gets: "68°F"
# Agent responds: "20 Celsius is 68°F"
```

### Error Handling

Always handle errors in your tools:

```python
@tool
def divide(a: int, b: int) -> str:
    """Divide two numbers.
    
    Args:
        a: Numerator
        b: Denominator
    
    Returns:
        The result
    """
    try:
        result = a / b
        return str(result)
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except Exception as e:
        return f"Error: {e}"
```

---

## Common Patterns

### Pattern 1: Simple Query
```python
agent = Agent(system_prompt="...", tools=[tool1])
response = agent("Question")
```

### Pattern 2: Interactive Loop
```python
while True:
    user_input = input("You > ")
    if user_input.lower() == "exit":
        break
    response = agent(user_input)
    print(f"Agent > {response}")
```

### Pattern 3: Multiple Tools
```python
agent = Agent(
    system_prompt="...",
    tools=[tool1, tool2, tool3],
)
# Agent decides which tool to use
```

### Pattern 4: Multi-turn Conversation
```python
agent("My name is Alice")
agent("I like Python")
response = agent("What's my name and what do I like?")
# Agent remembers both facts
```

---

## Best Practices

### ✅ DO:
1. **Write clear docstrings** - LLM reads these
2. **Include Args section** - Describe each parameter
3. **Handle errors** - Use try/except blocks
4. **Be specific in system prompt** - Guide the agent's behavior
5. **Test tools independently** - Ensure they work before adding to agent
6. **Use appropriate temperature** - 0.1-0.3 for factual, 0.7-0.9 for creative

### ❌ DON'T:
1. **Skip docstrings** - Agent won't know how to use the tool
2. **Hardcode API keys** - Use environment variables
3. **Make tools too complex** - Keep them focused
4. **Forget error handling** - Always handle exceptions
5. **Use vague system prompts** - Be specific about the agent's role

---

## Comparison: Agent vs Regular Program

### Regular Program:
```python
# You have to write all the logic
def help_user(question):
    if "weather" in question:
        return get_weather()
    elif "calculate" in question:
        return calculate()
    elif "search" in question:
        return search()
    else:
        return "I don't understand"
```

**Problems:**
- Hard to add new capabilities
- Lots of if/else statements
- Doesn't understand natural language well
- Can't handle variations in how users ask

### Agent:
```python
# Agent handles the logic
agent = Agent(
    system_prompt="You are helpful",
    tools=[get_weather, calculate, search],
)

response = agent(user_question)
```

**Benefits:**
- Easy to add new tools
- Understands natural language
- Handles variations automatically
- More flexible and powerful

---

## The Recipe Bot Example

The recipe bot is a real-world agent:

```python
from strands import Agent, tool
from ddgs import DDGS

# Tool: Web search
@tool
def websearch(keywords: str) -> str:
    """Search the web for recipes."""
    results = DDGS().text(keywords)
    return results

# Agent: Recipe assistant
recipe_agent = Agent(
    system_prompt="""You are RecipeBot, a helpful cooking assistant.
    Help users find recipes and answer cooking questions.
    Use the websearch tool to find recipes.""",
    tools=[websearch],
)

# Interactive loop
while True:
    user_input = input("You > ")
    if user_input.lower() == "exit":
        break
    response = recipe_agent(user_input)
    print(f"RecipeBot > {response}")
```

**How it works:**
1. User asks: "I want to make pasta carbonara"
2. Agent decides to use websearch tool
3. Tool searches for "pasta carbonara recipe"
4. Agent gets search results
5. Agent generates helpful response
6. User sees the response

---

## Summary

### What is an Agent?
A software program that can understand requests, decide what to do, use tools, and respond intelligently.

### What is Strands?
A Python framework that makes building agents easy by handling all the complexity.

### How to Build an Agent:
1. Define tools (functions with `@tool` decorator)
2. Create agent (combine tools + system prompt)
3. Use it (call agent with questions)

### Key Concepts:
- **Tools** = Functions the agent can call
- **System Prompt** = Instructions for the agent
- **Agent** = Orchestrator that combines everything
- **Conversation History** = Automatic memory of previous messages
- **Tool Calling** = Agent automatically decides which tool to use

### The Flow:
```
User Input → Agent → LLM → Tool Decision → Tool Execution → Response
```

---

## Next Steps

1. **Run my_first_agent.py** - See a working agent
2. **Run recipe_bot_explained.py** - See a real-world example
3. **Build your own agent** - Create a simple agent with one tool
4. **Add more tools** - Expand your agent's capabilities
5. **Deploy** - Put your agent in production

---

## Quick Reference

### Create a Tool:
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

### Create an Agent:
```python
agent = Agent(
    system_prompt="You are X",
    tools=[my_tool],
)
```

### Use the Agent:
```python
response = agent("Question")
```

### Interactive Loop:
```python
while True:
    user_input = input("You > ")
    response = agent(user_input)
    print(f"Agent > {response}")
```

That's it! You now understand agents and how to build them with Strands.
