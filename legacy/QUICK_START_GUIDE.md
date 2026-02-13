# Strands Quick Start Guide

## 5-Minute Overview

### What is Strands?
A Python framework for building AI agents that can use tools and maintain conversations.

### The Three Things You Need:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. TOOLS                                               │
│     Functions your agent can call                       │
│     Marked with @tool decorator                         │
│                                                         │
│  2. SYSTEM PROMPT                                       │
│     Instructions for the agent                          │
│     Defines personality and behavior                    │
│                                                         │
│  3. AGENT                                               │
│     Combines tools + system prompt                      │
│     Handles everything else                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## The Minimal Example

```python
from strands import Agent, tool

# 1. Define a tool
@tool
def greet(name: str) -> str:
    """Greet someone by name.
    
    Args:
        name: The person's name
    
    Returns:
        A greeting message
    """
    return f"Hello, {name}!"

# 2. Create an agent
agent = Agent(
    system_prompt="You are a friendly assistant",
    tools=[greet],
)

# 3. Use it
response = agent("Say hello to Alice")
print(response)
```

---

## The Recipe Bot Pattern

```python
from strands import Agent, tool
from ddgs import DDGS

# 1. Define a tool
@tool
def websearch(keywords: str) -> str:
    """Search the web.
    
    Args:
        keywords: What to search for
    
    Returns:
        Search results
    """
    results = DDGS().text(keywords)
    return results

# 2. Create an agent
recipe_agent = Agent(
    system_prompt="You are RecipeBot, a helpful cooking assistant",
    tools=[websearch],
)

# 3. Use it in a loop
while True:
    user_input = input("You > ")
    if user_input.lower() == "exit":
        break
    response = recipe_agent(user_input)
    print(f"RecipeBot > {response}")
```

---

## Building Your Own Agent - Step by Step

### Step 1: Identify What Your Agent Should Do

```
Example: Customer Support Agent

What should it do?
- Look up customer orders
- Process refunds
- Answer FAQs
```

### Step 2: Create Tools for Each Capability

```python
@tool
def lookup_order(order_id: str) -> str:
    """Look up an order by ID.
    
    Args:
        order_id: The customer's order ID
    
    Returns:
        Order details
    """
    # Query your database
    return f"Order {order_id}: Status: Shipped"

@tool
def process_refund(order_id: str) -> str:
    """Process a refund for an order.
    
    Args:
        order_id: The order to refund
    
    Returns:
        Confirmation message
    """
    # Process refund
    return f"Refund processed for order {order_id}"

@tool
def get_faq(question: str) -> str:
    """Get answer to frequently asked questions.
    
    Args:
        question: The FAQ question
    
    Returns:
        The answer
    """
    faqs = {
        "shipping": "We ship within 2-3 business days",
        "returns": "30-day return policy",
    }
    return faqs.get(question.lower(), "FAQ not found")
```

### Step 3: Create the Agent

```python
support_agent = Agent(
    system_prompt="""You are a helpful customer support agent.
    Help customers with:
    - Order lookups
    - Refunds
    - General questions
    
    Be professional and empathetic.""",
    tools=[lookup_order, process_refund, get_faq],
)
```

### Step 4: Use It

```python
# Single query
response = support_agent("What's the status of my order?")
print(response)

# Or interactive
while True:
    user_input = input("Customer > ")
    response = support_agent(user_input)
    print(f"Support > {response}")
```

---

## Common Tool Patterns

### Pattern 1: Database Query
```python
@tool
def query_database(query: str) -> str:
    """Query the database.
    
    Args:
        query: SQL query
    
    Returns:
        Query results
    """
    # Execute query
    return results
```

### Pattern 2: API Call
```python
@tool
def call_api(endpoint: str, params: str) -> str:
    """Call an API endpoint.
    
    Args:
        endpoint: API endpoint
        params: Query parameters
    
    Returns:
        API response
    """
    response = requests.get(endpoint, params=params)
    return response.json()
```

### Pattern 3: Web Search
```python
@tool
def websearch(keywords: str) -> str:
    """Search the web.
    
    Args:
        keywords: Search terms
    
    Returns:
        Search results
    """
    results = DDGS().text(keywords)
    return results
```

### Pattern 4: Calculation
```python
@tool
def calculate(expression: str) -> str:
    """Calculate a math expression.
    
    Args:
        expression: Math expression (e.g., "2 + 2")
    
    Returns:
        The result
    """
    result = eval(expression)
    return str(result)
```

### Pattern 5: File Operations
```python
@tool
def read_file(filename: str) -> str:
    """Read a file.
    
    Args:
        filename: Path to file
    
    Returns:
        File contents
    """
    with open(filename, 'r') as f:
        return f.read()
```

---

## Debugging Tips

### Problem: Agent doesn't use the tool

