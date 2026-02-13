# What-If Scenario Agent - Visual Guide

## 🎯 Complete System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INPUT SCENARIO                          │
│         "What if the internet went down for 30 days?"           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │   SCENARIO STATE (Briefcase)       │
        │  Carries data through all stages   │
        └────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Stage 1 │    │ Stage 2 │    │ Stage 3 │
    │ Parser  │───▶│ Domain  │───▶│ Impact  │
    │         │    │ Mapper  │    │Generator│
    └─────────┘    └─────────┘    └─────────┘
        │              │              │
        │ Fills in:    │ Adds:        │ Adds:
        │ • event      │ • domains    │ • impacts
        │ • scope      │              │
        │ • duration   │              │
        │ • scale      │              │
        │ • entities   │              │
        │              │              │
        └──────────────┴──────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │   SCENARIO STATE (Updated)         │
        │  Now has: event, scope, duration,  │
        │  scale, entities, domains, impacts │
        └────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Stage 4 │    │ Stage 5 │    │ Stage 6 │
    │ Ripple  │───▶│Severity │───▶│ Report  │
    │ Builder │    │ Scorer  │    │Formatter│
    └─────────┘    └─────────┘    └─────────┘
        │              │              │
        │ Adds:        │ Adds:        │ Produces:
        │ • ripples    │ • scores     │ • JSON
        │ • chains     │ • rankings   │ • Markdown
        │              │              │
        └──────────────┴──────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │      FINAL STRUCTURED REPORT       │
        │  • Scenario Summary                │
        │  • Impacted Domains                │
        │  • First-Order Effects             │
        │  • Ripple Effects                  │
        │  • Severity Rankings               │
        │  • Reasoning Trace                 │
        └────────────────────────────────────┘
```

---

## 🔄 Stage-by-Stage Flow

### Stage 1: Scenario Parser
```
INPUT:
┌──────────────────────────────────────────┐
│ "What if the internet went down for     │
│  30 days?"                               │
└──────────────────────────────────────────┘

PROCESSING:
┌──────────────────────────────────────────┐
│ Extract structured fields:               │
│ • What is the event?                     │
│ • What is the scope?                     │
│ • How long does it last?                 │
│ • How many people affected?              │
│ • Who/what are the key entities?         │
└──────────────────────────────────────────┘

OUTPUT:
┌──────────────────────────────────────────┐
│ {                                        │
│   "event": "Internet outage",            │
│   "scope": "Global",                     │
│   "duration": "30 days",                 │
│   "scale": "8 billion people",           │
│   "entities": ["ISPs", "Governments",    │
│                "Corporations", ...]      │
│ }                                        │
└──────────────────────────────────────────┘
```

### Stage 2: Domain Decomposition
```
INPUT: Parsed scenario from Stage 1

PROCESSING:
Which domains are affected?

┌─────────────────────────────────────────────┐
│ 1. Economy      ✓ (no trading, no jobs)     │
│ 2. Healthcare   ✓ (systems offline)         │
│ 3. Infrastructure ✓ (no coordination)       │
│ 4. Education    ✓ (schools closed)          │
│ 5. Technology   ✓ (all systems down)        │
│ 6. Social Systems ✓ (chaos, panic)          │
│ 7. Individual Behavior ✓ (fear, stress)     │
└─────────────────────────────────────────────┘

OUTPUT:
[economy, healthcare, infrastructure, 
 education, technology, social_systems, 
 individual_behavior]
```

### Stage 3: Impact Simulation
```
INPUT: Scenario + Domains

PROCESSING:
For EACH domain, what are the DIRECT effects?

┌─────────────────────────────────────────────┐
│ ECONOMY:                                    │
│ • Stock market crashes (no trading)         │
│ • Supply chains break (no coordination)     │
│ • Financial systems offline (no trans.)     │
│                                             │
│ HEALTHCARE:                                 │
│ • Hospital systems offline                  │
│ • Emergency response impaired               │
│ • Telemedicine unavailable                  │
│                                             │
│ INFRASTRUCTURE:                             │
│ • Traffic lights offline                    │
│ • Power grid coordination fails             │
│ • Water treatment systems affected          │
│ ... (and so on for all 7 domains)           │
└─────────────────────────────────────────────┘

