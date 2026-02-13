# Strands Agents SDK - Complete Guide

## What is Strands?

**Strands** is an open-source Python framework for building AI agents that can:
- Use Large Language Models (LLMs) from multiple providers
- Call tools/functions to accomplish tasks
- Maintain conversation history automatically
- Handle complex multi-turn interactions

Think of it as a bridge between your code and AI models, making it easy to create intelligent agents without dealing with low-level API complexity.

### Key Concepts

1. **Agent**: The main object that orchestrates everything. It takes user input, decides what tools to use, and generates responses.
2. **Model**: The LLM powering the agent (Claude, GPT, Gemini, etc.)
3. **Tools**: Functions the agent can call to get information or perform actions
4. **System Prompt**: Instructions that define the agent's personality and behavior

---

## Understanding the Recipe Bot Example

Let's break down `recipe_bot.py` line by line:

### 1. Imports
```python
from ddgs import DDGS  # DuckDuckGo search library
from strands import Agent, tool  # Strands framework
```

### 2. Define a Custom Tool

```python
@tool
def websearch(keywords: str, region: str = "us-en", max_results: int | None = None) -> str:
    """Search the web to get updated information.
    Args:
        keywords (str): The search query keywords.
        region (str): The search region: wt-wt, us-en, uk-en, ru-ru, etc..
        max_results (int | None): The maximum number of results to return.
    Returns:
        List of dictionaries with search results.
    """
    try:
        results = DDGS().text(keywords, region=region, max_results=max_results)
        return results if results else "No results found."
    except RatelimitException:
        return "RatelimitException: Please try again after a short delay."
    except DDGSException as d:
        return f"DuckDuckGoSearchException: {d}"
    except Exception as e:
        return f"Exception: {e}"
```

**What's happening:**
- `@tool` decorator tells Strands this is a tool the agent can use
- The **docstring** is crucial - the LLM reads this to understand what the tool does
- The function takes parameters (keywords, region, max_results)
- It returns a string with search results
- Error handling ensures the agent gets useful feedback if something goes wrong

**Why the docstring matters:**
The LLM reads the docstring to decide:
- When to use this tool
- What parameters to pass
- What to expect as output

### 3. Create the Agent

```python
recipe_agent = Agent(
    system_prompt="""You are RecipeBot, a helpful cooking assistant.
    Help users find recipes based on ingredients and answer cooking questions.
    Use the websearch tool to find recipes when users mention ingredients or to look up cooking information.""",
    tools=[websearch],
)
```

**What's happening:**
- `system_prompt`: Defines the agent's personality and instructions
- `tools=[websearch]`: Gives the agent access to the websearch tool
- The agent will automatically decide when to use the websearch tool based on user input

### 4. Interactive Loop

```python
while True:
    user_input = input("\nYou > ")
    if user_input.lower() == "exit":
        print("Happy cooking! 🍽️")
        break
    response = recipe_agent(user_input)
    print(f"\nRecipeBot > {response}")
```

**What's happening:**
- Continuously asks for user input
- Passes input to the agent
- Agent processes it (may call websearch tool)
- Prints the response
- Maintains conversation history automatically

---

## How Strands Works (Under the Hood)

```
User Input
    ↓
Agent receives input
    ↓
Agent + LLM decide: "Do I need a tool?"
    ↓
If YES → Call the tool → Get result
    ↓
LLM generates response based on tool result
    ↓
Return response to user
    ↓
Conversation history is saved
```

---

## Building Your Own Agent - Step by Step

### Step 1: Define Your Tools

```python
from strands import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city.
    
    Args:
        city: The city name to get weather for
    
    Returns:
        Weather information as a string
    """
    # Your implementation here
    return f"Weather in {city}: Sunny, 72°F"

@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression.
    
    Args:
        expression: Math expression like "2 + 2"
    
    Returns:
        The result of the calculation
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
```

**Key Points:**
- Each tool is a Python function with `@tool` decorator
- Docstring is mandatory - LLM reads it to understand the tool
- Include Args section with parameter descriptions
- Return type should be string or easily convertible to string
- Handle errors gracefully

### Step 2: Create the Agent

```python
from strands import Agent

my_agent = Agent(
    system_prompt="""You are a helpful assistant that can check weather and do calculations.
    Use the available tools to help the user.""",
    tools=[get_weather, calculate],
)
```

**Configuration Options:**
- `system_prompt`: Instructions for the agent (required)
- `tools`: List of tools the agent can use (optional)
- `model`: Which LLM to use (defaults to Bedrock Claude 4 Sonnet)
- `temperature`: Creativity level (0.1 = factual, 0.9 = creative)
- `max_tokens`: Maximum response length

### Step 3: Use the Agent

```python
# Single query
response = my_agent("What's the weather in New York?")
print(response)

# Multi-turn conversation (agent remembers context)
my_agent("My name is Alice")
response = my_agent("What's my name?")
print(response)  # Will remember "Alice"
```

---

## Complete Example: Weather Assistant

