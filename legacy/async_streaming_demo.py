"""Async Streaming Demo - Watch Agent Events in Real-Time
Demonstrates how to use async iterators to stream agent responses
"""

import asyncio
import logging
from strands import Agent
from strands_tools import calculator

# Configure logging
logging.getLogger("strands").setLevel(logging.INFO)

print("\n" + "="*70)
print("⚡ ASYNC STREAMING DEMO - Watch Agent Events in Real-Time")
print("="*70)

# ============================================================================
# BASIC STREAMING EXAMPLE
# ============================================================================
print("\n📌 BASIC STREAMING: Watch Each Event")
print("-" * 70)
print("Running: agent.stream_async('Calculate 2+2')\n")

async def process_streaming_response():
    """Watch each event as it happens"""
    agent = Agent(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        tools=[calculator],
        callback_handler=None
    )
    
    agent_stream = agent.stream_async("Calculate 2+2")
    event_count = 0
    
    async for event in agent_stream:  # Watch each event
        event_count += 1
        print(f"\n📬 Event #{event_count}:")
        print(f"   Keys: {list(event.keys())}")
        
        # Show relevant data
        if "data" in event:
            print(f"   📝 Text: {event['data'][:50]}..." if len(event['data']) > 50 else f"   📝 Text: {event['data']}")
        if "current_tool_use" in event and event["current_tool_use"]:
            print(f"   🔧 Tool: {event['current_tool_use'].get('name')}")
        if "result" in event:
            print(f"   ✅ Result: {event['result'][:50]}..." if len(str(event['result'])) > 50 else f"   ✅ Result: {event['result']}")

# Run the async function
asyncio.run(process_streaming_response())

# ============================================================================
# ADVANCED STREAMING WITH EVENT TRACKING
# ============================================================================
print("\n\n" + "="*70)
print("📌 ADVANCED STREAMING: Track Event Lifecycle")
print("-" * 70)
print("Running: agent.stream_async('What is 42+7?')\n")

async def track_event_lifecycle():
    """Track the lifecycle of events"""
    agent = Agent(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        tools=[calculator],
        callback_handler=None
    )
    
    agent_stream = agent.stream_async("What is 42+7?")
    
    async for event in agent_stream:
        # Track event loop lifecycle
        if event.get("init_event_loop", False):
            print("🔄 Event loop initialized")
        elif event.get("start_event_loop", False):
            print("▶️  Event loop cycle starting")
        elif event.get("start", False):
            print("📝 New cycle started")
        elif "message" in event:
            print(f"📬 New message created: {event['message']['role']}")
        elif event.get("force_stop", False):
            print(f"🛑 Event loop force-stopped: {event.get('force_stop_reason', 'unknown reason')}")
        
        # Track tool usage
        if "current_tool_use" in event and event["current_tool_use"].get("name"):
            tool_name = event["current_tool_use"]["name"]
            print(f"🔧 Using tool: {tool_name}")
        
        # Show text snippets
        if "data" in event:
            data_snippet = event["data"][:30] + ("..." if len(event["data"]) > 30 else "")
            print(f"📟 Text: {data_snippet}")

# Run the async function
asyncio.run(track_event_lifecycle())

# ============================================================================
# STREAMING WITH CUSTOM PROCESSING
# ============================================================================
print("\n\n" + "="*70)
print("📌 STREAMING WITH CUSTOM PROCESSING")
print("-" * 70)
print("Running: agent.stream_async('Calculate 100 + 50')\n")

async def process_with_custom_logic():
    """Process events with custom logic"""
    agent = Agent(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        tools=[calculator],
        callback_handler=None
    )
    
    agent_stream = agent.stream_async("Calculate 100 + 50")
    
    full_response = ""
    tools_used = []
    
    async for event in agent_stream:
        # Collect text
        if "data" in event:
            full_response += event["data"]
        
        # Track tools
        if "current_tool_use" in event and event["current_tool_use"]:
            tool_name = event["current_tool_use"].get("name")
            if tool_name and tool_name not in tools_used:
                tools_used.append(tool_name)
                print(f"🔧 Tool used: {tool_name}")
    
    print(f"\n✅ Final Response: {full_response}")
    print(f"📊 Tools used: {tools_used}")

# Run the async function
asyncio.run(process_with_custom_logic())

# ============================================================================
# STREAMING MULTIPLE QUESTIONS
# ============================================================================
print("\n\n" + "="*70)
print("📌 STREAMING MULTIPLE QUESTIONS")
print("-" * 70)

async def stream_multiple_questions():
    """Stream multiple questions sequentially"""
    agent = Agent(
        model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        tools=[calculator],
        callback_handler=None
    )
    
    questions = [
        "What is 5 + 3?",
        "Calculate 20 * 4",
        "What is 100 - 25?"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        print("-" * 40)
        
        agent_stream = agent.stream_async(question)
        response_text = ""
        
        async for event in agent_stream:
            if "data" in event:
                response_text += event["data"]
        
        print(f"✅ Answer: {response_text}")

# Run the async function
asyncio.run(stream_multiple_questions())

# ============================================================================
# SUMMARY
# ============================================================================
print("\n\n" + "="*70)
print("✅ ASYNC STREAMING DEMO COMPLETED!")
print("="*70)
print("""
What You Just Saw:

1. BASIC STREAMING:
   ✓ Watched each event as it happened
   ✓ Printed event keys and data
   ✓ Tracked tool usage

2. EVENT LIFECYCLE TRACKING:
   ✓ Tracked when event loop starts/stops
   ✓ Tracked message creation
   ✓ Tracked tool usage
   ✓ Tracked text generation

3. CUSTOM PROCESSING:
   ✓ Collected full response
   ✓ Tracked tools used
   ✓ Processed events with custom logic

4. MULTIPLE QUESTIONS:
   ✓ Streamed multiple questions
   ✓ Collected responses
   ✓ Processed each one

KEY CONCEPTS:

Async Iterator Pattern:
  async for event in agent.stream_async(prompt):
      # Process each event in real-time

Benefits:
  ✓ Real-time monitoring
  ✓ Custom processing
  ✓ Live dashboards
  ✓ Streaming APIs
  ✓ Progress tracking

Use Cases:
  ✓ FastAPI streaming endpoints
  ✓ WebSocket connections
  ✓ Real-time chat applications
  ✓ Live monitoring dashboards
  ✓ Event-driven systems
""")
print("="*70 + "\n")
