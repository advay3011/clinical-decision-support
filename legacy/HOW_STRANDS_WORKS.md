# How Strands Agentic AI Framework Works

## Overview

Strands is an agentic AI framework that orchestrates the interaction between:
1. **User Input** - What you ask the agent
2. **LLM (Large Language Model)** - The AI brain (Claude, GPT, etc.)
3. **Tools** - Functions the agent can call
4. **Conversation History** - Memory of previous messages

---

## The Complete Flow (Step by Step)

### Step 1: User Sends Input

```python
agent = Agent(system_prompt="You are helpful", tools=[calculator])
response = agent("What is 25 * 4?")
```

**What happens:**
- User input: "What is 25 * 4?"
- Input is captured by the agent

---

### Step 2: Agent Prepares the Context

The agent gathers everything needed:

```
┌─────────────────────────────────────────────────────────┐
│ CONTEXT PACKAGE                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. SYSTEM PROMPT                                        │
│    "You are a helpful assistant..."                     │
│                                                         │
│ 2. CONVERSATION HISTORY                                 │
│    [Previous messages from this strand]                 │
│                                                         │
│ 3. CURRENT USER MESSAGE                                 │
│    "What is 25 * 4?"                                    │
│                                                         │
│ 4. AVAILABLE TOOLS (with descriptions)                  │
│    - calculator(expression: str)                        │
│      "Calculate a math expression"                      │
│    - websearch(keywords: str)                           │
│      "Search the web"                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### Step 3: Send to LLM

The agent sends the context package to the LLM:

```python
# Internally, Strands does something like:
llm_input = {
    "system": system_prompt,
    "messages": conversation_history + [current_message],
    "tools": [
        {
            "name": "calculator",
            "description": "Calculate a math expression",
            "parameters": {
                "expression": "str"
            }
        },
        # ... other tools
    ]
}

response = llm.call(llm_input)
```

---

### Step 4: LLM Analyzes and Decides

The LLM reads everything and decides:

```
LLM's Thought Process:
├─ Read system prompt: "I'm a helpful assistant"
├─ Read conversation history: (empty on first turn)
├─ Read user message: "What is 25 * 4?"
├─ Read available tools:
│  ├─ calculator - for math
│  └─ websearch - for web search
├─ Analyze: "User wants to calculate 25 * 4"
├─ Decide: "I should use the calculator tool"
└─ Plan: "Call calculator(expression='25 * 4')"
```

**The LLM can respond in two ways:**

**Option A: Use a Tool**
```json
{
  "type": "tool_use",
  "tool_name": "calculator",
  "parameters": {
    "expression": "25 * 4"
  }
}
```

**Option B: Direct Response**
```json
{
  "type": "text",
  "content": "The answer is 100"
}
```

---

### Step 5: Agent Executes Tool (if needed)

If the LLM decided to use a tool:

```python
# Agent extracts the tool call
tool_name = "calculator"
parameters = {"expression": "25 * 4"}

# Agent finds the tool
tool = tools_dict[tool_name]

# Agent calls the tool
tool_result = tool(**parameters)
# Returns: "100"
```

**What happens inside the tool:**

```python
@tool
def calculator(expression: str) -> str:
    """Calculate a math expression."""
    try:
        result = eval(expression)  # Executes: 25 * 4
        return str(result)         # Returns: "100"
    except Exception as e:
        return f"Error: {e}"
```

---

### Step 6: Agent Sends Tool Result Back to LLM

The agent creates a new message with the tool result:

```python
# Agent sends back to LLM:
new_message = {
    "role": "assistant",
    "content": [
        {
            "type": "tool_result",
            "tool_name": "calculator",
            "result": "100"
        }
    ]
}

# LLM now has:
# - Original user message: "What is 25 * 4?"
# - Tool call it made: calculator(expression="25 * 4")
# - Tool result: "100"
```

---

### Step 7: LLM Generates Final Response

The LLM now generates a natural language response:

```python
# LLM thinks:
# "I called the calculator tool and got 100.
#  Now I should give a helpful response to the user."

