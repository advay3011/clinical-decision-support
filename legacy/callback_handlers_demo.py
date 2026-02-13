"""
Callback Handlers Demo - Method 2 for Processing Agent Responses

Think of callback handlers like having a personal assistant watching your agent work.
Every time something happens (model talks, tool is used, error occurs), your assistant
gets notified and can do something about it.

This is different from async iterators:
- Async iterators: YOU watch the events (you pull information)
- Callback handlers: Events notify YOU (events push information to you)

Both methods work, but callback handlers are simpler for many use cases.
"""

import asyncio
from strands import Agent, tool
from strands_tools import calculator


# ============================================================================
# EXAMPLE 1: Simple Callback Handler - Just Print What's Happening
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 1: Simple Callback Handler")
print("="*70)
print("This callback handler just prints what's happening as it happens.\n")


def simple_callback_handler(**kwargs):
    """
    A simple callback that prints events as they happen.
    
    The **kwargs contains different keys depending on what event occurred:
    - "data": Text from the model
    - "current_tool_use": Tool being used
    - "error": An error occurred
    - "result": Final result
    """
    
    # When the model generates text
    if "data" in kwargs:
        print(f"🤖 Model says: {kwargs['data']}", end="", flush=True)
    
    # When a tool is being used
    elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        tool_name = kwargs["current_tool_use"]["name"]
        print(f"\n🔧 Using tool: {tool_name}")
    
    # When there's an error
    elif "error" in kwargs:
        print(f"\n❌ Error: {kwargs['error']}")
    
    # When the agent finishes
    elif "result" in kwargs:
        print(f"\n✅ Final result: {kwargs['result']}")


# Create agent WITH callback handler
agent_with_callback = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[calculator],
    callback_handler=simple_callback_handler
)

print("Running: 'Calculate 2+2'\n")
result = agent_with_callback("Calculate 2+2")
print("\n")


# ============================================================================
# EXAMPLE 2: Advanced Callback Handler - Track Everything
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 2: Advanced Callback Handler - Track Everything")
print("="*70)
print("This callback handler tracks all events and builds a summary.\n")


class EventTracker:
    """A callback handler that tracks all events during agent execution."""
    
    def __init__(self):
        self.events = []
        self.tool_calls = []
        self.model_output = ""
        self.errors = []
    
    def __call__(self, **kwargs):
        """Called every time an event happens."""
        
        # Track all events
        self.events.append(kwargs)
        
        # Track model output
        if "data" in kwargs:
            self.model_output += kwargs["data"]
            print(f"📝 Model output chunk: {kwargs['data'][:30]}...")
        
        # Track tool usage
        elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
            tool_info = {
                "name": kwargs["current_tool_use"]["name"],
                "input": kwargs["current_tool_use"].get("input", {})
            }
            self.tool_calls.append(tool_info)
            print(f"🔧 Tool called: {tool_info['name']} with input: {tool_info['input']}")
        
        # Track errors
        elif "error" in kwargs:
            self.errors.append(kwargs["error"])
            print(f"⚠️ Error occurred: {kwargs['error']}")
        
        # Track completion
        elif "result" in kwargs:
            print(f"✅ Agent completed")
    
    def print_summary(self):
        """Print a summary of what happened."""
        print("\n" + "-"*70)
        print("EXECUTION SUMMARY")
        print("-"*70)
        print(f"Total events: {len(self.events)}")
        print(f"Tool calls: {len(self.tool_calls)}")
        print(f"Errors: {len(self.errors)}")
        print(f"Model output length: {len(self.model_output)} characters")
        
        if self.tool_calls:
            print("\nTools used:")
            for tool_call in self.tool_calls:
                print(f"  - {tool_call['name']}: {tool_call['input']}")
        
        if self.errors:
            print("\nErrors encountered:")
            for error in self.errors:
                print(f"  - {error}")


# Create tracker and agent
tracker = EventTracker()
agent_with_tracker = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[calculator],
    callback_handler=tracker
)

print("Running: 'What is 100 + 50 - 25?'\n")
result = agent_with_tracker("What is 100 + 50 - 25?")
tracker.print_summary()


# ============================================================================
# EXAMPLE 3: Callback Handler for Logging - Save Everything to a File
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 3: Callback Handler for Logging")
print("="*70)
print("This callback handler saves all events to a log file.\n")


