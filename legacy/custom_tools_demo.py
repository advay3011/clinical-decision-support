"""Custom Tools Demo - All 3 Ways to Create Tools
Demonstrates Way 1, Way 2, and Way 3 of creating custom tools
"""

import logging
import json
from strands import Agent, tool
from strands.types.tools import ToolResult, ToolUse
from typing import Any

# Configure logging
logging.getLogger("strands").setLevel(logging.INFO)

print("\n" + "="*70)
print("🛠️  CUSTOM TOOLS DEMO - All 3 Ways")
print("="*70)

# ============================================================================
# WAY 1: Simple Decorator (In Same File)
# ============================================================================
print("\n📌 WAY 1: Simple Decorator (In Same File)")
print("-" * 70)
print("Define tool with @tool decorator in SAME file as agent\n")

# Simulating a database
appointments_db = {}

@tool
def create_appointment(date: str, location: str, title: str, description: str) -> str:
    """Create a new appointment in the database
    
    Args:
        date: Date and time (YYYY-MM-DD HH:MM)
        location: Where the appointment is
        title: What the appointment is about
        description: Details about the appointment
    
    Returns:
        Confirmation with appointment ID
    """
    import uuid
    appointment_id = str(uuid.uuid4())[:8]
    
    appointments_db[appointment_id] = {
        "id": appointment_id,
        "date": date,
        "location": location,
        "title": title,
        "description": description
    }
    
    return f"✓ Appointment created! ID: {appointment_id}"

print("✓ Tool created with @tool decorator")
print("✓ Defined in SAME file as agent")
print("✓ Simple and quick!\n")

# ============================================================================
# WAY 2: Standalone File with Decorator (Simulated)
# ============================================================================
print("📌 WAY 2: Standalone File with Decorator")
print("-" * 70)
print("Define tool in SEPARATE file, then import it\n")

# Simulating a separate file: list_appointments.py
@tool
def list_appointments() -> str:
    """List all appointments from the database
    
    Returns:
        JSON string of all appointments
    """
    if not appointments_db:
        return "No appointments found"
    
    return json.dumps(list(appointments_db.values()), indent=2)

print("✓ Tool defined in separate function (simulating separate file)")
print("✓ Can be imported into multiple agents")
print("✓ Organized and reusable!\n")

# ============================================================================
# WAY 3: TOOL_SPEC (Most Control)
# ============================================================================
print("📌 WAY 3: TOOL_SPEC (Most Control)")
print("-" * 70)
print("Define tool with TOOL_SPEC dictionary for full control\n")

# Simulating a separate file: update_appointment.py
TOOL_SPEC = {
    "name": "update_appointment",
    "description": "Update an existing appointment",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "appointment_id": {
                    "type": "string",
                    "description": "The ID of the appointment to update"
                },
                "date": {
                    "type": "string",
                    "description": "New date (YYYY-MM-DD HH:MM)"
                },
                "location": {
                    "type": "string",
                    "description": "New location"
                },
                "title": {
                    "type": "string",
                    "description": "New title"
                }
            },
            "required": ["appointment_id"]  # Only ID is required
        }
    }
}

def update_appointment(tool: ToolUse, **kwargs: Any) -> ToolResult:
    """Update appointment in database"""
    
    tool_use_id = tool["toolUseId"]
    appointment_id = tool["input"]["appointment_id"]
    
    # Check if appointment exists
    if appointment_id not in appointments_db:
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": f"Appointment {appointment_id} not found"}]
        }
    
    # Update fields if provided
    if "date" in tool["input"]:
        appointments_db[appointment_id]["date"] = tool["input"]["date"]
    if "location" in tool["input"]:
        appointments_db[appointment_id]["location"] = tool["input"]["location"]
    if "title" in tool["input"]:
        appointments_db[appointment_id]["title"] = tool["input"]["title"]
    
    return {
        "toolUseId": tool_use_id,
        "status": "success",
        "content": [{"text": f"✓ Appointment {appointment_id} updated successfully"}]
    }

print("✓ Tool defined with TOOL_SPEC dictionary")
print("✓ Full control over inputs and outputs")
print("✓ Professional and detailed!\n")

# ============================================================================
# CREATE AGENT WITH ALL 3 TOOLS
# ============================================================================
print("="*70)
print("🎯 Creating Agent with All 3 Tools")
print("-" * 70)

system_prompt = """You are a helpful personal assistant that manages appointments.
You can:
1. Create new appointments (Way 1 tool)
2. List all appointments (Way 2 tool)
3. Update existing appointments (Way 3 tool)

Always provide appointment IDs when creating or updating."""

agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    system_prompt=system_prompt,
    tools=[create_appointment, list_appointments, update_appointment]
)

print("✓ Agent created with all 3 tools")
print("✓ Way 1: create_appointment")
print("✓ Way 2: list_appointments")
print("✓ Way 3: update_appointment\n")

# ============================================================================
# TEST THE TOOLS
# ============================================================================
print("="*70)
print("🎯 TEST 1: Create Appointment (Using Way 1 Tool)")
print("-" * 70)

response1 = agent("Create an appointment for tomorrow at 2pm in NYC. Title: Team Meeting. Description: Discuss Q1 goals")
print(f"Agent: {response1}\n")

# ============================================================================
print("="*70)
print("🎯 TEST 2: List Appointments (Using Way 2 Tool)")
print("-" * 70)

response2 = agent("Show me all my appointments")
print(f"Agent: {response2}\n")

# ============================================================================
print("="*70)
print("🎯 TEST 3: Create Another Appointment")
print("-" * 70)

response3 = agent("Add another appointment for next week at 10am in Boston. Title: Client Call. Description: Quarterly review")
print(f"Agent: {response3}\n")

# ============================================================================
print("="*70)
print("🎯 TEST 4: Update Appointment (Using Way 3 Tool)")
print("-" * 70)

response4 = agent("Actually, the Team Meeting location should be changed to San Francisco instead of NYC")
print(f"Agent: {response4}\n")

# ============================================================================
print("="*70)
print("🎯 TEST 5: List Updated Appointments")
print("-" * 70)

response5 = agent("Show me all appointments again")
print(f"Agent: {response5}\n")

# ============================================================================
print("="*70)
print("✅ CUSTOM TOOLS DEMO COMPLETED!")
print("="*70)
print("""
What You Just Saw:

WAY 1 - Simple Decorator:
✓ Used @tool decorator
✓ Defined in same file
✓ Quick and easy
✓ Used for: create_appointment

WAY 2 - Standalone File:
✓ Defined in separate function
✓ Can be reused
✓ Organized code
✓ Used for: list_appointments

WAY 3 - TOOL_SPEC:
✓ Full control with dictionary
✓ Specify required fields
✓ Professional format
✓ Used for: update_appointment

Key Takeaways:
- Way 1: Best for simple, quick tools
- Way 2: Best for organized, reusable code
- Way 3: Best for complex tools with specific requirements

All 3 ways work together in ONE agent!
The agent automatically decides which tool to use based on your request.
""")
print("="*70 + "\n")