response = "The answer is 100. (25 multiplied by 4 equals 100)"
```

---

### Step 8: Response Sent to User

```python
print(response)
# Output: "The answer is 100. (25 multiplied by 4 equals 100)"
```

---

### Step 9: Conversation History Saved

The agent saves this exchange for the next turn:

```python
# Conversation history is updated:
conversation_history = [
    {
        "role": "user",
        "content": "What is 25 * 4?"
    },
    {
        "role": "assistant",
        "content": "The answer is 100. (25 multiplied by 4 equals 100)"
    }
]

# Next time user sends a message, this history is included
```

---

## Complete Sequence Diagram

```
User
  │
  │ "What is 25 * 4?"
  ▼
┌─────────────────────────────────────────────────────────┐
│ AGENT                                                   │
│ ┌───────────────────────────────────────────────────┐  │
│ │ 1. Receive input                                  │  │
│ │ 2. Prepare context (system prompt + history)     │  │
│ │ 3. Add available tools                           │  │
│ └───────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Send context package
                     ▼
            ┌─────────────────────┐
            │ LLM (Claude, GPT)   │
            │                     │
            │ Analyzes:           │
            │ - System prompt     │
            │ - History           │
            │ - User message      │
            │ - Available tools   │
            │                     │
            │ Decides:            │
            │ "Use calculator"    │
            └────────┬────────────┘
                     │
                     │ "Call calculator(25 * 4)"
                     ▼
┌─────────────────────────────────────────────────────────┐
│ AGENT                                                   │
│ ┌───────────────────────────────────────────────────┐  │
│ │ 4. Extract tool call                              │  │
│ │ 5. Find tool: calculator                          │  │
│ │ 6. Execute: calculator("25 * 4")                  │  │
│ │ 7. Get result: "100"                              │  │
│ └───────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ "Tool result: 100"
                     ▼
            ┌─────────────────────┐
            │ LLM (Claude, GPT)   │
            │                     │
            │ Generates response: │
            │ "The answer is 100" │
            └────────┬────────────┘
                     │
                     │ Response text
                     ▼
┌─────────────────────────────────────────────────────────┐
│ AGENT                                                   │
│ ┌───────────────────────────────────────────────────┐  │
│ │ 8. Receive response                               │  │
│ │ 9. Save to conversation history                   │  │
│ │ 10. Return to user                                │  │
│ └───────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ "The answer is 100"
                     ▼
                   User
```

---

## Multi-Turn Conversation (How Memory Works)

### Turn 1:

```python
agent("My name is Alice")

# Internally:
# 1. User message: "My name is Alice"
# 2. Send to LLM with empty history
# 3. LLM responds: "Nice to meet you, Alice!"
# 4. Save to history:
#    [{"role": "user", "content": "My name is Alice"},
#     {"role": "assistant", "content": "Nice to meet you, Alice!"}]
```

### Turn 2:

```python
agent("What's my name?")

# Internally:
# 1. User message: "What's my name?"
# 2. Send to LLM WITH HISTORY from Turn 1
# 3. LLM reads history and knows: "User's name is Alice"
# 4. LLM responds: "Your name is Alice"
# 5. Save to history:
#    [{"role": "user", "content": "My name is Alice"},
#     {"role": "assistant", "content": "Nice to meet you, Alice!"},
#     {"role": "user", "content": "What's my name?"},
#     {"role": "assistant", "content": "Your name is Alice"}]
```

### Turn 3:

```python
agent("I like Python")

# Internally:
# 1. User message: "I like Python"
# 2. Send to LLM WITH FULL HISTORY from Turns 1 & 2
# 3. LLM reads history and knows: "User is Alice and likes Python"
# 4. LLM responds: "That's great, Alice! Python is a powerful language."
# 5. Save to history (now has 6 messages)
```

**Key Point:** Each turn includes ALL previous messages, so the LLM always has full context.

---

## Tool Calling Mechanism

### How LLM Decides to Use a Tool

```
LLM receives:
├─ System prompt: "You are a helpful assistant"
├─ Tools available:
│  ├─ calculator(expression: str)
│  │  "Calculate a math expression"
│  └─ websearch(keywords: str)
│     "Search the web"
└─ User message: "What is 25 * 4?"