```python
from strands import Agent, tool
import json

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city.
    
    Args:
        city: The city name
    
    Returns:
        Weather information
    """
    # Simulated weather data
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Rainy, 55°F",
        "Tokyo": "Cloudy, 68°F",
    }
    return weather_data.get(city, "City not found")

@tool
def convert_temperature(celsius: float, to_unit: str = "fahrenheit") -> str:
    """Convert temperature between units.
    
    Args:
        celsius: Temperature in Celsius
        to_unit: Target unit (fahrenheit or kelvin)
    
    Returns:
        Converted temperature
    """
    if to_unit == "fahrenheit":
        result = (celsius * 9/5) + 32
        return f"{result}°F"
    elif to_unit == "kelvin":
        result = celsius + 273.15
        return f"{result}K"
    return "Unknown unit"

# Create the agent
weather_agent = Agent(
    system_prompt="""You are a weather assistant. Help users check weather and convert temperatures.
    Be friendly and provide helpful information.""",
    tools=[get_weather, convert_temperature],
)

# Use it
if __name__ == "__main__":
    print("Weather Assistant")
    print("=" * 50)
    
    # Example 1
    response = weather_agent("What's the weather in New York?")
    print(f"Q: What's the weather in New York?\nA: {response}\n")
    
    # Example 2
    response = weather_agent("Convert 25 Celsius to Fahrenheit")
    print(f"Q: Convert 25 Celsius to Fahrenheit\nA: {response}\n")
    
    # Example 3 - Multi-turn
    weather_agent("I'm planning a trip to London")
    response = weather_agent("What should I wear?")
    print(f"Q: What should I wear?\nA: {response}\n")
```

---

## Key Differences: Recipe Bot vs Your Weather Agent

| Aspect | Recipe Bot | Weather Agent |
|--------|-----------|---------------|
| **Tool Type** | Web search (external API) | Local functions |
| **Tool Count** | 1 tool | 2 tools |
| **Interaction** | Interactive loop | Single/multi-turn queries |
| **Data Source** | Real-time web search | Simulated data |
| **Use Case** | Chat interface | Programmatic use |

---

## Common Patterns

### Pattern 1: Simple Query
```python
agent = Agent(system_prompt="You are helpful", tools=[tool1])
response = agent("User question")
```

### Pattern 2: Interactive Chat
```python
while True:
    user_input = input("You > ")
    if user_input.lower() == "exit":
        break
    response = agent(user_input)
    print(f"Agent > {response}")
```

### Pattern 3: Multi-turn with Context
```python
agent("My name is Alice")
agent("I like Python")
response = agent("What's my name and what do I like?")
# Agent remembers both facts
```

### Pattern 4: Error Handling
```python
try:
    response = agent("User input")
    print(response)
except Exception as e:
    print(f"Error: {e}")
```

---

## Model Providers

Strands supports multiple LLM providers:

### 1. Amazon Bedrock (Default)
```python
from strands import Agent

agent = Agent(
    system_prompt="You are helpful",
    tools=[tool1],
    # Uses Bedrock Claude 4 Sonnet by default
)
```

### 2. Anthropic Claude
```python
from strands import Agent
from strands.models.anthropic import AnthropicModel

model = AnthropicModel(
    model_id="claude-sonnet-4-20250514",
)

agent = Agent(
    model=model,
    system_prompt="You are helpful",
    tools=[tool1],
)
```

### 3. OpenAI GPT
```python
from strands import Agent
from strands.models.openai import OpenAIModel

model = OpenAIModel(
    model_id="gpt-5-mini",
)

agent = Agent(
    model=model,
    system_prompt="You are helpful",
    tools=[tool1],
)
```

---

## Best Practices

### ✅ DO:
1. **Write clear docstrings** - LLM reads these to understand tools
2. **Include Args section** - Describe each parameter
3. **Handle errors gracefully** - Return error messages, don't crash
4. **Use specific system prompts** - Guide the agent's behavior
5. **Test tools independently** - Ensure they work before adding to agent
6. **Use lower temperature for factual tasks** - temperature=0.1-0.3
7. **Use higher temperature for creative tasks** - temperature=0.7-0.9

### ❌ DON'T:
1. **Skip docstrings** - Agent won't know how to use the tool
2. **Hardcode API keys** - Use environment variables
3. **Make tools too complex** - Keep them focused and simple
4. **Forget error handling** - Always handle exceptions
5. **Use vague system prompts** - Be specific about the agent's role
6. **Ignore token limits** - Set appropriate max_tokens

---

## Troubleshooting

### Problem: "Tool not found" error
**Solution:** Ensure tool is in the tools list and has `@tool` decorator

### Problem: Agent doesn't use the tool
**Solution:** Check docstring is clear and system prompt mentions the tool

### Problem: Tool returns wrong format
**Solution:** Ensure tool returns a string or easily convertible value

### Problem: Agent gives incomplete responses
**Solution:** Increase max_tokens or simplify the task

---

## Summary

**Strands is:**
- A framework for building AI agents
- Works with multiple LLM providers
- Handles tool calling automatically
- Maintains conversation history
- Simple to use but powerful

**Recipe Bot demonstrates:**
- Custom tool creation with `@tool`
- Agent initialization with system prompt
- Interactive conversation loop
- Real-world use case (web search)

**To build your own agent:**
1. Define tools with `@tool` decorator
2. Create Agent with system_prompt and tools
3. Call agent with user input
4. Agent handles the rest!
