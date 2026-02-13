#!/usr/bin/env python3
"""
Operations Consulting Scenario Demo
Simulates a real client engagement with problem → analysis → solution
"""

from ops_consult_agent import agent
import json

print("=" * 70)
print("OPERATIONS CONSULTING SCENARIO DEMO")
print("=" * 70)
print("\nSimulating: Client comes to you with a problem")
print("You analyze it and provide recommendations\n")

# ============================================================================
# SCENARIO 1: MANUFACTURING COST PROBLEM
# ============================================================================

print("\n" + "=" * 70)
print("SCENARIO 1: MANUFACTURING COMPANY - HIGH COSTS")
print("=" * 70)

client_problem_1 = """
CLIENT BRIEF:
"We're a mid-size manufacturing company. Our profit margins are shrinking.
Last year we made $2M in revenue but only $200k profit (10% margin).
We need to improve profitability. Can you help us understand where our
money is going and what we should do?"

Here's our cost breakdown:
- Raw Materials: $800,000 (40% of revenue)
- Labor: $600,000 (30% of revenue)
- Equipment & Maintenance: $200,000 (10% of revenue)
- Overhead (rent, utilities, admin): $150,000 (7.5% of revenue)
- Logistics & Distribution: $100,000 (5% of revenue)
- Marketing: $50,000 (2.5% of revenue)
- Other: $100,000 (5% of revenue)

Total Costs: $2,000,000
Revenue: $2,000,000
Profit: $0 (we're breaking even!)

What should we focus on to improve profitability?
"""

print("\n📞 CLIENT SAYS:")
print(client_problem_1)

print("\n[Consultant analyzing...]")
print("\n💼 CONSULTANT RESPONSE:\n")
response_1 = agent(client_problem_1)
print(response_1)

# ============================================================================
# SCENARIO 2: PROCESS BOTTLENECK PROBLEM
# ============================================================================

print("\n\n" + "=" * 70)
print("SCENARIO 2: LOGISTICS COMPANY - SLOW DELIVERY")
print("=" * 70)

client_problem_2 = """
CLIENT BRIEF:
"We're a logistics company and our delivery times are getting complaints.
Competitors deliver in 2-3 days, we're taking 5-7 days.
We're losing customers because of this.

Here's our delivery process:
- Order received & processing: 1 day
- Warehouse picking: 2 days
- Quality check: 1 day
- Packing: 0.5 days
- Loading & dispatch: 0.5 days
- Transit: 2 days

Total: 7 days average

We need to speed this up to compete. Where should we focus?"
"""

print("\n📞 CLIENT SAYS:")
print(client_problem_2)

print("\n[Consultant analyzing...]")
print("\n💼 CONSULTANT RESPONSE:\n")
response_2 = agent(client_problem_2)
print(response_2)

# ============================================================================
# SCENARIO 3: SALES DECLINE PROBLEM
# ============================================================================

print("\n\n" + "=" * 70)
print("SCENARIO 3: E-COMMERCE COMPANY - DECLINING SALES")
print("=" * 70)

client_problem_3 = """
CLIENT BRIEF:
"We're an e-commerce company and our sales are declining.
We used to do $100k/month, now we're at $70k/month.
That's a 30% drop in 3 months!

Here's what we know:
- Website traffic is stable (10,000 visitors/month)
- But conversion rate dropped from 2% to 1.4%
- Average order value stayed the same ($50)
- Customer acquisition cost increased 20%
- Repeat customer rate dropped from 40% to 25%

What's going wrong and how do we fix it?"
"""

print("\n📞 CLIENT SAYS:")
print(client_problem_3)

print("\n[Consultant analyzing...]")
print("\n💼 CONSULTANT RESPONSE:\n")
response_3 = agent(client_problem_3)
print(response_3)

# ============================================================================
# SCENARIO 4: WHAT-IF ANALYSIS
# ============================================================================

print("\n\n" + "=" * 70)
print("SCENARIO 4: FOLLOW-UP - WHAT-IF ANALYSIS")
print("=" * 70)

client_followup = """
CLIENT FOLLOW-UP:
"Thanks for the analysis. Let's say we implement your recommendations.

What if we:
1. Reduce raw material costs by 15% (through better supplier negotiations)
2. Reduce labor costs by 10% (through process automation)
3. Cut overhead by 20% (move to smaller facility)

How much would that improve our profitability?"
"""

print("\n📞 CLIENT ASKS:")
print(client_followup)

print("\n[Consultant analyzing...]")
print("\n💼 CONSULTANT RESPONSE:\n")
response_4 = agent(client_followup)
print(response_4)

# ============================================================================
# SUMMARY
# ============================================================================

print("\n\n" + "=" * 70)
print("DEMO COMPLETE")
print("=" * 70)

print("""
KEY TAKEAWAYS:

1. UNDERSTAND THE PROBLEM
   - Listen to the client's challenge
   - Gather relevant data
   - Classify the problem type

2. ANALYZE THE DATA
   - Find trends and patterns
   - Identify root causes
   - Quantify the impact

3. GENERATE RECOMMENDATIONS
   - Provide 2-4 actionable steps
   - Estimate impact for each
   - Prioritize by effort vs. impact

4. EXPLAIN THE REASONING
   - Use plain language
   - Show the data
   - Make it consultant-style

5. SUPPORT WHAT-IF ANALYSIS
   - Test scenarios
   - Show before/after
   - Help client make decisions

This is how you work as an operations consultant!
""")
