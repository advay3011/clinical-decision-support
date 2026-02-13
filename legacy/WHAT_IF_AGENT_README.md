# What-If Scenario Agent - Multi-Strand Reasoning Workflow

A sophisticated Strands-based AI agent that analyzes hypothetical scenarios through structured multi-stage reasoning and tool orchestration.

## 🎯 Purpose

The What-If Scenario Agent takes user-provided hypothetical scenarios and simulates their consequences through a 6-stage reasoning workflow. Instead of a single LLM call, it uses explicit stage transitions, tool orchestration, and intermediate state passing to produce comprehensive scenario analysis.

**Example scenarios:**
- "What if the internet went down for 30 days?"
- "What if a major earthquake hit Tokyo?"
- "What if AI became sentient tomorrow?"
- "What if fossil fuels were banned globally?"

## 🏗️ Architecture

### Multi-Strand Workflow

```
User Scenario
    ↓
[STAGE 1] Scenario Parser Strand
    ↓ (structured scenario fields)
[STAGE 2] Domain Decomposition Strand
    ↓ (impacted domains list)
[STAGE 3] Impact Simulation Strand
    ↓ (first-order effects)
[STAGE 4] Ripple Effect Strand
    ↓ (second/third-order chains)
[STAGE 5] Severity Ranking Strand
    ↓ (severity scores)
[STAGE 6] Report Formatter Strand
    ↓
Structured JSON Report + Markdown
```

### Key Principle: Explicit Stage Transitions

Each stage:
1. Receives input from previous stage
2. Performs focused reasoning
3. Outputs structured data
4. Passes to next stage
5. Shows reasoning trace

This is NOT a single prompt chain - it's true multi-strand orchestration.

## 📋 Workflow Stages

### Stage 1: Scenario Parser
**Input:** User's hypothetical scenario  
**Output:** Structured scenario fields

Extracts:
- **Event**: What is happening?
- **Scope**: Geographic/organizational scope
- **Duration**: How long does it last?
- **Scale**: How many people/systems affected?
- **Entities**: Key actors/systems involved

**Tool:** `scenario_parser(user_prompt)`

---

### Stage 2: Domain Decomposition
**Input:** Parsed scenario  
**Output:** List of impacted domains

Maps scenario to 7 domains:
- **Economy**: Markets, jobs, trade, financial systems
- **Healthcare**: Medical systems, public health
- **Infrastructure**: Transportation, utilities, communications
- **Education**: Schools, universities, learning
- **Technology**: Digital systems, innovation
- **Social Systems**: Governance, culture, relationships
- **Individual Behavior**: Psychology, daily life

**Tool:** `domain_mapper(scenario_description)`

---

### Stage 3: Impact Simulation
**Input:** Scenario + impacted domains  
**Output:** First-order direct consequences

For each domain, generates:
- Impact description
- Causal explanation (why this happens)
- Affected entities
- Onset time (immediate/days/weeks/months)
- Magnitude (small/medium/large)

**Tool:** `impact_generator(scenario, domain)`

---

### Stage 4: Ripple Effect
**Input:** First-order impacts  
**Output:** Second and third-order chain reactions

Builds downstream chains:
- **Second-order**: Direct consequences of first-order impacts
- **Third-order**: Consequences of second-order effects

Represents as: `Cause → Effect → Effect` chains

**Tool:** `ripple_chain_builder(first_order_impact)`

---

### Stage 5: Severity Ranking
**Input:** All impacts (first, second, third-order)  
**Output:** Severity scores and rankings

Scores each impact 1-5:
- **1**: Minimal disruption, quick recovery
- **2**: Minor disruption, recoverable in days
- **3**: Moderate disruption, recoverable in weeks
- **4**: Severe disruption, recoverable in months
- **5**: Catastrophic, long-term/permanent damage

Considers:
- Scale of disruption
- Recovery difficulty
- Cascading effects
- Vulnerable populations affected

**Tool:** `severity_scorer(impact_description)`

---

### Stage 6: Report Formatter
**Input:** All prior stage outputs  
**Output:** Structured final report

Produces:
- Scenario Summary
- Impacted Domains
- First-Order Effects
- Ripple Effects
- Severity Rankings
- Reasoning Trace

**Tool:** `report_formatter(all_outputs)`

## 🔧 Tools

### Tool 1: scenario_parser
```python
@tool
def scenario_parser(user_prompt: str) -> str:
    """Extract structured scenario fields."""
    # Returns JSON with: event, scope, duration, scale, entities
```

### Tool 2: domain_mapper
```python
@tool
def domain_mapper(scenario_description: str) -> str:
    """Map scenario to impacted domains."""
    # Returns JSON with: impacted_domains list
```

### Tool 3: impact_generator
```python
@tool
def impact_generator(scenario: str, domain: str) -> str:
    """Generate first-order impacts per domain."""
    # Returns JSON with: impacts list with explanations
```

### Tool 4: ripple_chain_builder
```python
@tool
def ripple_chain_builder(first_order_impact: str) -> str:
    """Generate second/third-order chain reactions."""
    # Returns JSON with: ripple_effects chains
```

### Tool 5: severity_scorer
```python
@tool
def severity_scorer(impact_description: str) -> str:
    """Score impact severity 1-5."""
    # Returns JSON with: severity_score, justification
```

