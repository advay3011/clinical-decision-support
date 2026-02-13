# What-If Scenario Agent - Quick Reference

## 🎯 What Is This?

A multi-stage AI agent that analyzes hypothetical scenarios through 6 explicit reasoning stages.

**Example:**
```
Input: "What if the internet went down for 30 days?"
Output: Structured analysis of impacts on economy, healthcare, infrastructure, etc.
```

---

## 🏗️ The 6 Stages

| Stage | Name | Input | Output | Purpose |
|-------|------|-------|--------|---------|
| 1 | Scenario Parser | User prompt | Structured fields | Extract event, scope, duration, scale, entities |
| 2 | Domain Decomposition | Parsed scenario | Domain list | Identify impacted domains (7 categories) |
| 3 | Impact Simulation | Scenario + Domains | First-order impacts | Generate direct consequences per domain |
| 4 | Ripple Effect | First-order impacts | Chain reactions | Build 2nd and 3rd-order effects |
| 5 | Severity Ranking | All impacts | Severity scores | Score impacts 1-5 based on disruption |
| 6 | Report Formatter | All outputs | Final report | Format into JSON + Markdown |

---

## 🔧 The 6 Tools

```python
# Tool 1: Parse scenario
scenario_parser(user_prompt: str) -> str

# Tool 2: Map domains
domain_mapper(scenario_description: str) -> str

# Tool 3: Generate impacts
impact_generator(scenario: str, domain: str) -> str

# Tool 4: Build ripples
ripple_chain_builder(first_order_impact: str) -> str

# Tool 5: Score severity
severity_scorer(impact_description: str) -> str

# Tool 6: Format report
report_formatter(all_outputs: str) -> str
```

---

## 📊 Data Flow

```
ScenarioState (briefcase carrying data)
    ↓
Stage 1: Fills in event, scope, duration, scale, entities
    ↓
Stage 2: Adds impacted_domains
    ↓
Stage 3: Adds first_order_impacts
    ↓
Stage 4: Adds ripple_effects
    ↓
Stage 5: Adds severity_rankings
    ↓
Stage 6: Produces final report
```

---

## 🚀 How to Use

### Method 1: Orchestrator (Manual Control)
```python
from what_if_scenario_agent import WhatIfScenarioOrchestrator

orchestrator = WhatIfScenarioOrchestrator()
result = orchestrator.run_workflow("What if...")
```

### Method 2: Strands Agent (LLM-Driven)
```python
from what_if_scenario_agent import create_what_if_agent

agent = create_what_if_agent()
response = agent("What if...")
```

---

## 📋 7 Impacted Domains

1. **Economy**: Markets, jobs, trade, financial systems
2. **Healthcare**: Medical systems, public health, mental health
3. **Infrastructure**: Transportation, utilities, communications
4. **Education**: Schools, universities, learning systems
5. **Technology**: Digital systems, innovation, connectivity
6. **Social Systems**: Governance, culture, social structures
7. **Individual Behavior**: Psychology, daily routines, relationships

---

## 📈 Severity Scale (1-5)

| Score | Level | Recovery Time | Description |
|-------|-------|----------------|-------------|
| 1 | Minimal | Days | Quick recovery, minimal disruption |
| 2 | Minor | Days | Recoverable in days |
| 3 | Moderate | Weeks | Recoverable in weeks |
| 4 | Severe | Months | Recoverable in months |
| 5 | Catastrophic | Years+ | Long-term or permanent damage |

---

## 🔄 Ripple Effects

**First-Order**: Direct consequences of the scenario
```
Scenario: Internet down
First-order: Stock market crashes
```

**Second-Order**: Consequences of first-order effects
```
First-order: Stock market crashes
Second-order: People lose retirement savings
```

**Third-Order**: Consequences of second-order effects
```
Second-order: People lose retirement savings
Third-order: Elderly can't afford healthcare
```

---

## 📊 Output Format

### JSON Structure
```json
{
  "workflow_status": "complete",
  "scenario": "User's scenario",
  "stages": {
    "stage_1": {...},
    "stage_2": {...},
    "stage_3": {...},
    "stage_4": {...},
    "stage_5": {...},
    "stage_6": {...}
  }
}
```

### Markdown Report
```markdown
# What-If Scenario Analysis Report

## Scenario Summary
- Event: ...
- Scope: ...
- Duration: ...
- Scale: ...

## Impacted Domains
- Economy
- Healthcare
- ...

## First-Order Effects
### Economy
- Effect 1
- Effect 2

## Ripple Effects
### Second-Order
- Chain 1
- Chain 2

## Severity Rankings
| Domain | Score | Level |
|--------|-------|-------|
| Economy | 4 | Severe |

## Reasoning Trace
- Stage 1: ✓
- Stage 2: ✓
- ...
```

---

## 🎓 Key Concepts

### Multi-Stage Reasoning
Breaking complex analysis into focused stages instead of one big prompt.

### Tool Orchestration
Calling tools in sequence, each doing one focused job.

### State Management
Passing data between stages using ScenarioState.

### Reasoning Transparency
Every decision is traceable through the reasoning trace.

### Modular Architecture
Easy to add new stages without modifying existing ones.

---

## ⚙️ Prerequisites

- Python 3.10+
- Ollama installed and running
- Llama 2 model downloaded
- Strands framework installed

### Setup
```bash
# Start Ollama
ollama serve

# In another terminal, download Llama 2
ollama pull llama2

# Install dependencies
pip install strands-agents

# Run the agent
python what_if_scenario_agent.py
```

---

## 🧪 Example Scenarios

```
"What if fossil fuels were banned tomorrow?"
"What if a major earthquake hit Tokyo?"
"What if all cars became autonomous?"
"What if humans lived 200 years?"
"What if we discovered alien life?"
"What if AI became sentient?"
"What if climate change reversed?"
"What if money was abolished?"
```

---

## 🔗 Files

- `what_if_scenario_agent.py` - Main implementation
- `WHAT_IF_BUILD_GUIDE.md` - Detailed build explanation
- `WHAT_IF_AGENT_README.md` - Full documentation
- `WHAT_IF_QUICK_REFERENCE.md` - This file

---

## 💡 Tips

1. **Start simple**: Try basic scenarios first
2. **Read the reasoning trace**: Understand how conclusions were reached
3. **Extend it**: Add new stages or domains
4. **Experiment**: Try different scenarios
5. **Learn**: Study how multi-stage reasoning works

---

**Built with Strands Agent Framework** 🧠
