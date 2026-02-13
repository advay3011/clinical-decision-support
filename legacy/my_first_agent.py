#!/usr/bin/env python3
"""
Simple example agent using Strands SDK with Bedrock.
This agent can answer questions and perform calculations.
"""

from strands import Agent
from strands_tools import calculator, python_repl

# Create an agent with community tools
# Uses Amazon Bedrock Claude 4 Sonnet by default
agent = Agent(
    tools=[calculator, python_repl],
    system_prompt="You are a helpful assistant that can answer questions and perform calculations."
)

# Test the agent with a simple question
print("Testing your first Strands agent!\n")
print("=" * 50)

# Example 1: Simple question
response = agent("What is 25 * 4?")
print(f"Q: What is 25 * 4?\nA: {response}\n")

# Example 2: Multi-turn conversation (agent maintains context)
agent("My name is Alice")
response = agent("What's my name?")
print(f"Q: What's my name?\nA: {response}\n")

# Example 3: More complex calculation
response = agent("Calculate the square root of 144 and multiply by 2")
print(f"Q: Calculate the square root of 144 and multiply by 2\nA: {response}\n")

print("=" * 50)
print("✅ Agent is working! Try asking it more questions.")