class LoggingCallback:
    """A callback handler that logs all events to a file."""
    
    def __init__(self, filename="agent_log.txt"):
        self.filename = filename
        self.log_file = open(filename, "w")
        self.event_count = 0
    
    def __call__(self, **kwargs):
        """Called every time an event happens."""
        self.event_count += 1
        
        # Log the event
        self.log_file.write(f"\n--- Event {self.event_count} ---\n")
        
        if "data" in kwargs:
            self.log_file.write(f"Type: Model Output\n")
            self.log_file.write(f"Content: {kwargs['data']}\n")
            print(f"📝 Logged model output")
        
        elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
            self.log_file.write(f"Type: Tool Use\n")
            self.log_file.write(f"Tool: {kwargs['current_tool_use']['name']}\n")
            self.log_file.write(f"Input: {kwargs['current_tool_use'].get('input', {})}\n")
            print(f"🔧 Logged tool use")
        
        elif "result" in kwargs:
            self.log_file.write(f"Type: Result\n")
            self.log_file.write(f"Result: {kwargs['result']}\n")
            print(f"✅ Logged final result")
        
        self.log_file.flush()
    
    def close(self):
        """Close the log file."""
        self.log_file.close()
        print(f"\n📄 Log saved to {self.filename}")


# Create logger and agent
logger = LoggingCallback("agent_execution.log")
agent_with_logging = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[calculator],
    callback_handler=logger
)

print("Running: 'Calculate 15 * 3'\n")
result = agent_with_logging("Calculate 15 * 3")
logger.close()


# ============================================================================
# EXAMPLE 4: Comparing Callback Handlers vs Async Iterators
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 4: Callback Handlers vs Async Iterators")
print("="*70)
print("""
CALLBACK HANDLERS:
✅ Simpler to use - just define a function
✅ Good for logging and monitoring
✅ Good for real-time notifications
❌ Less control over the flow
❌ Can't easily stop the agent mid-execution

ASYNC ITERATORS:
✅ More control - you decide what to do with each event
✅ Can stop the agent mid-execution
✅ Good for complex processing
❌ More code to write
❌ Requires async/await knowledge

WHEN TO USE EACH:
- Use callback handlers for: logging, monitoring, notifications, simple tracking
- Use async iterators for: complex processing, conditional stopping, web streaming
""")


# ============================================================================
# EXAMPLE 5: Multiple Callback Handlers (Advanced)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 5: Combining Multiple Callbacks")
print("="*70)
print("You can create a callback that does multiple things at once.\n")


def multi_purpose_callback(**kwargs):
    """A callback that does multiple things."""
    
    # Purpose 1: Print to console
    if "data" in kwargs:
        print(f"[CONSOLE] {kwargs['data']}", end="", flush=True)
    
    # Purpose 2: Count events
    if not hasattr(multi_purpose_callback, 'event_count'):
        multi_purpose_callback.event_count = 0
    multi_purpose_callback.event_count += 1
    
    # Purpose 3: Track tool usage
    if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        if not hasattr(multi_purpose_callback, 'tools_used'):
            multi_purpose_callback.tools_used = []
        multi_purpose_callback.tools_used.append(kwargs["current_tool_use"]["name"])
        print(f"\n[TOOL] {kwargs['current_tool_use']['name']}")


agent_multi = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[calculator],
    callback_handler=multi_purpose_callback
)

print("Running: 'Add 10 and 20, then multiply by 2'\n")
result = agent_multi("Add 10 and 20, then multiply by 2")

print(f"\n\n[STATS] Total events: {multi_purpose_callback.event_count}")
print(f"[STATS] Tools used: {multi_purpose_callback.tools_used}")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================
print("\n" + "="*70)
print("KEY TAKEAWAYS")
print("="*70)
print("""
1. CALLBACK HANDLERS are functions that get called when events happen
2. They receive **kwargs with different keys depending on the event type
3. Common event types: "data" (model output), "current_tool_use" (tool usage)
4. Use them for: logging, monitoring, notifications, simple tracking
5. They're simpler than async iterators but less flexible

CALLBACK HANDLER PATTERN:
    def my_callback(**kwargs):
        if "data" in kwargs:
            # Handle model output
        elif "current_tool_use" in kwargs:
            # Handle tool usage
        elif "result" in kwargs:
            # Handle completion
    
    agent = Agent(tools=[...], callback_handler=my_callback)
    agent("your prompt")
""")
