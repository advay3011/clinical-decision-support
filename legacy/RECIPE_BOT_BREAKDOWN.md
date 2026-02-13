# Recipe Bot - Line by Line Breakdown

This document explains the original `recipe_bot.py` in detail.

---

## The Complete Code with Annotations

```python
# ============================================================================
# IMPORTS
# ============================================================================

import logging
# logging: Python's built-in logging module
# Used to see what the agent is doing (debugging)

from ddgs import DDGS
# DDGS: DuckDuckGo Search library
# Allows us to search the web for recipes
# Install with: pip install duckduckgo-search

from ddgs.exceptions import DDGSException, RatelimitException
# Exception handling for DuckDuckGo search
# RatelimitException: Too many requests too fast
# DDGSException: General search errors

from strands import Agent, tool
# Agent: The main Strands class that orchestrates everything
# tool: Decorator that marks a function as a tool the agent can use


# ============================================================================
# CONFIGURE LOGGING
# ============================================================================

logging.getLogger("strands").setLevel(logging.INFO)
# This shows what the agent is doing
# Set to DEBUG for even more detailed information
# Set to WARNING to see less output


# ============================================================================
# DEFINE CUSTOM TOOLS
# ============================================================================

@tool  # ← This decorator tells Strands this is a tool
def websearch(
    keywords: str,                    # Required parameter: search terms
    region: str = "us-en",           # Optional parameter: search region
    max_results: int | None = None   # Optional parameter: max results
) -> str:                             # Returns a string
    """Search the web to get updated information.
    
    This docstring is CRITICAL - the LLM reads this to understand:
    - What the tool does
    - What parameters it needs
    - When to use it
    
    Args:
        keywords (str): The search query keywords.
        region (str): The search region: wt-wt, us-en, uk-en, ru-ru, etc..
        max_results (int | None): The maximum number of results to return.
    
    Returns:
        List of dictionaries with search results.
    """
    
    # Try to search using DuckDuckGo
    try:
        # DDGS().text() performs the actual web search
        results = DDGS().text(
            keywords,              # What to search for
            region=region,         # Which region
            max_results=max_results # How many results
        )
        
        # Return results if found, otherwise return "No results found."
        return results if results else "No results found."
    
    # Handle rate limiting (too many requests)
    except RatelimitException:
        return "RatelimitException: Please try again after a short delay."
    
    # Handle DuckDuckGo specific errors
    except DDGSException as d:
        return f"DuckDuckGoSearchException: {d}"
    
    # Handle any other unexpected errors
    except Exception as e:
        return f"Exception: {e}"


# ============================================================================
# CREATE THE AGENT
# ============================================================================

recipe_agent = Agent(
    # system_prompt: Instructions that define the agent's personality
    # The LLM reads this to understand how to behave
    system_prompt="""You are RecipeBot, a helpful cooking assistant.
    Help users find recipes based on ingredients and answer cooking questions.
    Use the websearch tool to find recipes when users mention ingredients or to look up cooking information.""",
    
    # tools: List of tools the agent can use
    # The agent will automatically decide when to use each tool
    tools=[websearch],
)


# ============================================================================
# MAIN PROGRAM - INTERACTIVE LOOP
# ============================================================================

if __name__ == "__main__":
    # This runs only when the script is executed directly
    # (not when imported as a module)
    
    print("\n👨‍🍳 RecipeBot: Ask me about recipes or cooking! Type 'exit' to quit.\n")
    
    # Infinite loop for continuous conversation
    while True:
        # Get user input from command line
        user_input = input("\nYou > ")
        
        # Check if user wants to exit
        if user_input.lower() == "exit":
            print("Happy cooking! 🍽️")
            break  # Exit the loop
        
        # Call the agent with user input
        # The agent will:
        # 1. Read the user input
        # 2. Decide if it needs to use the websearch tool
        # 3. Call websearch if needed
        # 4. Generate a response based on the search results
        # 5. Remember this conversation for the next turn
        response = recipe_agent(user_input)
        
        # Print the agent's response
        print(f"\nRecipeBot > {response}")
```

---

## Step-by-Step Execution Example

### Example Conversation:

```
User Input: "I want to make pasta carbonara"

Step 1: Agent receives input
  Input: "I want to make pasta carbonara"

Step 2: Agent sends to LLM with:
  - System prompt: "You are RecipeBot..."
  - User input: "I want to make pasta carbonara"
  - Available tools: [websearch]
  - Conversation history: (empty on first turn)

Step 3: LLM analyzes
  "The user is asking about a specific recipe (pasta carbonara).
   I should use the websearch tool to find recipes."

Step 4: LLM decides to use websearch
  Tool call: websearch(keywords="pasta carbonara recipe")

Step 5: websearch executes
  - Searches DuckDuckGo for "pasta carbonara recipe"
  - Returns search results with recipe links and descriptions

Step 6: LLM generates response
  "Here's how to make pasta carbonara:
   - Cook pasta
   - Mix eggs with cheese
   - Combine with pasta and bacon
   - Serve immediately"

Step 7: Response sent to user
  Output: "Here's how to make pasta carbonara..."

Step 8: Conversation history saved
  History: [
    {"role": "user", "content": "I want to make pasta carbonara"},
    {"role": "assistant", "content": "Here's how to make..."}
  ]
```

---

## Key Concepts Explained

### 1. The @tool Decorator

```python
@tool
def websearch(keywords: str) -> str:
    """Search the web..."""
    # Implementation
```

**What it does:**
- Marks the function as a tool the agent can use
- Strands automatically extracts the docstring
- LLM reads the docstring to understand the tool

