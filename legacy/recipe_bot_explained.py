#!/usr/bin/env python3
"""
Enhanced Recipe Bot with detailed comments explaining how Strands works.
This is an educational version of the recipe_bot.py example.
"""

import logging
from strands import Agent, tool

# Configure logging to see what the agent is doing
logging.getLogger("strands").setLevel(logging.INFO)


# ============================================================================
# STEP 1: DEFINE CUSTOM TOOLS
# ============================================================================
# Tools are functions that the agent can call to accomplish tasks.
# The @tool decorator tells Strands this is a tool.

@tool
def search_recipes(ingredients: str, cuisine: str = "any") -> str:
    """Search for recipes based on ingredients.
    
    This is a CUSTOM TOOL - the agent will call this when users ask about recipes.
    
    Args:
        ingredients: Comma-separated list of ingredients (e.g., "chicken, garlic, tomato")
        cuisine: Type of cuisine (e.g., "Italian", "Asian", "Mexican")
    
    Returns:
        A string with recipe suggestions
    """
    # In a real app, this would search a database or API
    # For this example, we'll return simulated results
    
    recipes = {
        ("chicken", "italian"): [
            "Chicken Parmesan - Breaded chicken with tomato sauce and mozzarella",
            "Chicken Piccata - Chicken with lemon and capers",
        ],
        ("chicken", "asian"): [
            "Kung Pao Chicken - Spicy chicken with peanuts",
            "Teriyaki Chicken - Sweet and savory glazed chicken",
        ],
        ("pasta", "italian"): [
            "Carbonara - Pasta with eggs, bacon, and cheese",
            "Bolognese - Pasta with meat sauce",
        ],
    }
    
    # Normalize inputs
    ingredients_lower = ingredients.lower()
    cuisine_lower = cuisine.lower()
    
    # Search for matching recipes
    key = (ingredients_lower.split(",")[0].strip(), cuisine_lower)
    
    if key in recipes:
        result = f"Found recipes for {ingredients} ({cuisine}):\n"
        for recipe in recipes[key]:
            result += f"  • {recipe}\n"
        return result
    else:
        return f"No recipes found for {ingredients} in {cuisine} cuisine. Try different ingredients!"


@tool
def get_cooking_tips(technique: str) -> str:
    """Get cooking tips for a specific technique.
    
    This tool provides cooking advice and techniques.
    
    Args:
        technique: Cooking technique (e.g., "sauteing", "baking", "grilling")
    
    Returns:
        Cooking tips as a string
    """
    tips = {
        "sauteing": "Heat oil until shimmering, add ingredients, stir frequently. High heat, quick cooking.",
        "baking": "Preheat oven, measure ingredients precisely, don't open door while baking.",
        "grilling": "Preheat grill, oil grates, cook over medium-high heat, let meat rest after cooking.",
        "boiling": "Use enough water, add salt, bring to rolling boil, adjust heat to maintain boil.",
    }
    
    technique_lower = technique.lower()
    return tips.get(technique_lower, f"No tips found for {technique}. Try: sauteing, baking, grilling, or boiling.")


# ============================================================================
# STEP 2: CREATE THE AGENT
# ============================================================================
# The Agent is the main object that:
# 1. Receives user input
# 2. Decides which tools to use
# 3. Calls the tools
# 4. Generates a response
# 5. Maintains conversation history

recipe_agent = Agent(
    # system_prompt: Instructions that define the agent's personality and behavior
    # The LLM reads this to understand how to behave
    system_prompt="""You are RecipeBot, a friendly and helpful cooking assistant.
    
Your responsibilities:
- Help users find recipes based on ingredients they have
- Provide cooking tips and techniques
- Answer questions about food and cooking
- Be encouraging and supportive

When users mention ingredients, use the search_recipes tool to find recipes.
When users ask about cooking techniques, use the get_cooking_tips tool.
Always be friendly and provide helpful suggestions.""",
    
    # tools: List of tools the agent can use
    # The agent will automatically decide when to use each tool
    tools=[search_recipes, get_cooking_tips],
)


# ============================================================================
# STEP 3: USE THE AGENT
# ============================================================================
# The agent maintains conversation history automatically.
# Each call to agent() remembers previous messages.

def main():
    print("\n" + "="*60)
    print("👨‍🍳 RecipeBot - Your Cooking Assistant")
    print("="*60)
    print("Ask me about recipes, cooking tips, or food questions!")
    print("Type 'exit' to quit.\n")
    
    # Interactive loop - keeps the conversation going
    while True:
        try:
            user_input = input("You > ").strip()
            
            # Exit condition
            if user_input.lower() == "exit":
                print("\nHappy cooking! 🍽️ Goodbye!")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Call the agent with user input
            # The agent will:
            # 1. Read the user input
            # 2. Decide if it needs to use any tools
            # 3. Call the appropriate tools
            # 4. Generate a response based on tool results
            # 5. Remember this conversation for next turn
            response = recipe_agent(user_input)
            
            print(f"\nRecipeBot > {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


# ============================================================================
# EXAMPLE: How the Agent Works (Step by Step)
# ============================================================================
"""
Example conversation:

User: "I have chicken and garlic, what can I make?"

Agent's thought process:
1. Read: "I have chicken and garlic, what can I make?"
2. Think: "User is asking for recipes with specific ingredients"
3. Decide: "I should use the search_recipes tool"
4. Call: search_recipes(ingredients="chicken, garlic", cuisine="any")
5. Get result: "Found recipes for chicken, garlic (any):
   • Chicken Parmesan - Breaded chicken with tomato sauce and mozzarella
   • Chicken Piccata - Chicken with lemon and capers"
6. Generate response: "Great! With chicken and garlic, you can make..."
7. Return response to user
8. Remember this conversation for next turn

User: "How do I sauté the chicken?"

Agent's thought process:
1. Read: "How do I sauté the chicken?"
2. Think: "User is asking about sauteing technique"
3. Remember: "We were just talking about chicken recipes"
4. Decide: "I should use the get_cooking_tips tool"
5. Call: get_cooking_tips(technique="sauteing")
6. Get result: "Heat oil until shimmering, add ingredients, stir frequently..."
7. Generate response: "To sauté your chicken, here's what you do..."
8. Return response to user
"""


if __name__ == "__main__":
    main()
