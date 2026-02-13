# Clinical Decision Support Chatbot Agent

A friendly, knowledgeable clinical assistant built with the Strands Agents SDK that helps patients understand their health through natural conversation.

## Overview

This agent mimics a real doctor's conversational style — warm, attentive, and practical. It:
- Listens carefully to patient concerns
- Asks one thoughtful question at a time
- Provides simple, actionable advice
- Checks for medication interactions
- Summarizes conversations into health reports
- Always reminds patients to see a real doctor for serious concerns

## Features

### 1. **Vital Assessment** (`assess_vitals`)
Evaluates blood pressure and heart rate readings, flags abnormalities, and provides context.

```python
assess_vitals(systolic=160, diastolic=90, heart_rate=85)
# Returns: BP status, HR status, and any flags
```

### 2. **Symptom Checking** (`check_symptoms`)
Cross-references symptoms and returns possible conditions ranked by likelihood.

```python
check_symptoms(['headache', 'fatigue', 'dizziness'])
# Returns: Ranked list of possible conditions with disclaimer
```

### 3. **Drug Interaction Checker** (`check_drug_interaction`)
Checks for dangerous interactions between medications.

```python
check_drug_interaction(['metformin', 'lisinopril', 'aspirin'])
# Returns: Safety assessment and any interactions found
```

### 4. **Treatment Guidelines** (`get_treatment_guidelines`)
Provides plain English treatment guidelines for common conditions.

```python
get_treatment_guidelines('high blood pressure')
# Returns: Simple explanation, lifestyle changes, when to see doctor
```

### 5. **Session Summarizer** (`summarize_patient_session`)
Creates a clean health report from the conversation.

```python
summarize_patient_session("Patient reported elevated BP, stressed, on metformin and lisinopril...")
# Returns: Formatted summary with next steps
```

### 6. **Medical Knowledge Search** (`search_medical_knowledge`)
Searches the knowledge base for relevant health information.

```python
search_medical_knowledge('what is lisinopril')
# Returns: Plain English explanation
```

## Installation

1. Install the Strands Agents SDK:
```bash
pip install strands-agents
```

2. Set up your API key (Claude):
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

## Usage

### Interactive Chatbot

Run the interactive chatbot:
```bash
python agents/clinical_decision_support_agent.py
```

Example conversation:
```
You: hey my blood pressure is 160 over 90
Agent: That's a little on the high side — are you feeling anything along with it, like headaches or chest tightness?

You: no dizziness or anything
Agent: Good, that's reassuring. Since your pressure is elevated but you're not feeling symptoms, the main things that help day to day are cutting back on salty foods, drinking more water, and try to get some light movement in even just a short walk. Have you checked your blood pressure before or is this a new reading for you?

You: i've also been stressed lately
Agent: Stress can definitely push blood pressure up. That's actually really common. Managing stress helps bring it down naturally. Have you tried anything to help with the stress, or is this something new?

You: i take metformin, just started lisinopril too
Agent: Good — lisinopril is specifically for blood pressure, so that should help bring those numbers down over time. Metformin and lisinopril work well together with no major interactions. The key is staying consistent with them and keeping up with those lifestyle changes we talked about.

You: can you summarize what we talked about?
Agent: [Provides clean summary of session]
```

### Test the Agent

Run the test suite:
```bash
python agents/test_clinical_agent.py
```

This tests:
- Individual tools
- Sample conversation flow
- Tool integration

### Use in Your Own Code

```python
from clinical_decision_support_agent import agent

# Single query
response = agent("I've had a headache for 3 days")
print(response)

# Multi-turn conversation
messages = [
    "my blood pressure is 160 over 90",
    "no dizziness",
    "i'm stressed lately"
]

for msg in messages:
    response = agent(msg)
    print(f"Agent: {response}")
```

## Agent Personality & Behavior

### Tone
- Warm and friendly, like a real doctor
- Simple, plain English — never robotic
- Matches patient's energy (casual or worried)
- Acknowledges feelings before diving into advice

