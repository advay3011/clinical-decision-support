#!/usr/bin/env python3
"""
Supply Chain Agent - SIMPLE DEMO
Easy-to-understand examples for beginners
"""

from supply_chain_optimizer_agent import agent
import json

print("=" * 70)
print("SUPPLY CHAIN HELPER - SIMPLE DEMO")
print("=" * 70)

# Example 1: Simple supplier choice
print("\n" + "=" * 70)
print("EXAMPLE 1: CHOOSING SUPPLIERS")
print("=" * 70)

example1 = """
I need to order 1000 items by day 15.

Here are my suppliers:
- Supplier A: costs $10 per item, delivers in 5 days, 95% reliable, can make 400 items
- Supplier B: costs $8 per item, delivers in 10 days, 80% reliable, can make 300 items
- Supplier C: costs $12 per item, delivers in 3 days, 98% reliable, can make 250 items
- Supplier D: costs $9 per item, delivers in 7 days, 85% reliable, can make 350 items

Which suppliers should I use? How much should I order from each?
"""

print(example1)
print("\n[Agent thinking...]\n")
response1 = agent(example1)
print(f"Agent: {response1}\n")

# Example 2: What-if scenario
print("\n" + "=" * 70)
print("EXAMPLE 2: WHAT-IF QUESTION")
print("=" * 70)

example2 = """
What if Supplier A gets delayed by 5 days? Can I still get my 1000 items by day 15?
"""

print(example2)
print("\n[Agent thinking...]\n")
response2 = agent(example2)
print(f"Agent: {response2}\n")

# Example 3: Reorder planning
print("\n" + "=" * 70)
print("EXAMPLE 3: REORDER PLANNING")
print("=" * 70)

example3 = """
I sell about 50 items per day. The suppliers take about 7 days to deliver.
When should I reorder? How much extra should I keep in stock?
"""

print(example3)
print("\n[Agent thinking...]\n")
response3 = agent(example3)
print(f"Agent: {response3}\n")

print("=" * 70)
print("DEMO COMPLETE")
print("=" * 70)
print("\nTry asking your own questions!")
print("Examples:")
print("  'I need 500 items by day 10'")
print("  'What if the cheapest supplier runs out of stock?'")
print("  'Which supplier is most reliable?'")