OUTPUT:
{
  "economy": [impact1, impact2, impact3],
  "healthcare": [impact1, impact2],
  "infrastructure": [impact1, impact2, impact3],
  ...
}
```

### Stage 4: Ripple Effects
```
INPUT: First-order impacts

PROCESSING:
For EACH impact, what are the CASCADING effects?

EXAMPLE CHAIN:
┌─────────────────────────────────────────────┐
│ First-order:                                │
│ "Stock market crashes"                      │
│         │                                   │
│         ▼                                   │
│ Second-order:                               │
│ "People lose retirement savings"            │
│         │                                   │
│         ▼                                   │
│ Third-order:                                │
│ "Elderly can't afford healthcare"           │
│         │                                   │
│         ▼                                   │
│ Fourth-order (if we tracked it):            │
│ "Healthcare system overwhelmed"             │
└─────────────────────────────────────────────┘

OUTPUT:
{
  "second_order": [
    {"cause": "Stock crash", "effect": "Savings lost"},
    {"cause": "Supply break", "effect": "Shortages"},
    ...
  ],
  "third_order": [
    {"cause": "Savings lost", "effect": "Healthcare unaffordable"},
    ...
  ]
}
```

### Stage 5: Severity Ranking
```
INPUT: All impacts (first, second, third-order)

PROCESSING:
Score each impact 1-5

