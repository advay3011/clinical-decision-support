# What-If Scenario Agent - Step-by-Step Build Guide

## 📚 Complete Breakdown of How We Built This

This guide explains every step of building the What-If Scenario Agent.

---

## 🏗️ STEP 1: Foundation & Imports

**What we did:**
- Imported necessary libraries
- Explained the overall concept

**Why it matters:**
- `json`: For structured data (JSON output)
- `dataclasses`: For clean data structures
- `typing`: For type hints (makes code clearer)
- `strands`: The agent framework

**Key concept:**
Multi-stage reasoning ≠ Single prompt
- Single prompt: "Analyze this" → One LLM call → Done
- Multi-stage: Parse → Decompose → Simulate → Ripple → Rank → Report

---

## 📊 STEP 2: Data Structures (ScenarioState)

**What we did:**
Created a `ScenarioState` class to hold data across all 6 stages.

**Why it matters:**
Think of it like a "briefcase" that carries data through the workflow:

```
Stage 1 fills in: event, scope, duration, scale, entities
    ↓
Stage 2 reads those, adds: impacted_domains
    ↓
Stage 3 reads both, adds: first_order_impacts
    ↓
Stage 4 reads all, adds: ripple_effects
    ↓
Stage 5 reads all, adds: severity_rankings
    ↓
Stage 6 reads everything, produces: final report
```

**Without ScenarioState:**
- Data would be lost between stages
- Stages couldn't communicate
- No way to track what happened

**With ScenarioState:**
- All data persists
- Stages can access previous outputs
- Complete reasoning trace

---

## 🔧 STEP 3: The 6 Tools

**What we did:**
Created 6 specialized tools, each doing ONE focused job.

### Tool 1: scenario_parser
```
INPUT: User's hypothetical scenario
OUTPUT: Structured fields (event, scope, duration, scale, entities)
PURPOSE: Convert vague input into structured data
```

**Example:**
```
Input: "What if the internet went down for 30 days?"
Output: {
  "event": "Internet outage",
  "scope": "Global",
  "duration": "30 days",
  "scale": "8 billion people",
  "entities": ["ISPs", "Governments", "Corporations"]
}
```

### Tool 2: domain_mapper
```
INPUT: Scenario description
OUTPUT: List of impacted domains
PURPOSE: Organize thinking into categories
```

**7 Domains:**
1. Economy (markets, jobs, trade)
2. Healthcare (medical systems, public health)
3. Infrastructure (transportation, utilities)
4. Education (schools, universities)
5. Technology (digital systems, innovation)
6. Social Systems (governance, culture)
7. Individual Behavior (psychology, daily life)

### Tool 3: impact_generator
```
INPUT: Scenario + domain
OUTPUT: First-order direct consequences
PURPOSE: Identify immediate effects
```

**Example:**
```
Scenario: "Internet down for 30 days"
Domain: "Economy"
First-order impacts:
  - Stock market crashes (no trading)
  - Supply chains break (no coordination)
  - Financial systems offline (no transactions)
```

### Tool 4: ripple_chain_builder
```
INPUT: First-order impact
OUTPUT: Second and third-order chain reactions
PURPOSE: Show cascading effects
```

**Example:**
```
First-order: "Stock market crashes"
    ↓
Second-order: "People lose retirement savings"
    ↓
Third-order: "Elderly can't afford healthcare"

Chain: Crash → Savings lost → Healthcare unaffordable
```

### Tool 5: severity_scorer
```
INPUT: Impact description
OUTPUT: Severity score (1-5) + justification
PURPOSE: Prioritize which impacts matter most
```

**Severity Scale:**
- 1: Minimal disruption, quick recovery
- 2: Minor disruption, recoverable in days
- 3: Moderate disruption, recoverable in weeks
- 4: Severe disruption, recoverable in months
- 5: Catastrophic, long-term/permanent damage

### Tool 6: report_formatter
```
INPUT: All outputs from Stages 1-5
OUTPUT: Structured final report
PURPOSE: Format everything into readable output
```

**Report Sections:**
1. Scenario Summary
2. Impacted Domains
3. First-Order Effects
4. Ripple Effects
5. Severity Rankings
6. Reasoning Trace

---

## 🎭 STEP 4: The Orchestrator

**What we did:**
Created `WhatIfScenarioOrchestrator` class to coordinate all stages.

**Why it matters:**
The Orchestrator is like a CONDUCTOR:
- Doesn't do the analysis itself
- Tells each tool when to run
- Passes data between stages
- Ensures proper sequencing

**How it works:**

```python
orchestrator = WhatIfScenarioOrchestrator()
result = orchestrator.run_workflow("What if...")

# Inside run_workflow():
state = ScenarioState(user_prompt)
state = stage_1(state)  # Fills in event, scope, etc.
state = stage_2(state)  # Uses Stage 1 data, adds domains
state = stage_3(state)  # Uses Stages 1&2 data, adds impacts
state = stage_4(state)  # Uses Stage 3 data, adds ripples
state = stage_5(state)  # Uses Stages 3&4 data, adds scores
state = stage_6(state)  # Uses all data, produces report
```

**Key methods:**
- `run_workflow()`: Main entry point
- `_stage_1_parse_scenario()`: Stage 1 implementation
- `_stage_2_domain_decomposition()`: Stage 2 implementation
- ... (and so on for all 6 stages)
- `_compile_final_output()`: Combine all results

