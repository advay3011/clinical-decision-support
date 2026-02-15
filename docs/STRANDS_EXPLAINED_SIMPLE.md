# Strands Explained Simply

A beginner-friendly explanation of how Strands works.

## What is Strands?

Think of Strands as a **smart assistant framework**. It lets you:
- Create an AI agent
- Give it tools to use
- Let it decide which tools to use
- Have natural conversations

## The Simple Version

```
You: "My blood pressure is 160 over 90"
     ↓
Agent: "I should use the assess_vitals tool"
     ↓
Tool: assess_vitals(160, 90, 85)
     ↓
Result: "This is Stage 2 hypertension"
     ↓
Agent: "That's elevated. Let me ask you..."
     ↓
You: See friendly response
```

## The Three Main Parts

### 1. System Prompt

This is the **instructions** for the agent. It tells the agent:
- Who it is ("You are a friendly clinical assistant")
- How to behave ("Ask one question at a time")
- What to do ("Always recommend seeing a real doctor")

```python
system_prompt = """
You are a friendly clinical assistant.
You talk in simple, plain English.
You ask one question at a time.
You always remind patients to see a real doctor.
"""
```

### 2. Tools

These are **functions** the agent can use. Examples:

```python
@tool
def assess_vitals(systolic, diastolic, heart_rate):
    """Check if vitals are normal"""
    # Returns assessment
    
@tool
def check_symptoms(symptoms):
    """Check what conditions match these symptoms"""
    # Returns possible conditions
    
@tool
def check_drug_interaction(drugs):
    """Check if drugs interact"""
    # Returns interaction info
```

### 3. LLM (Claude)

This is the **brain**. It:
- Reads the system prompt
- Sees the available tools
- Analyzes what the user said
- Decides which tools to use
- Generates a response

## How It Works Step-by-Step

### Step 1: User Sends Message

```
User: "I have a headache and I'm tired"
```

### Step 2: Agent Receives It

The agent gets:
- The user message
- The system prompt (instructions)
- The list of available tools

### Step 3: LLM Analyzes

Claude (the LLM) thinks:
- "The user is reporting symptoms"
- "I should use the check_symptoms tool"
- "I need to extract: headache, fatigue"

### Step 4: Tool Executes

```python
check_symptoms(["headache", "fatigue"])
# Returns: [
#   {"condition": "tension headache", "relevance": 2},
#   {"condition": "migraine", "relevance": 2},
#   {"condition": "dehydration", "relevance": 2}
# ]
```

### Step 5: Agent Generates Response

Claude uses the tool result to write:
```
"Those symptoms could be from a few things. 
Let me ask - how long have you had these?"
```

### Step 6: User Sees Response

The response appears word-by-word in the chat.

## Real Example: Drug Interaction Check

```
User: "I take aspirin and ibuprofen together"

Agent thinks:
├─ This is about medications
├─ I should check for interactions
└─ I'll use check_drug_interaction()

Tool executes:
├─ Looks up aspirin
├─ Looks up ibuprofen
└─ Checks if they interact

Result:
├─ Severity: HIGH
└─ Risk: Increased bleeding

Agent responds:
"Taking aspirin and ibuprofen together increases 
bleeding risk. You should pick one or the other. 
Have you talked to your doctor about this?"
```

## The Tools in Our Chatbot

| Tool | What It Does | Example |
|------|-------------|---------|
| `assess_vitals()` | Checks BP and heart rate | "Your BP is elevated" |
| `check_symptoms()` | Finds possible conditions | "Could be a migraine" |
| `check_drug_interaction()` | Checks if drugs interact | "These don't interact" |
| `get_treatment_guidelines()` | Gives advice for conditions | "Cut back on salt" |
| `summarize_patient_session()` | Creates a health report | "Here's what we discussed" |
| `search_medical_knowledge()` | Searches medical info | "Metformin is for diabetes" |
| `get_real_drug_info()` | Gets real drug data from NIH | "Aspirin is a pain reliever" |
| `check_real_drug_interactions()` | Gets real interactions from NIH | "HIGH severity interaction" |
| `get_drug_adverse_events()` | Gets real side effects from FDA | "32,886 fatigue reports" |

## Why This is Cool

