# What-If Scenario Agent - Quick Start

## ⚡ Get Running in 5 Minutes

### Step 1: Make Sure Ollama is Running
```bash
ollama serve
```
Keep this terminal open.

### Step 2: Download Llama 2 (if not already done)
In a new terminal:
```bash
ollama pull llama2
```

### Step 3: Install Strands
```bash
pip install strands-agents
```

### Step 4: Run the Agent
```bash
python what_if_scenario_agent.py
```

### Step 5: Try a Scenario
```python
from what_if_scenario_agent import WhatIfScenarioOrchestrator

orchestrator = WhatIfScenarioOrchestrator()
result = orchestrator.run_workflow("What if the internet went down for 30 days?")
```

---

## 🎯 What Happens

The agent will:
1. Parse your scenario
2. Identify impacted domains
3. Generate first-order effects
4. Build ripple effect chains
5. Score severity of impacts
6. Produce a structured report

---

## 📊 Output

You'll get:
- Scenario summary
- List of impacted domains
- First-order effects per domain
- Ripple effect chains
- Severity rankings (1-5)
- Complete reasoning trace

---

## 🧪 Try These Scenarios

```python
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

## 📚 Learn More

- **WHAT_IF_BUILD_GUIDE.md** - How we built it
- **WHAT_IF_QUICK_REFERENCE.md** - Quick lookup
- **WHAT_IF_VISUAL_GUIDE.md** - Diagrams
- **WHAT_IF_COMPLETE_SUMMARY.md** - Full overview

---

## ❓ Troubleshooting

### "Connection refused"
Make sure Ollama is running: `ollama serve`

### "Model not found"
Download Llama 2: `ollama pull llama2`

### "Module not found"
Install Strands: `pip install strands-agents`

---

## 🚀 You're Ready!

Start analyzing scenarios now! 🎉

---

**Built with Strands Agent Framework** 🧠