### Tool 6: report_formatter
```python
@tool
def report_formatter(all_outputs: str) -> str:
    """Format all outputs into structured report."""
    # Returns JSON structured report
```

## 📊 Output Format

### JSON Structure
```json
{
  "workflow_status": "complete",
  "scenario": "User's hypothetical scenario",
  "stages": {
    "stage_1": {
      "event": "...",
      "scope": "...",
      "duration": "...",
      "scale": "...",
      "entities": [...]
    },
    "stage_2": {
      "impacted_domains": [...]
    },
    "stage_3": {
      "first_order_impacts": {
        "domain1": [...],
        "domain2": [...]
      }
    },
    "stage_4": {
      "second_order": [...],
      "third_order": [...]
    },
    "stage_5": {
      "rankings": {
        "domain1": {"score": 4, "level": "Severe"},
        "domain2": {"score": 3, "level": "Moderate"}
      }
    },
    "stage_6": {
      "report_type": "What-If Scenario Analysis",
      "reasoning_trace": {...}
    }
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
- Infrastructure
- ...

## First-Order Effects
### Economy
- Effect 1: ...
- Effect 2: ...

### Healthcare
- Effect 1: ...
- Effect 2: ...

## Ripple Effects
### Second-Order Chains
- Cause → Effect
- Cause → Effect

### Third-Order Chains
- Cause → Effect
- Cause → Effect

## Severity Rankings
| Domain | Score | Level | Justification |
|--------|-------|-------|---------------|
| Economy | 4 | Severe | ... |
| Healthcare | 3 | Moderate | ... |

## Reasoning Trace
- Stage 1: Scenario parsed ✓
- Stage 2: Domains identified ✓
- Stage 3: First-order impacts ✓
- Stage 4: Ripple effects ✓
- Stage 5: Severity ranking ✓
- Stage 6: Report formatted ✓
```

## 🚀 Usage

### Basic Usage
```python
from what_if_scenario_agent import WhatIfScenarioOrchestrator

orchestrator = WhatIfScenarioOrchestrator()
result = orchestrator.run_workflow(
    "What if the internet went down for 30 days?"
)

print(result)
```

### With Strands Agent
```python
from what_if_scenario_agent import create_what_if_agent

agent = create_what_if_agent()
response = agent("What if AI became sentient tomorrow?")
```

## 🎓 Key Design Principles

### 1. Explicit Stage Transitions
Each stage has clear input/output contracts. No hidden state.

### 2. Tool Orchestration
Tools are called in sequence, not embedded in prompts.

### 3. Intermediate State Passing
Each stage receives structured output from previous stage.

### 4. Modular Architecture
New stages can be added without modifying existing ones.

### 5. Reasoning Transparency
Every decision is traceable through the reasoning trace.

### 6. Structured Output
JSON + Markdown for both machine and human consumption.

## 🔄 Workflow Execution Example

```
Input: "What if the internet went down for 30 days?"

[STAGE 1] Scenario Parser Strand
✓ Scenario parsed: Internet outage
  Scope: Global
  Duration: 30 days
  Scale: 8 billion people
  Entities: ISPs, Governments, Corporations, Individuals

[STAGE 2] Domain Decomposition Strand
✓ Domains identified: 7 domains
  • economy
  • healthcare
  • infrastructure
  • education
  • technology
  • social_systems
  • individual_behavior

[STAGE 3] Impact Simulation Strand
✓ First-order impacts generated
  economy: 3 impacts
    - Global stock market crash
    - Supply chain disruption
    - Financial system paralysis
  healthcare: 2 impacts
    - Hospital systems offline
    - Emergency response impaired
  ...

[STAGE 4] Ripple Effect Strand
✓ Ripple effects generated
  Second-order chains: 12
  Third-order chains: 8

[STAGE 5] Severity Ranking Strand
✓ Severity rankings computed
  economy: 5/5 (Catastrophic)
  healthcare: 4/5 (Severe)
  infrastructure: 5/5 (Catastrophic)
  ...

[STAGE 6] Report Formatter Strand
✓ Structured report generated

WORKFLOW COMPLETE
```

## 🛠️ Extending the Agent

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

## 📈 Complexity Levels

### Level 1: Simple Scenarios
- Single domain impact
- 2-3 ripple effects
- Quick analysis

### Level 2: Complex Scenarios
- Multiple domain impacts
- 5-10 ripple effects
- Detailed analysis

### Level 3: Systemic Scenarios
- All domains affected
- 20+ ripple effects
- Comprehensive analysis

## 🎯 Use Cases

1. **Policy Analysis**: Simulate policy changes
2. **Risk Assessment**: Analyze potential disasters
3. **Strategic Planning**: Explore future scenarios
4. **Education**: Teach systems thinking
5. **Research**: Study complex systems
6. **Business**: Scenario planning

## 📚 Resources

- [Strands Agent Documentation](https://github.com/strands-agents/samples)
- [Multi-Agent Reasoning Patterns](https://arxiv.org/abs/2305.16291)
- [Systems Thinking](https://en.wikipedia.org/wiki/Systems_thinking)

## 🔐 Notes

- This is a demonstration system
- Real-world scenarios require domain expertise
- Outputs should be validated by experts
- Use for educational and analytical purposes

---

**Built with Strands Agent Framework** 🧠
