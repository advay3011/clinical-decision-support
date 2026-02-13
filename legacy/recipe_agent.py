#!/usr/bin/env python3
"""
Simple Recipe Agent using Strands Framework
Gives you recipes when you ask for them
"""

from strands import Agent, tool
import json

print("""
╔════════════════════════════════════════════════════════════════════╗
║              SIMPLE RECIPE AGENT - STRANDS FRAMEWORK              ║
║                                                                    ║
║  Ask for a recipe, get ingredients and instructions               ║
╚════════════════════════════════════════════════════════════════════╝
""")

# ============================================================================
# STEP 1: CREATE TOOLS
# ============================================================================
"""
Tools are functions the agent can call.
We'll create 2 simple tools:
1. get_recipe - returns a recipe for a dish
2. get_cooking_tips - returns cooking tips
"""

@tool
def get_recipe(dish_name: str) -> str:
    """
    Get a recipe for a dish.
    
    INPUT: Name of the dish (e.g., "pasta", "chicken", "salad")
    OUTPUT: JSON with ingredients and instructions
    """
    
    # Simple recipe database
    recipes = {
        "pasta": {
            "name": "Simple Pasta",
            "ingredients": ["200g pasta", "2 cloves garlic", "2 tbsp olive oil", "salt", "pepper"],
            "instructions": [
                "Boil water and cook pasta",
                "Heat olive oil and sauté garlic",
                "Mix pasta with garlic oil",
                "Season with salt and pepper"
            ],
            "time": "15 minutes"
        },
        "chicken": {
            "name": "Grilled Chicken",
            "ingredients": ["2 chicken breasts", "2 tbsp olive oil", "lemon", "garlic", "salt", "pepper"],
            "instructions": [
                "Season chicken with salt, pepper, and garlic",
                "Heat oil in pan",
                "Cook chicken 6-7 minutes each side",
                "Squeeze lemon on top"
            ],
            "time": "20 minutes"
        },
        "salad": {
            "name": "Fresh Salad",
            "ingredients": ["lettuce", "tomato", "cucumber", "olive oil", "vinegar", "salt"],
            "instructions": [
                "Wash and chop vegetables",
                "Mix in a bowl",
                "Drizzle with olive oil and vinegar",
                "Season with salt"
            ],
            "time": "10 minutes"
        }
    }
    
    # Get recipe or return default
    recipe = recipes.get(dish_name.lower(), recipes["pasta"])
    return json.dumps(recipe)


@tool
def get_cooking_tips(cooking_method: str) -> str:
    """
    Get cooking tips for a method.
    
    INPUT: Cooking method (e.g., "grilling", "boiling", "frying")
    OUTPUT: JSON with tips
    """
    
    tips = {
        "grilling": {
            "method": "Grilling",
            "tips": [
                "Preheat grill for 10 minutes",
                "Oil the grates to prevent sticking",
                "Don't flip too often",
                "Use medium-high heat"
            ]
        },
        "boiling": {
            "method": "Boiling",
            "tips": [
                "Use plenty of water",
                "Add salt to water",
                "Bring to rolling boil before adding food",
                "Don't cover the pot"
            ]
        },
        "frying": {
            "method": "Frying",
            "tips": [
                "Heat oil to right temperature",
                "Don't overcrowd the pan",
                "Use medium-high heat",
                "Pat food dry before frying"
            ]
        }
    }
    
    tip = tips.get(cooking_method.lower(), tips["grilling"])
    return json.dumps(tip)


print("✓ Tool 1 created: get_recipe")
print("✓ Tool 2 created: get_cooking_tips")


# ============================================================================
# STEP 2: CREATE THE AGENT
# ============================================================================
"""
The Agent is the brain that:
1. Listens to user input
2. Decides which tools to use
3. Calls the tools
4. Returns the result

We tell it:
- Which model to use (Llama 2 via Ollama - free!)
- Which tools it can access
- How to behave (system prompt)
"""

def create_recipe_agent():
    """Create and return a recipe agent."""
    
    system_prompt = """You are a helpful recipe assistant. 
When someone asks for a recipe, use the get_recipe tool to find it.
When they ask for cooking tips, use the get_cooking_tips tool.
Be friendly and helpful. Explain the recipe clearly."""
    
    agent = Agent(
        model="ollama/llama2",  # Free local model
        tools=[get_recipe, get_cooking_tips],  # Tools the agent can use
        system_prompt=system_prompt
    )
    
    return agent


print("\n✓ Agent created with Llama 2 model")
print("✓ Agent has access to 2 tools")


# ============================================================================
# STEP 3: RUN THE AGENT
# ============================================================================
"""
This is where we actually use the agent.
We create it, then ask it questions.
It will use the tools to answer.
"""

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CREATING AGENT...")
    print("="*70)
    
    # Create the agent
    agent = create_recipe_agent()
    
    print("\n✓ Agent ready!")
    print("\nExample usage:")
    print('  response = agent("Give me a pasta recipe")')
    print('  response = agent("How do I grill chicken?")')
    print('  response = agent("What are boiling tips?")')
    
    # Test it with a few questions
    print("\n" + "="*70)
    print("TESTING AGENT")
    print("="*70)
    
    test_questions = [
        "Give me a pasta recipe",
        "How do I grill chicken?",
        "What are boiling tips?"
    ]
    
    for question in test_questions:
        print(f"\n[USER] {question}")
        print("-" * 70)
        try:
            response = agent(question)
            print(f"[AGENT] {response}")
        except Exception as e:
            print(f"[ERROR] {str(e)[:100]}")
    
    print("\n" + "="*70)
    print("AGENT READY FOR USE")
    print("="*70)
    print("\nTo use interactively:")
    print("  from recipe_agent import create_recipe_agent")
    print("  agent = create_recipe_agent()")
    print('  agent("Your question here")')