LLM thinks:
"The user is asking for a calculation.
 I have a calculator tool.
 I should use it."

LLM responds:
{
  "type": "tool_use",
  "tool_name": "calculator",
  "parameters": {"expression": "25 * 4"}
}
```

### How Agent Executes the Tool

```python
# Agent receives LLM's response
response = {
    "type": "tool_use",
    "tool_name": "calculator",
    "parameters": {"expression": "25 * 4"}
}

# Agent extracts information
tool_name = response["tool_name"]  # "calculator"
parameters = response["parameters"]  # {"expression": "25 * 4"}

# Agent finds the tool
tool_function = self.tools[tool_name]  # The calculator function

# Agent calls the tool
try:
    result = tool_function(**parameters)  # calculator(expression="25 * 4")
    # result = "100"
except Exception as e:
    result = f"Error: {e}"

# Agent sends result back to LLM
return result
```

---

## Error Handling Flow

### When a Tool Fails

```python
@tool
def divide(a: int, b: int) -> str:
    """Divide two numbers."""
    try:
        result = a / b
        return str(result)
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"

# User asks: "What is 10 / 0?"
# LLM calls: divide(a=10, b=0)
# Tool returns: "Error: Cannot divide by zero"
# LLM receives error and responds: "I cannot divide by zero"
```

**Flow:**
```
User: "What is 10 / 0?"
  ↓
LLM: "Use divide tool"
  ↓
Agent: Calls divide(10, 0)
  ↓
Tool: Returns "Error: Cannot divide by zero"
  ↓
Agent: Sends error back to LLM
  ↓
LLM: Generates response: "I cannot divide by zero"
  ↓
User: Sees helpful error message
```

---

## System Prompt Role

The system prompt guides the LLM's behavior:

```python
# Example 1: Vague system prompt
system_prompt = "You are helpful"
# LLM might not know when to use tools

# Example 2: Specific system prompt
system_prompt = """You are a helpful math tutor.
Help students solve math problems.
Use the calculator tool for calculations.
Explain your reasoning step by step."""
# LLM knows exactly what to do and when to use tools
```

**How it works:**
```
LLM reads system prompt first
  ↓
LLM understands its role and responsibilities
  ↓
LLM reads user message
  ↓
LLM decides: "Based on my role, I should use this tool"
  ↓
LLM calls the appropriate tool
```

---

## Temperature and Creativity

Strands allows you to control LLM behavior:

```python
from strands.models import BedrockModel

# Low temperature = Factual, consistent
model = BedrockModel(
    model_id="anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0.1,  # Very factual
)
agent = Agent(model=model, system_prompt="...", tools=[...])

# High temperature = Creative, varied
model = BedrockModel(
    model_id="anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0.9,  # Very creative
)
agent = Agent(model=model, system_prompt="...", tools=[...])
```

**Effect:**
- **Low temperature (0.1)**: "The answer is exactly 100"
- **High temperature (0.9)**: "The answer is 100, which is a nice round number!"

---

## Token Management

Strands manages tokens (the "cost" of LLM calls):

```python
from strands.models import BedrockModel

model = BedrockModel(
    model_id="anthropic.claude-sonnet-4-20250514-v1:0",
    max_tokens=2048,  # Maximum response length
)

agent = Agent(model=model, system_prompt="...", tools=[...])

# If response would exceed max_tokens, LLM stops early
```

**Why it matters:**
- Tokens = Cost (you pay per token)
- Longer responses = More tokens = More cost
- Setting max_tokens prevents runaway costs

---

## Model Provider Abstraction

Strands abstracts different LLM providers:

```python
# Using Bedrock (default)
from strands.models import BedrockModel
model = BedrockModel(model_id="anthropic.claude-sonnet-4-20250514-v1:0")

# Using Anthropic directly
from strands.models.anthropic import AnthropicModel
model = AnthropicModel(model_id="claude-sonnet-4-20250514")