### 1. Automatic Tool Selection
You don't tell the agent which tool to use. It figures it out!

```
User: "My BP is 160/90"
Agent: "I'll use assess_vitals()"  ← Automatic!

User: "I have a headache"
Agent: "I'll use check_symptoms()"  ← Automatic!
```

### 2. Natural Conversation
The agent talks like a real person, not a robot.

```
❌ Bad: "BLOOD PRESSURE STATUS: ELEVATED. RECOMMENDATION: REDUCE SODIUM."
✅ Good: "That's a little on the high side. Have you tried cutting back on salt?"
```

### 3. Real Medical Data
The agent uses real data from trusted sources:
- NIH (RxNorm) for drug info
- FDA (OpenFDA) for adverse events
- Not just made-up information

### 4. Context Aware
The agent remembers patient info:
- Name, age, gender
- Previous messages
- What was already discussed

## The Flow Diagram

```
┌──────────────────┐
│  User Message    │
│ "My BP is 160/90"│
└────────┬─────────┘
         │
         ↓
┌──────────────────────────────────┐
│  Strands Agent                   │
│  ┌────────────────────────────┐  │
│  │ System Prompt              │  │
│  │ "You are friendly..."      │  │
│  └────────────────────────────┘  │
│  ┌────────────────────────────┐  │
│  │ LLM (Claude)               │  │
│  │ Analyzes message           │  │
│  │ Decides: use assess_vitals │  │
│  └────────────────────────────┘  │
│  ┌────────────────────────────┐  │
│  │ Tools                      │  │
│  │ assess_vitals(160, 90, 85) │  │
│  └────────────────────────────┘  │
└────────┬─────────────────────────┘
         │
         ↓
┌──────────────────────────────────┐
│  Tool Result                     │
│ "Stage 2 hypertension"           │
└────────┬─────────────────────────┘
         │
         ↓
┌──────────────────────────────────┐
│  Agent Response                  │
│ "That's elevated. Let me ask..." │
└────────┬─────────────────────────┘
         │
         ↓
┌──────────────────┐
│  User Sees It    │
│  In Chat         │
└──────────────────┘
```

## Key Concepts

### System Prompt
- **What it is**: Instructions for the agent
- **Why it matters**: Controls personality and behavior
- **Example**: "Be friendly, ask one question at a time"

### Tools
- **What they are**: Functions the agent can call
- **Why they matter**: Give the agent superpowers
- **Example**: `assess_vitals()` lets it evaluate blood pressure

### LLM (Claude)
- **What it is**: The AI brain
- **Why it matters**: Makes decisions and generates responses
- **Example**: Decides to use `assess_vitals()` when user mentions BP

### Session State
- **What it is**: Memory for the conversation
- **Why it matters**: Remembers patient info and chat history
- **Example**: Remembers patient is "John, age 35, male"

## How to Use It

### 1. Run the App
```bash
streamlit run streamlit_app.py
```

### 2. Register a Patient
- Enter name, DOB, gender
- Click "Register Patient"

### 3. Chat Naturally
- "My blood pressure is 160/90"
- "I have a headache"
- "What should I do?"

### 4. Watch the Magic
- Agent automatically uses the right tools
- Gives personalized responses
- Uses real medical data

## Common Questions

### Q: How does the agent know which tool to use?
**A:** The LLM (Claude) reads the system prompt and available tools, then decides based on what the user said.

### Q: Can I add new tools?
**A:** Yes! Just define a new function with `@tool` decorator and add it to the agent.

### Q: Is the data real?
**A:** Yes! We use real APIs from NIH (RxNorm) and FDA (OpenFDA).

### Q: Can it replace a real doctor?
**A:** No! It's a clinical assistant. We always remind users to see a real doctor.

### Q: How does it remember patient info?
**A:** We store it in Streamlit's session state and add it to every message.

## Summary

**Strands is simple:**
1. You give it a system prompt (instructions)
2. You give it tools (functions)
3. User sends a message
4. Agent decides which tools to use
5. Tools execute and return data
6. Agent generates a response
7. User sees the answer

**That's it!** The magic is that the agent automatically figures out what to do. 🎉

---

**Ready to understand the code?** Check out `CLINICAL_DECISION_SUPPORT_COMPLETE_GUIDE.md` for the full technical explanation!