### Conversation Rules
1. **One insight at a time** — Never dump all information
2. **Acknowledge feelings first** — "That sounds stressful" before advice
3. **Ask one question at a time** — Never bombard with multiple questions
4. **Remember context** — Reference what they've told you naturally
5. **Transition to advice** — Don't keep asking questions forever
6. **Handle "no" gracefully** — Either ask one more question or move to advice
7. **Be honest but calm** — If something sounds serious, don't panic them
8. **Always end with a question** — Keep conversation flowing naturally

### Example Conversation Flow

```
Patient: "my blood pressure is 160 over 90"
↓
Agent: Acknowledge (that's high) + Ask one question (feeling anything?)
↓
Patient: "no dizziness or anything"
↓
Agent: Acknowledge (good, reassuring) + Give advice + Ask follow-up
↓
Patient: "i've also been stressed lately"
↓
Agent: Connect to BP + Ask about stress management
↓
Patient: "i take metformin, just started lisinopril too"
↓
Agent: Check interactions + Reassure + Give guidance
↓
Patient: "can you summarize?"
↓
Agent: Provide clean summary with next steps
```

## Important Disclaimers

The agent always reminds patients:
- This is a clinical assistant, not a replacement for real medical care
- For serious concerns (chest pain, severe symptoms), see a real doctor immediately
- All advice is general guidance only
- A real doctor needs to examine them for proper diagnosis

## Supported Conditions

The agent has guidelines for:
- High blood pressure (hypertension)
- Anxiety
- Tension headaches
- And can search knowledge base for others

## Medication Knowledge

Built-in knowledge of:
- Metformin (diabetes medication)
- Lisinopril (blood pressure medication)
- Common interactions and side effects
- When to contact a doctor

## Customization

### Add New Conditions

Edit `get_treatment_guidelines()`:
```python
guidelines = {
    "your condition": {
        "condition": "Your Condition",
        "simple_explanation": "...",
        "lifestyle_changes": [...],
        "when_to_see_doctor": "..."
    }
}
```

### Add New Medications

Edit `search_medical_knowledge()`:
```python
knowledge_base = {
    "your medication": "Plain English explanation...",
}
```

### Adjust Vital Thresholds

Edit `assess_vitals()` to change BP/HR ranges:
```python
if systolic < 120 and diastolic < 80:
    assessment["bp_status"] = "normal"
```

## Limitations

- Simplified symptom-condition mapping (not a real diagnostic tool)
- Limited medication interaction database
- Cannot perform physical examination
- Should not be used for emergency situations
- Always recommend real doctor for serious concerns

## Best Practices

1. **Always include disclaimer** — Remind patients this isn't medical advice
2. **Encourage real doctor visits** — For anything serious or persistent
3. **Ask clarifying questions** — Don't assume, verify symptoms
4. **Be empathetic** — Acknowledge how patients feel
5. **Give actionable advice** — Practical steps they can take today
6. **Follow up naturally** — Keep conversation flowing with questions

## Troubleshooting

### Agent not responding
- Check ANTHROPIC_API_KEY is set
- Verify strands-agents is installed: `pip install strands-agents`
- Check internet connection

### Tools not working
- Run `python agents/test_clinical_agent.py` to test individual tools
- Check tool parameters match expected types
- Verify agent has access to all tools

### Conversation feels robotic
- Adjust system prompt to be more casual
- Add more personality to tool responses
- Include more natural follow-up questions

## Files

- `agents/clinical_decision_support_agent.py` — Main agent implementation
- `agents/test_clinical_agent.py` — Test suite and examples
- `docs/CLINICAL_DECISION_SUPPORT_README.md` — This file

## Next Steps

1. Run the interactive chatbot: `python agents/clinical_decision_support_agent.py`
2. Test with sample conversation: `python agents/test_clinical_agent.py`
3. Customize conditions and medications for your use case
4. Deploy as a web service or integrate into your app

---

**Remember:** This is a clinical assistant tool, not a replacement for real medical care. Always encourage patients to see a real doctor for serious concerns.
