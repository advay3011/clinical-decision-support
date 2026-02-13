# What is a Strand?

## Quick Answer

A **strand** is a single conversation thread or execution path in an agent system. Think of it like a single conversation between you and an AI assistant.

---

## Understanding "Strands" (The Framework Name)

The framework is called **"Strands"** because it's designed to handle multiple independent conversation threads (strands) simultaneously.

### Analogy: Threads in a Tapestry

Imagine a tapestry with multiple threads:
- Each thread is independent
- Each thread can have its own color and pattern
- Multiple threads together create the complete tapestry
- Each thread maintains its own state

Similarly in Strands:
- Each strand is an independent conversation
- Each strand has its own conversation history
- Multiple strands can run simultaneously
- Each strand maintains its own context

---

## What is a Strand in Practice?

### Single Strand (One Conversation):

```python
from strands import Agent, tool

@tool
def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"

agent = Agent(
    system_prompt="You are friendly",
    tools=[greet],
)

# This is ONE STRAND - a single conversation
response1 = agent("Say hello to Alice")
response2 = agent("What did you just say?")
response3 = agent("Say hello to Bob")

# The agent remembers all three messages in this strand
```

### Multiple Strands (Multiple Conversations):

```python
# Strand 1: Conversation with Alice
agent1 = Agent(system_prompt="You are friendly", tools=[greet])
agent1("Say hello to Alice")
agent1("What's my name?")  # Remembers "Alice"

# Strand 2: Conversation with Bob (separate)
agent2 = Agent(system_prompt="You are friendly", tools=[greet])
agent2("Say hello to Bob")
agent2("What's my name?")  # Remembers "Bob" (different from agent1)

# Each agent maintains its own conversation history
```

---

## Key Characteristics of a Strand

### 1. Conversation History
Each strand maintains its own conversation history:

```python
# Strand 1
agent("My name is Alice")
agent("I like Python")
response = agent("What's my name?")
# Response: "Your name is Alice"

# Strand 2 (different agent)
agent2("My name is Bob")
agent2("I like JavaScript")
response2 = agent2("What's my name?")
# Response: "Your name is Bob"

# Each strand remembers its own context
```

### 2. Independent State
Each strand has independent state:

```python
# Strand 1: Weather conversation
weather_agent("I'm in New York")
weather_agent("What should I wear?")

# Strand 2: Cooking conversation (different agent)
recipe_agent("I have chicken")
recipe_agent("How do I cook it?")

# Each strand has different context
```

### 3. Isolated Execution
Each strand executes independently:

```python
# Strand 1
agent1("Question 1")
agent1("Question 2")

# Strand 2 (doesn't affect Strand 1)
agent2("Question 1")
agent2("Question 2")

# They don't interfere with each other
```

---

## Real-World Example: Customer Support

Imagine a customer support system with multiple conversations:

```python
from strands import Agent, tool

@tool
def lookup_order(order_id: str) -> str:
    """Look up an order."""
    return f"Order {order_id}: Status Shipped"

# Create the agent
support_agent = Agent(
    system_prompt="You are a helpful support agent",
    tools=[lookup_order],
)

# STRAND 1: Customer Alice
print("=== STRAND 1: Alice ===")
support_agent("My name is Alice")
support_agent("I have order #123")
response1 = support_agent("What's the status?")
print(response1)
# Agent remembers: Alice, Order #123

# STRAND 2: Customer Bob (separate conversation)
print("\n=== STRAND 2: Bob ===")
support_agent2 = Agent(
    system_prompt="You are a helpful support agent",
    tools=[lookup_order],
)
support_agent2("My name is Bob")
support_agent2("I have order #456")
response2 = support_agent2("What's the status?")
print(response2)
# Agent remembers: Bob, Order #456

# Each strand has its own context
```

---

## Strands vs Single Agent

### Single Agent (One Strand):
```python
agent = Agent(system_prompt="...", tools=[...])

# All conversations go through the same agent
agent("Question 1")
agent("Question 2")
agent("Question 3")

# All messages are in the same conversation history
# Agent remembers everything
```

### Multiple Agents (Multiple Strands):
```python
agent1 = Agent(system_prompt="...", tools=[...])
agent2 = Agent(system_prompt="...", tools=[...])
agent3 = Agent(system_prompt="...", tools=[...])

# Each agent is a separate strand
agent1("Question 1")
agent2("Question 1")
agent3("Question 1")

# Each has its own conversation history
# They don't interfere with each other
```

---

## Why Multiple Strands Matter

### Scenario 1: Multi-User System
```python
# Each user gets their own strand
users = {}

def handle_user_message(user_id, message):
    if user_id not in users:
        users[user_id] = Agent(system_prompt="...", tools=[...])
    
    agent = users[user_id]
    response = agent(message)
    return response

# User 1
handle_user_message("user1", "My name is Alice")
handle_user_message("user1", "What's my name?")
# Agent remembers: Alice

# User 2 (separate strand)
handle_user_message("user2", "My name is Bob")
handle_user_message("user2", "What's my name?")
# Agent remembers: Bob (different from user1)
```

### Scenario 2: Parallel Conversations
```python
# Handle multiple conversations simultaneously
import threading

def conversation_thread(user_id):
    agent = Agent(system_prompt="...", tools=[...])
    agent(f"I'm user {user_id}")
    response = agent("What's my ID?")
    print(f"User {user_id}: {response}")

# Run multiple conversations in parallel
threads = []
for i in range(5):
    t = threading.Thread(target=conversation_thread, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# Each thread has its own strand
```

---

## The Name "Strands"

The framework is called **Strands** because:

1. **Multiple Threads**: It can handle multiple conversation threads (strands)
2. **Independent**: Each strand is independent
3. **Woven Together**: Multiple strands can work together in a system
4. **Metaphor**: Like threads in a tapestry, each strand contributes to the whole

---

## Strand vs Agent

| Aspect | Strand | Agent |
|--------|--------|-------|
| **What it is** | A conversation thread | The software that runs the conversation |
| **Scope** | One conversation | Can handle multiple strands |
| **History** | Maintains conversation history | Maintains history for its strand |
| **Example** | "Conversation with Alice" | The Agent object that talks to Alice |

---

## Simple Explanation

**A strand is simply one conversation.**

When you create an Agent and have a conversation with it, that's one strand. If you create another Agent and have a different conversation, that's another strand.

```python
# Strand 1
agent1 = Agent(...)
agent1("Hello")
agent1("How are you?")

# Strand 2
agent2 = Agent(...)
agent2("Hi there")
agent2("What's up?")

# Two separate strands, two separate conversations
```

---

## Key Takeaway

- **Strands** (the framework) = Tool for building AI agents
- **A strand** (in the framework) = One conversation thread
- **Multiple strands** = Multiple independent conversations
- Each strand has its own conversation history and context

Think of it like this:
- **Strands** = The phone system
- **A strand** = One phone call
- **Multiple strands** = Multiple phone calls happening at the same time

---

## In Context of Your Learning

When you've been learning about Strands, you've been learning about:
- How to build agents (the framework)
- How to create tools
- How to manage conversations (strands)
- How to handle multiple conversations

The framework is called "Strands" because it's designed to elegantly handle multiple conversation threads (strands) in your AI agent system.

---

## Summary

**What is a strand?**
- A single conversation thread
- One independent execution path
- A conversation history between user and agent

**Why is the framework called Strands?**
- It handles multiple conversation threads
- Each thread is independent
- Multiple threads work together like strands in a tapestry

**In practice:**
- Each Agent object represents one strand
- Multiple Agents = Multiple strands
- Each strand maintains its own context and history