**Why it matters:**
- Without `@tool`, the agent can't use the function
- The docstring is how the LLM learns about the tool

### 2. The Docstring

```python
"""Search the web to get updated information.

Args:
    keywords (str): The search query keywords.
    region (str): The search region: wt-wt, us-en, uk-en, ru-ru, etc..
    max_results (int | None): The maximum number of results to return.

Returns:
    List of dictionaries with search results.
"""
```

**What the LLM sees:**
- Tool name: `websearch`
- Description: "Search the web to get updated information"
- Parameters: keywords, region, max_results
- Return type: List of dictionaries

**How the LLM uses it:**
- When user asks about recipes, LLM thinks: "I should use websearch"
- LLM decides what parameters to pass
- LLM calls: `websearch(keywords="pasta carbonara recipe")`

### 3. Error Handling

```python
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

**Why it matters:**
- If search fails, the agent gets a helpful error message
- Agent can then explain to user what went wrong
- Without error handling, the agent would crash

### 4. The Agent

```python
recipe_agent = Agent(
    system_prompt="""You are RecipeBot, a helpful cooking assistant.
    Help users find recipes based on ingredients and answer cooking questions.
    Use the websearch tool to find recipes when users mention ingredients or to look up cooking information.""",
    tools=[websearch],
)
```

**What it does:**
- Creates an agent with a specific personality (system_prompt)
- Gives it access to the websearch tool
- Automatically maintains conversation history

**How it works:**
- Each call to `recipe_agent(user_input)` processes the input
- Agent decides if it needs tools
- Agent generates response
- Conversation history is saved for next turn

### 5. The Interactive Loop

```python
while True:
    user_input = input("\nYou > ")
    if user_input.lower() == "exit":
        print("Happy cooking! 🍽️")
        break
    response = recipe_agent(user_input)
    print(f"\nRecipeBot > {response}")
```

**What it does:**
- Continuously asks for user input
- Processes each input with the agent
- Maintains conversation across multiple turns
- Allows user to exit with "exit" command

**Why it matters:**
- Enables natural conversation
- Agent remembers previous messages
- User can ask follow-up questions

---

## How This Differs from Your First Agent

### Your First Agent (my_first_agent.py)
```python
from strands import Agent
from strands_tools import calculator, python_repl

agent = Agent(
    tools=[calculator, python_repl],
    system_prompt="You are a helpful assistant..."
)

response = agent("What is 25 * 4?")
print(response)
```

**Characteristics:**
- Uses pre-built tools (calculator, python_repl)
- Single query (not interactive)
- No web search
- Simpler setup

### Recipe Bot (recipe_bot.py)
```python
from strands import Agent, tool
from ddgs import DDGS

@tool
def websearch(keywords: str) -> str:
    """Search the web..."""
    results = DDGS().text(keywords)
    return results

recipe_agent = Agent(
    system_prompt="You are RecipeBot...",
    tools=[websearch],
)

while True:
    user_input = input("\nYou > ")
    response = recipe_agent(user_input)
    print(f"\nRecipeBot > {response}")
```

**Characteristics:**
- Custom tool (websearch)
- Interactive loop
- Real web search
- More complex setup

---

## Comparison Table

| Aspect | Your First Agent | Recipe Bot |
|--------|------------------|-----------|
| **Tools** | Pre-built (calculator, python_repl) | Custom (websearch) |
| **Tool Source** | strands_tools library | Custom function with @tool |
| **Interaction** | Single query | Interactive loop |
| **Data Source** | Local computation | Web search (DuckDuckGo) |
| **Complexity** | Simple | Intermediate |
| **Use Case** | Learning/testing | Real-world chatbot |
| **Conversation** | Single turn | Multi-turn |
| **Error Handling** | Basic | Comprehensive |

---

## What You Learned

### From the Recipe Bot:

1. **How to create custom tools** - Use `@tool` decorator
2. **Why docstrings matter** - LLM reads them to understand tools
3. **How to handle errors** - Try/except blocks for robustness
4. **How to create interactive agents** - While loop for continuous conversation
5. **How to use external APIs** - DuckDuckGo search integration
6. **How conversation history works** - Agent automatically maintains it

### Key Takeaway:

The recipe bot shows that Strands makes it easy to:
- Define what your agent can do (tools)
- Tell it how to behave (system_prompt)
- Let it handle the rest (tool calling, conversation history)

---

## Next Steps

### To Build Your Own Agent:

1. **Define your tools** - What should your agent be able to do?
2. **Write clear docstrings** - Help the LLM understand your tools
3. **Create the agent** - Combine tools + system_prompt
4. **Test it** - Try different inputs and see how it behaves
5. **Iterate** - Improve tools and system_prompt based on results

### Example: Customer Support Agent

```python
from strands import Agent, tool

@tool
def lookup_order(order_id: str) -> str:
    """Look up order details by order ID.
    
    Args:
        order_id: The customer's order ID
    
    Returns:
        Order details including status and items
    """
    # Query your database
    return f"Order {order_id}: Status: Shipped, Items: 2"

@tool
def process_refund(order_id: str, reason: str) -> str:
    """Process a refund for an order.
    
    Args:
        order_id: The order to refund
        reason: Reason for refund
    
    Returns:
        Confirmation of refund processing
    """
    # Process refund in your system
    return f"Refund processed for order {order_id}"

support_agent = Agent(
    system_prompt="""You are a helpful customer support agent.
    Help customers with order lookups and refunds.
    Be empathetic and professional.""",
    tools=[lookup_order, process_refund],
)

# Use it
response = support_agent("I want to return my order")
print(response)
```

This is the pattern: **Tools + System Prompt + Agent = Intelligent Assistant**
