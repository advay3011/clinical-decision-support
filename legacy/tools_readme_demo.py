"""Tools README Demo - Running All Examples from the README
Demonstrates all 3 ways to create tools with best practices
"""

import logging
from strands import Agent, tool
from strands.types.tools import ToolResult, ToolUse
from typing import Any

# Configure logging
logging.getLogger("strands").setLevel(logging.INFO)

print("\n" + "="*70)
print("🛠️  TOOLS README DEMO - All 3 Ways with Best Practices")
print("="*70)

# ============================================================================
# WAY 1: Using @tool Decorator (Simplest)
# ============================================================================
print("\n📌 WAY 1: Using @tool Decorator")
print("-" * 70)
print("Simplest way - uses Python docstrings and type hints\n")

@tool
def search_documents(query: str, max_results: int = 5) -> str:
    """
    Search through documents to find relevant information.
    
    Args:
        query: The search query string
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        String containing search results
    """
    # Simulated search results
    results = [
        f"Document 1: Found '{query}' in introduction",
        f"Document 2: Found '{query}' in chapter 3",
        f"Document 3: Found '{query}' in conclusion",
    ]
    return "\n".join(results[:max_results])

print("✓ Tool created with @tool decorator")
print("✓ Uses docstrings for documentation")
print("✓ Uses type hints for validation")
print("✓ Simple and quick!\n")

# ============================================================================
# WAY 2: Using TOOL_SPEC Dictionary (Most Control)
# ============================================================================
print("📌 WAY 2: Using TOOL_SPEC Dictionary")
print("-" * 70)
print("More control - define exact input/output format\n")

TOOL_SPEC = {
    "name": "calculate_statistics",
    "description": "Calculate statistics for a list of numbers",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "numbers": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "List of numbers to analyze"
                },
                "operation": {
                    "type": "string",
                    "description": "Operation: sum, average, min, max",
                    "default": "average"
                }
            },
            "required": ["numbers"]  # Only numbers is required
        }
    }
}

def calculate_statistics(tool: ToolUse, **kwargs: Any) -> ToolResult:
    """Calculate statistics on numbers"""
    
    tool_use_id = tool["toolUseId"]
    
    try:
        numbers = tool["input"].get("numbers", [])
        operation = tool["input"].get("operation", "average")
        
        if not numbers:
            return {
                "toolUseId": tool_use_id,
                "status": "error",
                "content": [{"text": "No numbers provided"}]
            }
        
        # Calculate based on operation
        if operation == "sum":
            result = sum(numbers)
        elif operation == "average":
            result = sum(numbers) / len(numbers)
        elif operation == "min":
            result = min(numbers)
        elif operation == "max":
            result = max(numbers)
        else:
            return {
                "toolUseId": tool_use_id,
                "status": "error",
                "content": [{"text": f"Unknown operation: {operation}"}]
            }
        
        return {
            "toolUseId": tool_use_id,
            "status": "success",
            "content": [{"text": f"{operation.capitalize()}: {result}"}]
        }
    
    except Exception as e:
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": f"Error: {str(e)}"}]
        }

print("✓ Tool created with TOOL_SPEC dictionary")
print("✓ Full control over input schema")
print("✓ Explicit error handling")
print("✓ Professional format!\n")

# ============================================================================
# WAY 3: MCP Tools (External Tools) - Simulated
# ============================================================================
print("📌 WAY 3: MCP Tools (External Tools)")
print("-" * 70)
print("Use pre-made tools from external servers\n")

print("✓ MCP tools connect to external servers")
print("✓ No need to build tools yourself")
print("✓ Supports stdio and HTTP transports")
print("✓ Example: AWS Documentation MCP Server\n")

# ============================================================================
# BEST PRACTICES DEMONSTRATED
# ============================================================================
print("📌 BEST PRACTICES")
print("-" * 70)
print("✓ Good Names: search_documents, calculate_statistics")
print("✓ Good Docs: Clear descriptions and parameter info")
print("✓ Error Handling: Try-catch blocks, error messages")
print("✓ Parameter Validation: Check inputs before processing")
print("✓ Clear Output: Structured, easy-to-understand results\n")

# ============================================================================
# CREATE AGENT WITH ALL TOOLS
# ============================================================================
print("="*70)
print("🎯 Creating Agent with All Tools")
print("-" * 70)

system_prompt = """You are a helpful assistant with access to tools.
You can:
1. Search documents for information
2. Calculate statistics on numbers
3. Help with various tasks

Always use the appropriate tool for the task."""

agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt=system_prompt,
    tools=[search_documents, calculate_statistics]
)

print("✓ Agent created with 2 tools")
print("✓ Way 1: search_documents")
print("✓ Way 2: calculate_statistics\n")

# ============================================================================
# TEST THE TOOLS
# ============================================================================
print("="*70)
print("🎯 TEST 1: Using Way 1 Tool (@tool Decorator)")
print("-" * 70)

response1 = agent("Search for information about machine learning in the documents")
print(f"Agent: {response1}\n")

# ============================================================================
print("="*70)
print("🎯 TEST 2: Using Way 2 Tool (TOOL_SPEC)")
print("-" * 70)

response2 = agent("Calculate the average of these numbers: 10, 20, 30, 40, 50")
print(f"Agent: {response2}\n")

# ============================================================================
print("="*70)
print("🎯 TEST 3: Using Way 1 Tool Again")
print("-" * 70)

response3 = agent("Find documents about Python programming")
print(f"Agent: {response3}\n")

# ============================================================================
print("="*70)
print("🎯 TEST 4: Using Way 2 Tool with Different Operation")
print("-" * 70)

response4 = agent("What's the maximum value in this list: 5, 15, 3, 22, 8, 12")
print(f"Agent: {response4}\n")

# ============================================================================
print("="*70)
print("✅ TOOLS README DEMO COMPLETED!")
print("="*70)
print("""
What You Just Saw:

WAY 1 - @tool Decorator:
✓ Simple and quick
✓ Uses Python docstrings
✓ Automatic type validation
✓ Best for: Simple tools

WAY 2 - TOOL_SPEC Dictionary:
✓ Full control
✓ Explicit input/output format
✓ Better error handling
✓ Best for: Complex tools

WAY 3 - MCP Tools:
✓ Use external tools
✓ No need to build
✓ Connect to servers
✓ Best for: Reusing existing tools

BEST PRACTICES APPLIED:
✓ Clear tool names
✓ Detailed documentation
✓ Error handling
✓ Input validation
✓ Structured output

KEY TAKEAWAY:
Choose the tool creation method that fits your needs:
- Quick & simple? Use Way 1
- Need control? Use Way 2
- Need external tools? Use Way 3

All methods work together in ONE agent!
""")
print("="*70 + "\n")
