# Strands Process & Tools - Super Simple Explanation

## What is Strands?

Strands is a framework that lets you create an AI agent that can use tools to help users.

Think of it like this:
- **You** = The user asking questions
- **Agent** = An AI assistant (Claude)
- **Tools** = Functions the agent can use to help you
- **Strands** = The framework that connects them all

## The Simple Process

```
1. You ask a question
   ↓
2. Agent reads your question
   ↓
3. Agent decides which tool to use
   ↓
4. Tool runs and returns data
   ↓
5. Agent uses that data to answer you
   ↓
6. You see the answer
```

## Real Example

```
You: "My blood pressure is 160 over 90"

Agent thinks: "This is about vitals. I should use assess_vitals()"

Tool runs: assess_vitals(160, 90, 85)
Returns: "This is Stage 2 hypertension"

Agent responds: "That's elevated. Let me ask you..."

You see: Friendly response about your BP
```

## The 9 Tools

### 1. assess_vitals()
**What it does:** Checks if blood pressure and heart rate are normal
**Input:** systolic, diastolic, heart_rate
**Output:** "normal", "elevated", "stage1_hypertension", etc.
**Example:** assess_vitals(160, 90, 85) → "stage2_hypertension"

### 2. check_symptoms()
**What it does:** Finds possible conditions based on symptoms
**Input:** List of symptoms like ["headache", "fatigue"]
**Output:** List of possible conditions ranked by likelihood
**Example:** check_symptoms(["headache", "fatigue"]) → ["tension headache", "migraine", ...]

### 3. check_drug_interaction()
**What it does:** Checks if two drugs interact badly
**Input:** List of drug names like ["aspirin", "warfarin"]
**Output:** Whether they're safe together and severity
**Example:** check_drug_interaction(["aspirin", "warfarin"]) → "HIGH severity interaction"

### 4. get_treatment_guidelines()
**What it does:** Gives plain English advice for a condition
**Input:** Condition name like "high blood pressure"
**Output:** Simple explanation and lifestyle tips
**Example:** get_treatment_guidelines("high blood pressure") → "Cut back on salt, drink water, exercise..."

### 5. summarize_patient_session()
**What it does:** Creates a clean summary of the conversation
**Input:** Everything discussed
**Output:** Clean health report with next steps
**Example:** Summarizes BP reading, symptoms, and advice into a report

### 6. search_medical_knowledge()
**What it does:** Searches medical knowledge base
**Input:** Query like "what is metformin"
**Output:** Plain English explanation
**Example:** search_medical_knowledge("metformin") → "A diabetes medication that..."

### 7. get_real_drug_info()
**What it does:** Gets real drug data from NIH (RxNorm API)
**Input:** Drug name like "aspirin"
**Output:** Real drug information
**Example:** get_real_drug_info("aspirin") → Real data from NIH

### 8. check_real_drug_interactions()
**What it does:** Gets real drug interactions from NIH
**Input:** List of drugs
**Output:** Real interaction data
**Example:** check_real_drug_interactions(["aspirin", "warfarin"]) → Real interaction from NIH

### 9. get_drug_adverse_events()
**What it does:** Gets real side effects from FDA database
**Input:** Drug name
**Output:** Real adverse events with report counts
**Example:** get_drug_adverse_events("aspirin") → "Fatigue: 32,886 reports, Nausea: 27,987 reports"

## What the Agent Does

The agent is Claude (an AI). It:

1. **Reads your message** - Understands what you're asking
2. **Reads the system prompt** - Knows it should be friendly and ask one question at a time
3. **Looks at available tools** - Sees which tools it can use
4. **Decides which tool to use** - Based on your question
5. **Calls the tool** - Runs the tool and gets data
6. **Generates a response** - Uses the tool data to answer you
7. **Adds patient context** - Remembers your name, age, gender
8. **Sends response** - You see the answer

## The System Prompt

This tells the agent how to behave:

```
"You are a friendly clinical assistant.
You talk in simple, plain English.
You ask one question at a time.
You always remind patients to see a real doctor.
You remember patient information.
You use tools to get real medical data."
```

## How Tools Are Used

### Automatic Selection
The agent automatically picks the right tool:

| User Says | Tool Used |
|-----------|-----------|
| "My BP is 160/90" | assess_vitals() |
| "I have a headache" | check_symptoms() |
| "I take aspirin and ibuprofen" | check_drug_interaction() |
| "What should I do?" | get_treatment_guidelines() |
| "Summarize our chat" | summarize_patient_session() |
| "What is metformin?" | search_medical_knowledge() |

### Tool Execution
```
User: "I take aspirin and warfarin"
     ↓
Agent: "I'll use check_real_drug_interactions()"
     ↓
Tool: Calls NIH API
     ↓
Result: "HIGH severity interaction - increased bleeding risk"
     ↓
Agent: "These have a HIGH severity interaction..."
```

## The Complete Flow

```
┌─────────────────────────────────────────┐
│ 1. USER SENDS MESSAGE                   │
│    "My blood pressure is 160 over 90"   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 2. AGENT RECEIVES MESSAGE               │
│    + System prompt (instructions)       │
│    + Available tools                    │
│    + Patient context (name, age, etc)   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 3. AGENT ANALYZES                       │
│    "This is about vitals"               │
│    "I should use assess_vitals()"       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 4. TOOL EXECUTES                        │
│    assess_vitals(160, 90, 85)           │
│    Returns: "stage2_hypertension"       │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 5. AGENT GENERATES RESPONSE             │
│    Uses tool result                     │
│    Adds patient context                 │
│    Generates friendly message           │
│    Adds follow-up question              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│ 6. RESPONSE STREAMS TO USER             │
│    Words appear one by one              │
│    User sees friendly answer            │
└─────────────────────────────────────────┘
```

## Key Points

1. **Agent decides** - You don't tell it which tool to use, it figures it out
2. **Tools are functions** - Each tool is a Python function that does something
3. **Real data** - Some tools use real APIs (NIH, FDA)
4. **Natural conversation** - Feels like talking to a real doctor
5. **Context aware** - Remembers patient info and previous messages
6. **Always safe** - Always reminds users to see a real doctor

## Summary

**Strands = Framework**
- Connects user → agent → tools

**Agent = Claude (AI)**
- Reads your message
- Decides which tool to use
- Generates response

**Tools = Functions**
- assess_vitals() - Check BP/HR
- check_symptoms() - Find conditions
- check_drug_interaction() - Check drug safety
- get_treatment_guidelines() - Get advice
- summarize_patient_session() - Create report
- search_medical_knowledge() - Search info
- get_real_drug_info() - Real drug data
- check_real_drug_interactions() - Real interactions
- get_drug_adverse_events() - Real side effects

**Process:**
1. You ask → 2. Agent reads → 3. Agent picks tool → 4. Tool runs → 5. Agent responds → 6. You see answer

**That's it!** 🎉

---

**Want more details?** Check out:
- `STRANDS_EXPLAINED_SIMPLE.md` - More detailed explanation
- `CLINICAL_DECISION_SUPPORT_COMPLETE_GUIDE.md` - Full technical guide
- `HOW_ASSESS_VITALS_WORKS.md` - Deep dive into one tool