---

## 🤖 STEP 5: Strands Agent Wrapper

**What we did:**
Created `create_what_if_agent()` function to integrate with Strands.

**Why it matters:**
The Orchestrator is great for manual control.
But Strands agents are better for:
- Letting the LLM decide which tools to call
- Streaming responses
- Integration with other systems
- Production deployments

**How it works:**

```python
agent = Agent(
    model="ollama/llama2",           # Free local model
    tools=[
        scenario_parser,
        domain_mapper,
        impact_generator,
        ripple_chain_builder,
        severity_scorer,
        report_formatter
    ],
    system_prompt="Instructions..."  # How to behave
)

response = agent("What if...")       # Run the agent
```

**System Prompt tells the agent:**
- Use 6 stages in order
- Call appropriate tool for each stage
- Show reasoning between stages
- Produce structured output

---

## ⚙️ STEP 6: Main Execution

**What we did:**
Created the entry point with two usage methods.

**Method 1: Orchestrator (Manual Control)**
```python
orchestrator = WhatIfScenarioOrchestrator()
result = orchestrator.run_workflow("What if...")
```

**Pros:**
- See exactly what happens at each stage
- Full control over execution
- Great for learning

**Cons:**
- Manual, not using LLM reasoning
- Less flexible

**Method 2: Strands Agent (LLM-Driven)**
```python
agent = create_what_if_agent()
response = agent("What if...")
```

**Pros:**
- LLM decides tool usage
- More flexible
- Production-ready

**Cons:**
- Less predictable
- Less control over stage order

---

## 🔄 Complete Workflow Visualization

```
User Input: "What if the internet went down for 30 days?"
    ↓
[STAGE 1] Scenario Parser
    Input: User prompt
    Output: {event, scope, duration, scale, entities}
    ↓
[STAGE 2] Domain Decomposition
    Input: Parsed scenario
    Output: [economy, healthcare, infrastructure, ...]
    ↓
[STAGE 3] Impact Simulation
    Input: Scenario + Domains
    Output: {domain1: [impacts], domain2: [impacts], ...}
    ↓
[STAGE 4] Ripple Effect
    Input: First-order impacts
    Output: {second_order: [...], third_order: [...]}
    ↓
[STAGE 5] Severity Ranking
    Input: All impacts
    Output: {domain1: {score: 4, level: "Severe"}, ...}
    ↓
[STAGE 6] Report Formatter
    Input: All stage outputs
    Output: Structured JSON + Markdown report
    ↓
Final Report with:
- Scenario Summary
- Impacted Domains
- First-Order Effects
- Ripple Effects
- Severity Rankings
- Reasoning Trace
```

---

## 📋 Key Design Principles

### 1. Explicit Stage Transitions
Each stage has clear input/output contracts.
No hidden state or magic.

### 2. Tool Orchestration
Tools are called in sequence, not embedded in prompts.
Each tool does ONE focused job.

### 3. Intermediate State Passing
Each stage receives structured output from previous stage.
Data flows through the system.

### 4. Modular Architecture
New stages can be added without modifying existing ones.
Easy to extend.

### 5. Reasoning Transparency
Every decision is traceable through the reasoning trace.
You can see exactly how we got to the conclusion.

### 6. Structured Output
JSON for machines, Markdown for humans.
Both formats available.

---

## 🚀 How to Run It

### Prerequisites
1. Ollama installed and running: `ollama serve`
2. Llama 2 downloaded: `ollama pull llama2`
3. Python 3.10+
4. Strands installed: `pip install strands-agents`

### Run the Agent
```bash
python what_if_scenario_agent.py
```

### Try Different Scenarios
```python
from what_if_scenario_agent import WhatIfScenarioOrchestrator

orchestrator = WhatIfScenarioOrchestrator()

# Try different scenarios
scenarios = [
    "What if fossil fuels were banned tomorrow?",
    "What if a major earthquake hit Tokyo?",
    "What if all cars became autonomous?",
    "What if humans lived 200 years?",
    "What if we discovered alien life?"
]

for scenario in scenarios:
    result = orchestrator.run_workflow(scenario)
    print(result)
```

---

## 🎓 Learning Outcomes

After building this, you understand:

✓ **Multi-stage reasoning**: Breaking complex problems into stages
✓ **Tool orchestration**: Coordinating tool usage
✓ **State management**: Passing data between stages
✓ **Strands framework**: How to build agents
✓ **Structured output**: JSON + Markdown
✓ **Reasoning transparency**: Tracing decisions

---

## 🔧 Extending the Agent

### Adding a New Stage

1. Create a new tool:
```python
@tool
def new_stage_tool(input_data: str) -> str:
    """New stage description."""
    # Implementation
    return json.dumps(output)
```

2. Add to orchestrator:
```python
def _stage_7_new_stage(self, previous_output: Dict) -> Dict:
    """Stage 7: New stage."""
    # Implementation
    return output
```

3. Register with agent:
```python
agent = Agent(
    model="ollama/llama2",
    tools=[
        # ... existing tools ...
        new_stage_tool
    ]
)
```

---

## 📚 Resources

- [Strands Agent Documentation](https://github.com/strands-agents/samples)
- [Multi-Agent Reasoning](https://arxiv.org/abs/2305.16291)
- [Systems Thinking](https://en.wikipedia.org/wiki/Systems_thinking)

---

**Built with Strands Agent Framework** 🧠