SCORING FACTORS:
┌─────────────────────────────────────────────┐
│ • Scale of disruption (how many affected?)  │
│ • Recovery difficulty (how hard to fix?)    │
│ • Cascading effects (does it cause more?)   │
│ • Vulnerable populations (who's hit worst?) │
└─────────────────────────────────────────────┘

EXAMPLE SCORING:
┌─────────────────────────────────────────────┐
│ Impact: "Stock market crashes"              │
│                                             │
│ Scale: 5/5 (affects billions)               │
│ Recovery: 4/5 (takes months)                │
│ Cascading: 5/5 (causes many effects)        │
│ Vulnerable: 4/5 (elderly, poor hit hard)    │
│                                             │
│ FINAL SCORE: 4.5 → 4/5 (SEVERE)             │
└─────────────────────────────────────────────┘

OUTPUT:
{
  "economy": {"score": 5, "level": "Catastrophic"},
  "healthcare": {"score": 4, "level": "Severe"},
  "infrastructure": {"score": 5, "level": "Catastrophic"},
  ...
}
```

### Stage 6: Report Formatter
```
INPUT: All outputs from Stages 1-5

PROCESSING:
Combine everything into readable report

OUTPUT:
┌─────────────────────────────────────────────┐
│ WHAT-IF SCENARIO ANALYSIS REPORT            │
│                                             │
│ SCENARIO SUMMARY                            │
│ • Event: Internet outage                    │
│ • Scope: Global                             │
│ • Duration: 30 days                         │
│ • Scale: 8 billion people                   │
│                                             │
│ IMPACTED DOMAINS (7)                        │
│ • Economy                                   │
│ • Healthcare                                │
│ • Infrastructure                            │
│ • Education                                 │
│ • Technology                                │
│ • Social Systems                            │
│ • Individual Behavior                       │
│                                             │
│ FIRST-ORDER EFFECTS                         │
│ Economy:                                    │
│   - Stock market crashes                    │
│   - Supply chains break                     │
│   - Financial systems offline               │
│ Healthcare:                                 │
│   - Hospital systems offline                │
│   - Emergency response impaired             │
│ ... (and so on)                             │
│                                             │
│ RIPPLE EFFECTS                              │
│ Second-Order:                               │
│   - Stock crash → Savings lost              │
│   - Supply break → Shortages                │
│ Third-Order:                                │
│   - Savings lost → Healthcare unaffordable  │
│   - Shortages → Panic buying                │
│                                             │
│ SEVERITY RANKINGS                           │
│ Economy: 5/5 (Catastrophic)                 │
│ Healthcare: 4/5 (Severe)                    │
│ Infrastructure: 5/5 (Catastrophic)          │
│ Education: 3/5 (Moderate)                   │
│ Technology: 5/5 (Catastrophic)              │
│ Social Systems: 4/5 (Severe)                │
│ Individual Behavior: 4/5 (Severe)           │
│                                             │
│ REASONING TRACE                             │
│ ✓ Stage 1: Scenario parsed                  │
│ ✓ Stage 2: Domains identified               │
│ ✓ Stage 3: First-order impacts generated    │
│ ✓ Stage 4: Ripple effects generated         │
│ ✓ Stage 5: Severity ranking computed        │
│ ✓ Stage 6: Report formatted                 │
└─────────────────────────────────────────────┘
```

---

## 🎭 Two Usage Methods

### Method 1: Orchestrator (Manual Control)
```
┌──────────────────────────────────────────┐
│ orchestrator = WhatIfScenarioOrchestrator()
│ result = orchestrator.run_workflow(...)  │
└──────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│ Orchestrator controls every stage        │
│ • Calls Stage 1                          │
│ • Waits for result                       │
│ • Calls Stage 2                          │
│ • Waits for result                       │
│ • ... (and so on)                        │
└──────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│ You see EXACTLY what happens             │
│ Perfect for learning                     │
└──────────────────────────────────────────┘
```

### Method 2: Strands Agent (LLM-Driven)
```
┌──────────────────────────────────────────┐
│ agent = create_what_if_agent()           │
│ response = agent("What if...")           │
└──────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│ LLM decides which tools to call           │
│ • Reads system prompt                    │
│ • Decides: "I should call tool 1"        │
│ • Calls tool 1                           │
│ • Reads result                           │
│ • Decides: "Now I should call tool 2"    │
│ • ... (and so on)                        │
└──────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│ More flexible, less predictable          │
│ Good for production                      │
└──────────────────────────────────────────┘
```

---

## 📊 Data Structure Visualization

```
ScenarioState (The Briefcase)

┌─────────────────────────────────────────┐
│ user_prompt: "What if..."               │
│                                         │
│ [STAGE 1 FILLS IN]                      │
│ event: "Internet outage"                │
│ scope: "Global"                         │
│ duration: "30 days"                     │
│ scale: "8 billion"                      │
│ entities: [...]                         │
│                                         │
│ [STAGE 2 FILLS IN]                      │
│ impacted_domains: [...]                 │
│                                         │
│ [STAGE 3 FILLS IN]                      │
│ first_order_impacts: {...}              │
│                                         │
│ [STAGE 4 FILLS IN]                      │
│ ripple_effects: [...]                   │
│                                         │
│ [STAGE 5 FILLS IN]                      │
│ severity_rankings: {...}                │
│                                         │
│ [STAGE 6 READS ALL]                     │
│ → Produces final report                 │
└─────────────────────────────────────────┘
```

---

## 🔗 Tool Connections

```
┌─────────────────────────────────────────────────────────────┐
│                    STRANDS AGENT                            │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ System Prompt:                                       │  │
│  │ "Use 6 stages in order, call appropriate tool"      │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│         ┌───────────────┼───────────────┐                   │
│         │               │               │                   │
│         ▼               ▼               ▼                   │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐              │
│    │ Tool 1  │    │ Tool 2  │    │ Tool 3  │              │
│    │ Parser  │    │ Mapper  │    │Generator│              │
│    └─────────┘    └─────────┘    └─────────┘              │
│         │               │               │                   │
│         └───────────────┼───────────────┘                   │
│                         │                                   │
│         ┌───────────────┼───────────────┐                   │
│         │               │               │                   │
│         ▼               ▼               ▼                   │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐              │
│    │ Tool 4  │    │ Tool 5  │    │ Tool 6  │              │
│    │ Ripple  │    │ Scorer  │    │Formatter│              │
│    └─────────┘    └─────────┘    └─────────┘              │
│         │               │               │                   │
│         └───────────────┴───────────────┘                   │
│                         │                                   │
│                         ▼                                   │
│              ┌──────────────────────┐                       │
│              │  Final Report        │                       │
│              │  (JSON + Markdown)   │                       │
│              └──────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎓 Learning Path

```
START HERE
    │
    ▼
Understand Stage 1 (Parse)
    │
    ▼
Understand Stage 2 (Decompose)
    │
    ▼
Understand Stage 3 (Simulate)
    │
    ▼
Understand Stage 4 (Ripple)
    │
    ▼
Understand Stage 5 (Rank)
    │
    ▼
Understand Stage 6 (Report)
    │
    ▼
Understand Orchestrator (Coordinates all)
    │
    ▼
Understand Strands Integration (LLM-driven)
    │
    ▼
Run the agent
    │
    ▼
Try different scenarios
    │
    ▼
Extend with new stages
    │
    ▼
MASTERY ✓
```

---

**Built with Strands Agent Framework** 🧠
