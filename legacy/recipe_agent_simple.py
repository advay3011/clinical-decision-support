#!/usr/bin/env python3
"""
Simple Recipe Agent - No LLM needed
Just uses tools directly to give recipes
"""

import json

print("""
╔════════════════════════════════════════════════════════════════════╗
║              SIMPLE RECIPE AGENT                                  ║
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

def get_recipe(dish_name: str) -> dict:
    """
    Get a recipe for a dish.
    
    INPUT: Name of the dish (e.g., "pasta", "chicken", "salad")
    OUTPUT: Dictionary with ingredients and instructions
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
        },
        "eggs": {
            "name": "Scrambled Eggs",
            "ingredients": ["3 eggs", "butter", "salt", "pepper", "milk"],
            "instructions": [
                "Beat eggs with milk",
                "Heat butter in pan",
                "Pour eggs in",
                "Stir constantly until cooked",
                "Season with salt and pepper"
            ],
            "time": "5 minutes"
        }
    }
    
    # Get recipe or return default
    recipe = recipes.get(dish_name.lower(), recipes["pasta"])
    return recipe


def get_cooking_tips(cooking_method: str) -> dict:
    """
    Get cooking tips for a method.
    
    INPUT: Cooking method (e.g., "grilling", "boiling", "frying")
    OUTPUT: Dictionary with tips
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
    return tip


print("✓ Tool 1 created: get_recipe")
print("✓ Tool 2 created: get_cooking_tips")

# ============================================================================
# STEP 2: CREATE THE AGENT CLASS
# ============================================================================
"""
The Agent class is the brain that:
1. Listens to user input
2. Decides which tool to use
3. Calls the tool
4. Returns the result in a nice format
"""

class RecipeAgent:
    """Simple recipe agent that uses tools."""
    
    def __init__(self):
        """Initialize the agent."""
        self.tools = {
            "recipe": get_recipe,
            "tips": get_cooking_tips
        }
    
    def ask(self, question: str) -> str:
        """
        Ask the agent a question.
        
        The agent will figure out which tool to use and return the answer.
        """
        
        question_lower = question.lower()
        
        # Decide which tool to use based on the question
        if "recipe" in question_lower or "how to make" in question_lower or "make" in question_lower:
            # Extract dish name
            words = question_lower.split()
            dish = None
            
            # Look for dish names
            for word in words:
                if word in ["pasta", "chicken", "salad", "eggs"]:
                    dish = word
                    break
            
            if dish:
                result = self.tools["recipe"](dish)
                return self._format_recipe(result)
            else:
                return "I didn't catch which dish. Try: pasta, chicken, salad, or eggs"
        
        elif "tip" in question_lower or "how to" in question_lower:
            # Extract cooking method
            words = question_lower.split()
            method = None
            
            # Look for cooking methods
            for word in words:
                if word in ["grilling", "boiling", "frying"]:
                    method = word
                    break
            
            if method:
                result = self.tools["tips"](method)
                return self._format_tips(result)
            else:
                return "I didn't catch the cooking method. Try: grilling, boiling, or frying"
        
        else:
            return "I can help with recipes or cooking tips. Ask me for a recipe or tips!"
    
    def _format_recipe(self, recipe: dict) -> str:
        """Format a recipe nicely."""
        output = f"\n🍳 {recipe['name']}\n"
        output += f"⏱️  Time: {recipe['time']}\n\n"
        
        output += "📋 Ingredients:\n"
        for ingredient in recipe['ingredients']:
            output += f"  • {ingredient}\n"
        
        output += "\n📝 Instructions:\n"
        for i, instruction in enumerate(recipe['instructions'], 1):
            output += f"  {i}. {instruction}\n"
        
        return output
    
    def _format_tips(self, tips: dict) -> str:
        """Format tips nicely."""
        output = f"\n💡 {tips['method']} Tips:\n"
        for tip in tips['tips']:
            output += f"  • {tip}\n"
        return output


print("✓ Agent class created")

# ============================================================================
# STEP 3: RUN THE AGENT
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CREATING AGENT...")
    print("="*70)
    
    # Create the agent
    agent = RecipeAgent()
    
    print("\n✓ Agent ready!")
    print("\nExample questions:")
    print('  "Give me a pasta recipe"')
    print('  "How do I grill?"')
    print('  "Make me a chicken recipe"')
    print('  "Boiling tips"')
    
    # Test it with a few questions
    print("\n" + "="*70)
    print("TESTING AGENT")
    print("="*70)
    
    test_questions = [
        "Give me a pasta recipe",
        "How do I grill?",
        "Make me a chicken recipe",
        "Boiling tips"
    ]
    
    for question in test_questions:
        print(f"\n[USER] {question}")
        print("-" * 70)
        response = agent.ask(question)
        print(f"[AGENT] {response}")
    
    print("\n" + "="*70)
    print("AGENT READY FOR USE")
    print("="*70)
    print("\nTo use interactively:")
    print("  from recipe_agent_simple import RecipeAgent")
    print("  agent = RecipeAgent()")
    print('  agent.ask("Your question here")')