**Check:**
1. Is the tool in the tools list?
2. Does the tool have a docstring?
3. Is the system prompt clear about when to use the tool?

**Fix:**
```python
# Bad
agent = Agent(
    system_prompt="You are helpful",
    tools=[my_tool],  # Tool is there
)

# Good
agent = Agent(
    system_prompt="""You are helpful.
    Use the my_tool to do X when users ask about Y.""",
    tools=[my_tool],
)
```

### Problem: Tool returns wrong format

**Check:**
1. Does the tool return a string?
2. Is the return value properly formatted?

**Fix:**
```python
# Bad
@tool
def my_tool(param: str) -> str:
    result = {"key": "value"}
    return result  # Returns dict, not string

# Good
@tool
def my_tool(param: str) -> str:
    result = {"key": "value"}
    return str(result)  # Returns string
```

### Problem: Agent gives incomplete responses

**Check:**
1. Is max_tokens set too low?
2. Is the task too complex?

**Fix:**
```python
from strands.models import BedrockModel

model = BedrockModel(
    model_id="anthropic.claude-sonnet-4-20250514-v1:0",
    max_tokens=4096,  # Increase this
)

agent = Agent(
    model=model,
    system_prompt="...",
    tools=[...],
)
```

---

## Real-World Examples

### Example 1: Weather Assistant
```python
@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    # Call weather API
    return f"Weather in {city}: Sunny, 72°F"

agent = Agent(
    system_prompt="You are a weather assistant",
    tools=[get_weather],
)

response = agent("What's the weather in New York?")
```

### Example 2: Code Helper
```python
@tool
def search_docs(query: str) -> str:
    """Search programming documentation."""
    # Search docs
    return results

agent = Agent(
    system_prompt="You are a helpful programming assistant",
    tools=[search_docs],
)

response = agent("How do I use list comprehensions in Python?")
```

### Example 3: Task Manager
```python
@tool
def add_task(task: str) -> str:
    """Add a task to the list."""
    # Add to database
    return f"Task added: {task}"

@tool
def list_tasks() -> str:
    """List all tasks."""
    # Query database
    return tasks

agent = Agent(
    system_prompt="You are a task management assistant",
    tools=[add_task, list_tasks],
)

response = agent("Add 'Buy groceries' to my task list")
```

---

## Installation

```bash
# Core SDK
pip install strands-agents

# Community tools (optional)
pip install strands-agents-tools

# For web search (recipe bot)
pip install duckduckgo-search

# For other providers (optional)
pip install 'strands-agents[anthropic]'  # Anthropic
pip install 'strands-agents[openai]'     # OpenAI
pip install 'strands-agents[gemini]'     # Google Gemini
```

---

## Configuration

### Bedrock (Default)
```bash
export AWS_BEDROCK_API_KEY=your_key
# OR
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### Anthropic
```bash
export ANTHROPIC_API_KEY=your_key
```

### OpenAI
```bash
export OPENAI_API_KEY=your_key
```

### Google Gemini
```bash
export GOOGLE_API_KEY=your_key
```

---

## Checklist: Building an Agent

- [ ] Identify what your agent should do
- [ ] Create tools for each capability
- [ ] Write clear docstrings for each tool
- [ ] Include Args section in docstrings
- [ ] Handle errors in tools
- [ ] Create agent with system_prompt and tools
- [ ] Test with simple queries
- [ ] Iterate based on results
- [ ] Add error handling
- [ ] Deploy!

---

## Key Takeaways

1. **Strands = Tools + System Prompt + Agent**
2. **Docstrings are critical** - LLM reads them
3. **Error handling matters** - Always handle exceptions
4. **System prompt guides behavior** - Be specific
5. **Conversation history is automatic** - No extra work needed
6. **Tools are just functions** - Use `@tool` decorator
7. **Test early and often** - Iterate quickly

---

## Next Steps

1. **Run the recipe bot** - Try the example
2. **Build a simple agent** - Create your first custom agent
3. **Add more tools** - Expand capabilities
4. **Try different LLMs** - Switch providers
5. **Deploy** - Put it in production

---

## Resources

- **Strands Documentation** - Official docs
- **Recipe Bot Example** - `samples/01-tutorials/01-fundamentals/01-first-agent/02-simple-interactive-usecase/recipe_bot.py`
- **STRANDS_GUIDE.md** - Comprehensive guide
- **RECIPE_BOT_BREAKDOWN.md** - Detailed explanation
- **STRANDS_ARCHITECTURE.md** - Visual diagrams

---

## Quick Reference

### Create Tool
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

### Create Agent
```python
agent = Agent(
    system_prompt="You are X",
    tools=[my_tool],
)
```

### Use Agent
```python
response = agent("Question")
```

### Interactive Loop
```python
while True:
    user_input = input("You > ")
    response = agent(user_input)
    print(f"Agent > {response}")
```

That's it! You're ready to build AI agents with Strands.
