# Clinical Decision Support Chatbot - Complete Technical Guide

A comprehensive guide to understanding how the Clinical Decision Support chatbot works, including the Strands SDK, tools, and the entire architecture.

## 📚 Table of Contents

1. [What is Strands?](#what-is-strands)
2. [How the Chatbot Works](#how-the-chatbot-works)
3. [Tools Explained](#tools-explained)
4. [The Agent Process](#the-agent-process)
5. [Architecture](#architecture)
6. [Real Medical Data Integration](#real-medical-data-integration)
7. [Patient Registration](#patient-registration)
8. [Conversation Flow](#conversation-flow)
9. [Code Examples](#code-examples)

---

## What is Strands?

### Overview

**Strands** is an AI agent framework that lets you build intelligent agents with tools. It's built on top of LLMs (Large Language Models) like Claude.

### Key Concepts

```
┌─────────────────────────────────────────────────────────┐
│                    STRANDS AGENT                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         System Prompt (Instructions)             │  │
│  │  "You are a friendly clinical assistant..."      │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↓                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │         LLM (Claude 3.5 Sonnet)                  │  │
│  │  Reads prompt + tools, decides what to do        │  │
│  └──────────────────────────────────────────────────┘  │
│                          ↓                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Available Tools                     │  │
│  │  • assess_vitals()                               │  │
│  │  • check_symptoms()                              │  │
│  │  • check_drug_interaction()                      │  │
│  │  • get_treatment_guidelines()                    │  │
│  │  • summarize_patient_session()                   │  │
│  │  • search_medical_knowledge()                    │  │
│  │  • get_real_drug_info()                          │  │
│  │  • check_real_drug_interactions()                │  │
│  │  • get_drug_adverse_events()                     │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### How Strands Works

1. **User sends message** → "my blood pressure is 160 over 90"
2. **Agent reads message** → Understands it's about vitals
3. **Agent decides** → "I should use assess_vitals() tool"
4. **Tool executes** → Returns BP assessment
5. **Agent responds** → "That's elevated, let me ask..."
6. **User sees response** → Friendly, conversational reply

---

## How the Chatbot Works

### High-Level Flow

```
User Input
    ↓
Streamlit UI
    ↓
Patient Context Added
    ↓
Strands Agent
    ├─ Reads system prompt
    ├─ Analyzes user message
    ├─ Decides which tools to use
    ├─ Executes tools
    └─ Generates response
    ↓
Response Streamed to UI
    ↓
User Sees Answer
```

### Step-by-Step Example

**User:** "I'm taking aspirin and ibuprofen together"

**Step 1: Agent Receives Message**
```
Message: "I'm taking aspirin and ibuprofen together"
Patient Context: Name: John, Age: 35, Gender: Male
```

**Step 2: Agent Analyzes**
- Recognizes this is about drug interactions
- Decides to use `check_real_drug_interactions()` tool

**Step 3: Tool Executes**
```python
check_real_drug_interactions(["aspirin", "ibuprofen"])
# Returns: {
#   "safe": False,
#   "interactions": [
#     {
#       "drugs": ["aspirin", "ibuprofen"],
#       "severity": "high",
#       "description": "Increased bleeding risk..."
#     }
#   ]
# }
```

**Step 4: Agent Generates Response**
- Uses tool result to craft response
- Personalizes with patient context
- Adds follow-up question

**Step 5: Response Streamed**
- Words appear one by one
- User sees real-time response

---

## Tools Explained

### 1. assess_vitals()

**Purpose:** Evaluate blood pressure and heart rate

**Input:**
```python
systolic: int      # Top number (e.g., 160)
diastolic: int     # Bottom number (e.g., 90)
heart_rate: int    # Beats per minute (e.g., 85)
```

**Output:**
```python
{
    "bp_status": "stage2_hypertension",  # normal, elevated, stage1, stage2
    "hr_status": "normal",                # low, normal, elevated
    "flags": [                            # Warnings
        "Stage 2 hypertension - medical attention recommended"
    ]
}
```

**Example:**
```
User: "my blood pressure is 160 over 90 and heart rate is 85"
Tool: assess_vitals(160, 90, 85)
Result: BP is Stage 2 hypertension, HR is normal
Agent: "Your BP is elevated, but your heart rate is good..."
```

### 2. check_symptoms()

**Purpose:** Cross-reference symptoms with possible conditions

**Input:**
```python
symptoms: list[str]  # ["headache", "fatigue", "dizziness"]
```

**Output:**
```python
{
    "symptoms_checked": ["headache", "fatigue"],
    "possible_conditions": [
        {"condition": "tension headache", "relevance": 2},
        {"condition": "migraine", "relevance": 2},
        {"condition": "dehydration", "relevance": 2}
    ]
}
```

**Example:**
```
User: "I have a headache and fatigue"
Tool: check_symptoms(["headache", "fatigue"])
Result: Possible conditions ranked by likelihood
Agent: "These could be from several things. Let me ask..."
```

### 3. check_drug_interaction()

**Purpose:** Check for dangerous drug interactions

**Input:**
```python
drugs: list[str]  # ["aspirin", "warfarin"]
```

**Output:**
```python
{
    "safe": False,
    "interactions": [
        {
            "drugs": ["aspirin", "warfarin"],
            "severity": "high",
            "note": "Increased bleeding risk"
        }
    ]
}
```

**Example:**
```
User: "I take aspirin and warfarin"
Tool: check_drug_interaction(["aspirin", "warfarin"])
Result: HIGH severity interaction found
Agent: "These two together increase bleeding risk. Talk to your doctor."
```

### 4. get_treatment_guidelines()

**Purpose:** Get plain English treatment advice for conditions

**Input:**
```python
condition: str  # "high blood pressure"
```

**Output:**
```python
{
    "condition": "High Blood Pressure (Hypertension)",
    "simple_explanation": "Your heart is working harder...",
    "lifestyle_changes": [
        "Cut back on salt",
        "Drink more water",
        "Move your body"
    ],
    "when_to_see_doctor": "If readings stay above 140/90..."
}
```

**Example:**
```
User: "What should I do about my high blood pressure?"
Tool: get_treatment_guidelines("high blood pressure")
Result: Practical lifestyle advice
Agent: "Here are simple things that help..."
```

### 5. summarize_patient_session()

**Purpose:** Create a clean health report from conversation

**Input:**
```python
notes: str  # Everything discussed in the conversation
```

**Output:**
```python
{
    "session_date": "2024-02-13T...",
    "session_summary": "Patient reported elevated BP...",
    "next_steps": [
        "Follow up with primary care doctor",
        "Monitor symptoms",
        "Keep track of vital signs"
    ]
}
```

**Example:**
```
User: "Can you summarize what we talked about?"
Tool: summarize_patient_session("Patient reported BP 160/90...")
Result: Clean summary with next steps
Agent: "Here's what we discussed today..."
```

### 6. search_medical_knowledge()

**Purpose:** Search medical knowledge base

**Input:**
```python
query: str  # "what is lisinopril"
```

**Output:**
```python
{
    "query": "what is lisinopril",
    "result": "A blood pressure medication (ACE inhibitor)...",
    "source": "Clinical knowledge base"
}
```

**Example:**
```
User: "What is metformin?"
Tool: search_medical_knowledge("metformin")
Result: Plain English explanation
Agent: "Metformin is a diabetes medication that..."
```

### 7. get_real_drug_info()

**Purpose:** Get real drug information from RxNorm API (NIH)

**Input:**
```python
drug_name: str  # "aspirin"
```

**Output:**
```python
{
    "name": "Aspirin",
    "rxcui": "7682",
    "found": True,
    "source": "RxNorm (NIH)"
}
```

**Example:**
```
User: "Tell me about aspirin"
Tool: get_real_drug_info("aspirin")
Result: Real drug data from NIH
Agent: "Aspirin is a common pain reliever..."
```

### 8. check_real_drug_interactions()

**Purpose:** Check real drug interactions from RxNorm API

**Input:**
```python
drug_names: list[str]  # ["aspirin", "warfarin"]
```

**Output:**
```python
{
    "safe": False,
    "interactions": [
        {
            "drugs": ["aspirin", "warfarin"],
            "severity": "high",
            "description": "Increased bleeding risk..."
        }
    ],
    "source": "RxNorm (NIH)"
}
```

**Example:**
```
User: "Is aspirin safe with warfarin?"
Tool: check_real_drug_interactions(["aspirin", "warfarin"])
Result: Real interaction data from NIH
Agent: "These have a HIGH severity interaction..."
```

### 9. get_drug_adverse_events()

**Purpose:** Get real adverse events from OpenFDA API

**Input:**
```python
drug_name: str  # "aspirin"
```

**Output:**
```python
{
    "drug": "aspirin",
    "adverse_events": [
        {"reaction": "FATIGUE", "count": 32886},
        {"reaction": "NAUSEA", "count": 27987}
    ],
    "source": "OpenFDA"
}
```

**Example:**
```
User: "What are the side effects of aspirin?"
Tool: get_drug_adverse_events("aspirin")
Result: Real adverse events from FDA database
Agent: "The most reported side effects are fatigue (32,886 reports)..."
```

---

## The Agent Process

### How Strands Decides What to Do

```
┌─────────────────────────────────────────────────────────┐
│ 1. USER MESSAGE ARRIVES                                 │
│    "my blood pressure is 160 over 90"                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. AGENT READS SYSTEM PROMPT                            │
│    "You are a friendly clinical assistant..."           │
│    "You have these tools available: ..."                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. LLM ANALYZES                                         │
│    • Understands user is reporting vitals               │
│    • Recognizes need for assess_vitals() tool           │
│    • Extracts: systolic=160, diastolic=90               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. TOOL EXECUTION                                       │
│    assess_vitals(160, 90, 85)                           │
│    Returns: {"bp_status": "stage2_hypertension", ...}   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. RESPONSE GENERATION                                  │
│    • Uses tool result                                   │
│    • Adds patient context                               │
│    • Generates friendly response                        │
│    • Adds follow-up question                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 6. RESPONSE STREAMED                                    │
│    "That's a little on the high side..."                │
│    (Words appear one by one)                            │
└─────────────────────────────────────────────────────────┘
```

### Tool Selection Logic

The LLM decides which tools to use based on:

1. **User Intent** - What is the user asking?
2. **Available Tools** - Which tools can help?
3. **Context** - What do we already know?
4. **System Prompt** - What are we instructed to do?

**Examples:**

| User Says | Intent | Tool Used |
|-----------|--------|-----------|
| "my BP is 160/90" | Report vitals | assess_vitals() |
| "I have a headache" | Report symptom | check_symptoms() |
| "I take aspirin and ibuprofen" | Check interaction | check_drug_interaction() |
| "What should I do?" | Get advice | get_treatment_guidelines() |
| "Summarize our chat" | Create report | summarize_patient_session() |

---

## Architecture

### File Structure

```
streamlit_app.py                          # Main Streamlit app
├── Page config
├── Session state initialization
├── Patient registration form
├── Chat interface
└── Message handling

agents/
├── clinical_decision_support_agent.py    # CLI version
├── clinical_decision_support_streamlit.py # Streamlit version
├── clinical_decision_support_enhanced.py  # With real medical data
└── test_real_medical_data.py             # API tests

docs/
├── CLINICAL_DECISION_SUPPORT_README.md
├── MEDICAL_APIs_GUIDE.md
└── REAL_MEDICAL_DATA_INTEGRATION.md
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                   STREAMLIT UI                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Patient Registration Form                        │   │
│  │ • Name, DOB, Gender                              │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Chat Interface                                   │   │
│  │ • Message input                                  │   │
│  │ • Message history                                │   │
│  │ • Streaming responses                            │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              STRANDS AGENT                              │
│  ┌──────────────────────────────────────────────────┐   │
│  │ System Prompt                                    │   │
│  │ "You are a friendly clinical assistant..."      │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ LLM (Claude 3.5 Sonnet)                          │   │
│  │ • Reads prompt + tools                           │   │
│  │ • Decides what to do                             │   │
│  │ • Generates responses                            │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Tools                                            │   │
│  │ • assess_vitals()                                │   │
│  │ • check_symptoms()                               │   │
│  │ • check_drug_interaction()                       │   │
│  │ • get_treatment_guidelines()                     │   │
│  │ • summarize_patient_session()                    │   │
│  │ • search_medical_knowledge()                     │   │
│  │ • get_real_drug_info()                           │   │
│  │ • check_real_drug_interactions()                 │   │
│  │ • get_drug_adverse_events()                      │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              EXTERNAL APIs                              │
│  • RxNorm (NIH) - Drug information                      │
│  • OpenFDA - Adverse events                             │
│  • SNOMED CT - Medical terminology                      │
│  • PubMed - Medical research                            │
└─────────────────────────────────────────────────────────┘
```

---

## Real Medical Data Integration

### How Real Data Works

```
User: "What are the side effects of aspirin?"
                    ↓
Agent decides to use get_drug_adverse_events()
                    ↓
Tool calls OpenFDA API:
  GET https://api.fda.gov/drug/event.json?search=aspirin
                    ↓
OpenFDA returns real adverse event data:
  {
    "results": [
      {"term": "FATIGUE", "count": 32886},
      {"term": "NAUSEA", "count": 27987}
    ]
  }
                    ↓
Agent generates response:
  "The most reported side effects are fatigue (32,886 reports)
   and nausea (27,987 reports)..."
```

### APIs Used

| API | Source | Data | Rate Limit |
|-----|--------|------|-----------|
| RxNorm | NIH | Drug info, interactions | Unlimited |
| OpenFDA | FDA | Adverse events | 240/min |
| SNOMED CT | SNOMED | Medical terms | Varies |
| PubMed | NIH | Research papers | 3/sec |

---

## Patient Registration

### How Patient Context Works

```
┌─────────────────────────────────────────────────────────┐
│ PATIENT REGISTRATION                                    │
│ • Name: John Doe                                        │
│ • DOB: 1989-05-15                                       │
│ • Gender: Male                                          │
│ • Age: 35 (calculated)                                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ STORED IN SESSION STATE                                 │
│ st.session_state.patient = {                            │
│   "name": "John Doe",                                   │
│   "dob": "1989-05-15",                                  │
│   "gender": "Male",                                     │
│   "age": 35                                             │
│ }                                                       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ ADDED TO EVERY MESSAGE                                  │
│ User: "I have a headache"                               │
│ + Patient Context: "Age: 35, Gender: Male"              │
│ = Full Input to Agent                                   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ AGENT USES CONTEXT                                      │
│ "For a 35-year-old male with a headache..."             │
│ (Personalized response based on age/gender)             │
└─────────────────────────────────────────────────────────┘
```

---

## Conversation Flow

### Example: Complete Conversation

```
┌─ STEP 1: PATIENT REGISTRATION ─────────────────────────┐
│ User fills form:                                        │
│ • Name: Sarah                                           │
│ • DOB: 1990-03-20                                       │
│ • Gender: Female                                        │
│ • Age: 34 (calculated)                                  │
└─────────────────────────────────────────────────────────┘

┌─ STEP 2: FIRST MESSAGE ────────────────────────────────┐
│ User: "my blood pressure is 160 over 90"                │
│                                                         │
│ Agent:                                                  │
│ 1. Reads system prompt                                  │
│ 2. Sees assess_vitals() tool                            │
│ 3. Calls: assess_vitals(160, 90, ?)                     │
│ 4. Gets: "stage2_hypertension"                          │
│ 5. Generates: "That's elevated, Sarah..."               │
│ 6. Asks: "Are you feeling anything?"                    │
└─────────────────────────────────────────────────────────┘

┌─ STEP 3: FOLLOW-UP ────────────────────────────────────┐
│ User: "no dizziness or anything"                        │
│                                                         │
│ Agent:                                                  │
│ 1. Acknowledges: "Good, that's reassuring"              │
│ 2. Provides advice: "Cut back on salt..."               │
│ 3. Asks: "Have you checked before?"                     │
└─────────────────────────────────────────────────────────┘

┌─ STEP 4: MEDICATION CHECK ─────────────────────────────┐
│ User: "i take metformin and lisinopril"                 │
│                                                         │
│ Agent:                                                  │
│ 1. Calls: check_real_drug_interactions()                │
│ 2. Gets: "No major interaction"                         │
│ 3. Generates: "Those work well together..."             │
│ 4. Asks: "How long have you been on them?"              │
└─────────────────────────────────────────────────────────┘

┌─ STEP 5: SUMMARY ──────────────────────────────────────┐
│ User: "summarize what we talked about"                  │
│                                                         │
│ Agent:                                                  │
│ 1. Calls: summarize_patient_session()                   │
│ 2. Gets: Clean summary with next steps                  │
│ 3. Displays: "Here's what we discussed..."              │
└─────────────────────────────────────────────────────────┘
```

---

## Code Examples

### Creating an Agent

```python
from strands import Agent, tool

# Define tools
@tool
def my_tool(param: str) -> dict:
    """Tool description"""
    return {"result": "data"}

# Create agent
agent = Agent(
    tools=[my_tool],
    system_prompt="You are helpful..."
)

# Use agent
response = agent("user message")
```

### Using Tools

```python
# Tool is called automatically by agent
# But you can also call directly:

result = assess_vitals(160, 90, 85)
print(result)
# Output: {
#   "bp_status": "stage2_hypertension",
#   "hr_status": "normal",
#   "flags": [...]
# }
```

### Streamlit Integration

```python
import streamlit as st
from strands import Agent, tool

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = Agent(...)

# Get user input
user_input = st.chat_input("Ask something...")

if user_input:
    # Call agent
    response = st.session_state.agent(user_input)
    
    # Display response
    st.write(response)
```

### Patient Context

```python
# Add patient context to message
patient_context = f"""
[Patient: {patient['name']}, Age: {patient['age']}, Gender: {patient['gender']}]
"""

full_input = user_message + patient_context
response = agent(full_input)
```

---

## Key Takeaways

### How It All Works Together

1. **User sends message** via Streamlit UI
2. **Patient context is added** (name, age, gender)
3. **Strands Agent receives** the full message
4. **LLM analyzes** and decides which tools to use
5. **Tools execute** and return data
6. **Agent generates** a friendly response
7. **Response streams** to UI word-by-word
8. **User sees** personalized, helpful answer

### The Magic of Strands

- **Automatic tool selection** - LLM decides what to use
- **Natural conversation** - Feels like talking to a real person
- **Tool integration** - Seamlessly uses external APIs
- **Context awareness** - Remembers patient info
- **Flexible** - Easy to add new tools

### Real Medical Data

- **RxNorm API** - Real drug information from NIH
- **OpenFDA API** - Real adverse events from FDA
- **No API keys** - All free and public
- **Evidence-based** - Trusted medical sources
- **Always accurate** - Real data, not hardcoded

---

## Next Steps

1. **Run the chatbot**: `streamlit run streamlit_app.py`
2. **Register a patient** with name, DOB, gender
3. **Chat naturally** - Ask about symptoms, medications, etc.
4. **See tools in action** - Watch the agent use real medical data
5. **Explore the code** - See how tools are defined and used

---

## Resources

- **Strands Documentation**: https://github.com/strands-ai/strands-agents
- **Claude API**: https://docs.anthropic.com/
- **Streamlit Docs**: https://docs.streamlit.io/
- **RxNorm API**: https://rxnav.nlm.nih.gov/
- **OpenFDA API**: https://open.fda.gov/

---

**You now understand how the entire Clinical Decision Support chatbot works!** 🏥