# Using OpenAI
from strands.models.openai import OpenAIModel
model = OpenAIModel(model_id="gpt-5-mini")

# Using Google Gemini
from strands.models.gemini import GeminiModel
model = GeminiModel(model_id="gemini-2.5-pro")

# All work the same way!
agent = Agent(model=model, system_prompt="...", tools=[...])
```

**Key Point:** You can switch LLM providers without changing your agent code.

---

## Conversation Strand Management

How Strands handles multiple conversations:

```python
# Each Agent instance = One strand
agent1 = Agent(system_prompt="...", tools=[...])  # Strand 1
agent2 = Agent(system_prompt="...", tools=[...])  # Strand 2

# Each maintains separate history
agent1("My name is Alice")
agent1("What's my name?")  # Remembers "Alice"

agent2("My name is Bob")
agent2("What's my name?")  # Remembers "Bob"

# They don't interfere with each other
```

**Internally:**
```python
# Agent 1 history
agent1.history = [
    {"role": "user", "content": "My name is Alice"},
    {"role": "assistant", "content": "..."},
    {"role": "user", "content": "What's my name?"},
    {"role": "assistant", "content": "Your name is Alice"}
]

# Agent 2 history (separate)
agent2.history = [
    {"role": "user", "content": "My name is Bob"},
    {"role": "assistant", "content": "..."},
    {"role": "user", "content": "What's my name?"},
    {"role": "assistant", "content": "Your name is Bob"}
]
```

---

## Complete Internal Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STRANDS FRAMEWORK                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ AGENT CLASS                                          │  │
│  │ ├─ system_prompt: str                               │  │
│  │ ├─ tools: List[Tool]                                │  │
│  │ ├─ model: LLMModel                                  │  │
│  │ ├─ conversation_history: List[Message]              │  │
│  │ └─ __call__(user_input: str) -> str                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ CONTEXT BUILDER                                      │  │
│  │ ├─ Gather system prompt                             │  │
│  │ ├─ Gather conversation history                      │  │
│  │ ├─ Add current user message                         │  │
│  │ └─ Format tools for LLM                             │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ LLM INTERFACE                                        │  │
│  │ ├─ Send context to LLM                              │  │
│  │ ├─ Receive response                                 │  │
│  │ └─ Parse tool calls or text                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ TOOL EXECUTOR                                        │  │
│  │ ├─ Check if tool call needed                        │  │
│  │ ├─ Find tool by name                                │  │
│  │ ├─ Execute tool with parameters                     │  │
│  │ └─ Handle errors                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ RESPONSE GENERATOR                                   │  │
│  │ ├─ Send tool result back to LLM                     │  │
│  │ ├─ LLM generates final response                     │  │
│  │ └─ Return to user                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ HISTORY MANAGER                                      │  │
│  │ ├─ Save user message                                │  │
│  │ ├─ Save assistant response                          │  │
│  │ └─ Maintain conversation state                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Summary: How Strands Works

1. **User sends input** → Agent receives it
2. **Agent prepares context** → Gathers system prompt, history, tools
3. **Send to LLM** → LLM analyzes everything
4. **LLM decides** → Use tool or respond directly
5. **Execute tool** (if needed) → Agent calls the tool
6. **Send result to LLM** → LLM gets tool output
7. **LLM generates response** → Creates natural language response
8. **Return to user** → User sees the response
9. **Save history** → Conversation is remembered for next turn

**Key Insight:** Strands automates all of this complexity so you only need to:
1. Define tools
2. Create an agent
3. Call the agent

The framework handles everything else!

---

## Why This Architecture Matters

### Without Strands:
```python
# You have to manually:
# 1. Call LLM API
# 2. Parse response
# 3. Decide which tool to use
# 4. Call the tool
# 5. Send result back to LLM
# 6. Manage conversation history
# 7. Handle errors
# ... hundreds of lines of complex code
```

### With Strands:
```python
agent = Agent(system_prompt="...", tools=[...])
response = agent("Question")
# Done! Strands handles everything
```

This is the power of the Strands framework!
