"""First Agent Demo - Running all examples from 01-first-agent.ipynb"""

import logging
import warnings
warnings.filterwarnings(action="ignore", message=r"datetime.datetime.utcnow")

from strands import Agent, tool
from strands_tools import calculator
from ddgs import DDGS
from ddgs.exceptions import RatelimitException, DDGSException

# Configure logging
logging.getLogger("strands").setLevel(logging.INFO)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

print("\n" + "="*70)
print("FIRST AGENT DEMO - Learning Strands Agents")
print("="*70)

# ============================================================================
# SECTION 1: Simple Agent (No Tools)
# ============================================================================
print("\n📌 SECTION 1: Simple Agent (No Tools)")
print("-" * 70)
print("Creating a basic agent that just talks...\n")

agent_simple = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt="You are a helpful assistant that provides concise responses."
)

print("Question: Hello! Tell me a joke.")
response1 = agent_simple("Hello! Tell me a joke.")
print(f"Response: {response1}\n")

# ============================================================================
# SECTION 2: Agent with Tools
# ============================================================================
print("\n" + "="*70)
print("📌 SECTION 2: Agent with Tools (Calculator + Custom Weather)")
print("-" * 70)
print("Creating an agent with tools...\n")

# Create a custom tool
@tool
def weather():
    """Get weather information"""
    return "sunny and 72°F"

# Create agent with tools
agent_with_tools = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculations and tell the weather."
)

print("Question: What is the weather today?")
response2 = agent_with_tools("What is the weather today?")
print(f"Response: {response2}\n")

print("Question: What is 25 times 8?")
response3 = agent_with_tools("What is 25 times 8?")
print(f"Response: {response3}\n")

# ============================================================================
# SECTION 3: Invoking Tools Directly
# ============================================================================
print("\n" + "="*70)
print("📌 SECTION 3: Invoking Tools Directly")
print("-" * 70)
print("Calling a tool directly without going through the agent...\n")

print("Calling calculator tool directly: sin(x) derivative")
result = agent_with_tools.tool.calculator(expression="sin(x)", mode="derive", wrt="x", order=2)
print(f"Result: {result}\n")

# ============================================================================
# SECTION 4: RecipeBot with WebSearch
# ============================================================================
print("\n" + "="*70)
print("📌 SECTION 4: RecipeBot with WebSearch Tool")
print("-" * 70)
print("Creating a task-specific agent with web search...\n")

# Define websearch tool
@tool
def websearch(keywords: str, region: str = "us-en", max_results: int | None = None) -> str:
    """Search the web to get updated information.
    Args:
        keywords (str): The search query keywords.
        region (str): The search region: wt-wt, us-en, uk-en, ru-ru, etc.
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

# Create RecipeBot
recipe_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt="""You are RecipeBot, a helpful cooking assistant.
    Help users find recipes based on ingredients and answer cooking questions.
    Use the websearch tool to find recipes when users mention ingredients or to
    look up cooking information.""",
    tools=[websearch],
)

print("Question: Suggest a recipe with chicken and broccoli.")
response4 = recipe_agent("Suggest a recipe with chicken and broccoli.")
print(f"Response: {response4}\n")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✅ DEMO COMPLETED!")
print("="*70)
print("""
You've seen:
1. ✓ Simple Agent (just talks)
2. ✓ Agent with Tools (calculator + weather)
3. ✓ Direct Tool Invocation (calling tools directly)
4. ✓ RecipeBot (real-world example with web search)

Key Takeaways:
- Agents are AI assistants that can use tools
- Tools give agents superpowers (search, calculate, etc.)
- You can create custom tools with @tool decorator
- Agents decide when and how to use tools
- System prompts control agent behavior
""")
print("="*70 + "\n")
