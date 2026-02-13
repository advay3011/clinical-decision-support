#!/usr/bin/env python3
"""
Simple Strands Agent with Tool List
A minimal example showing how to create an agent with multiple tools.
"""

from strands import Agent, tool


# Define your tools
@tool
def add_numbers(a: float, b: float) -> str:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of the two numbers
    """
    result = a + b
    return f"{a} + {b} = {result}"


@tool
def multiply_numbers(a: float, b: float) -> str:
    """Multiply two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The product of the two numbers
    """
    result = a * b
    return f"{a} × {b} = {result}"


@tool
def get_weather(city: str) -> str:
    """Get weather information for a city.
    
    Args:
        city: Name of the city
    
    Returns:
        Weather information
    """
    # Simulated weather data
    weather_data = {
        "new york": "Sunny, 72°F",
        "london": "Cloudy, 59°F",
        "tokyo": "Rainy, 68°F",
        "paris": "Partly cloudy, 64°F",
    }
    city_lower = city.lower()
    return weather_data.get(city_lower, f"Weather data not available for {city}")


@tool
def get_time_zone(city: str) -> str:
    """Get the time zone for a city.
    
    Args:
        city: Name of the city
    
    Returns:
        Time zone information
    """
    timezones = {
        "new york": "EST (UTC-5)",
        "london": "GMT (UTC+0)",
        "tokyo": "JST (UTC+9)",
        "paris": "CET (UTC+1)",
    }
    city_lower = city.lower()
    return timezones.get(city_lower, f"Time zone not found for {city}")


# Create the agent with all tools
agent = Agent(
    system_prompt="""You are a helpful assistant with access to various tools.
    You can help with:
    - Math calculations (addition, multiplication)
    - Weather information
    - Time zone lookups
    
    Be friendly and provide clear answers.""",
    tools=[add_numbers, multiply_numbers, get_weather, get_time_zone],
)


def main():
    """Run the agent in interactive mode."""
    print("=" * 60)
    print("Simple Strands Agent with Tool List")
    print("=" * 60)
    print("\nAvailable tools:")
    print("  • add_numbers - Add two numbers")
    print("  • multiply_numbers - Multiply two numbers")
    print("  • get_weather - Get weather for a city")
    print("  • get_time_zone - Get time zone for a city")
    print("\nType 'exit' to quit\n")
    
    while True:
        try:
            user_input = input("You > ").strip()
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = agent(user_input)
            print(f"Agent > {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    # Uncomment below to test with specific prompts instead of interactive mode
    # response = agent("What's 15 plus 8?")
    # print(response)
    # 
    # response = agent("What's the weather in Tokyo?")
    # print(response)
    
    # Run interactive mode
    main()
