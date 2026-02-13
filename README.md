# Strands Agent Framework - Project Workspace

A collection of AI agents built with the Strands Agent framework for various business use cases.

## 📁 Workspace Structure

```
.
├── agents/                    # Main agent implementations
│   ├── stock_predictor_agent.py
│   ├── supply_chain_optimizer_agent.py
│   ├── ops_consult_agent.py
│   ├── multi_agent_orchestrator.py
│   └── consulting_agent_demo.py
│
├── health_insights/           # Health Insights Agent (Educational)
│   ├── health_insights_agent.py
│   ├── health_insights_demo.py
│   ├── test_health_insights.py
│   ├── simple_test.py
│   ├── quick_test.py
│   └── health_insights_requirements.txt
│
├── docs/                      # Documentation
│   ├── HEALTH_INSIGHTS_README.md
│   ├── HEALTH_INSIGHTS_QUICK_START.md
│   ├── HEALTH_INSIGHTS_ARCHITECTURE.md
│   ├── HEALTH_INSIGHTS_EXAMPLES.md
│   ├── HEALTH_INSIGHTS_SUMMARY.md
│   ├── HEALTH_INSIGHTS_INDEX.md
│   ├── RUN_TESTS.md
│   └── TESTING_COMPLETE.txt
│
├── legacy/                    # Old files and tutorials
│   └── (archived files)
│
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🤖 Agents

### 1. Stock Predictor Agent
**Location:** `agents/stock_predictor_agent.py`

Analyzes stock prices and predicts trends using technical analysis.

**Tools:**
- Fetch historical stock data
- Calculate moving averages
- Analyze volatility
- Predict future trends
- Identify support/resistance levels
- Explain price movements
- Generate trading reports

**Run:** `python agents/stock_predictor_agent.py`

---

### 2. Supply Chain Optimizer Agent
**Location:** `agents/supply_chain_optimizer_agent.py`

Optimizes supplier selection and order allocation.

**Tools:**
- Score suppliers by reliability, speed, cost
- Allocate demand across suppliers
- Assess supply chain risk
- Calculate reorder points
- Simulate disruptions
- Generate recommendations

**Run:** `python agents/supply_chain_optimizer_agent.py`

---

### 3. Operations Consulting Agent
**Location:** `agents/ops_consult_agent.py`

Analyzes business problems and provides data-driven recommendations.

**Tools:**
- Classify business problems
- Summarize data and find trends
- Identify bottlenecks
- Analyze cost drivers
- Simulate scenarios
- Generate recommendations
- Create consultant reports

**Run:** `python agents/ops_consult_agent.py`

**Demo:** `python agents/consulting_agent_demo.py`

---

### 4. Health Insights Agent
**Location:** `health_insights/health_insights_agent.py`

Educational health analysis tool (NOT a medical diagnosis tool).

**Tools:**
- Extract lab values from medical reports
- Normalize units
- Check clinical reference ranges
- Flag abnormal values
- Detect multi-marker patterns
- Score risk levels
- Generate plain language explanations
- Build structured reports

**Run Tests:**
- `python health_insights/simple_test.py` (fastest)
- `python health_insights/quick_test.py` (4 scenarios)
- `python health_insights/health_insights_demo.py` (full walkthrough)
- `python health_insights/test_health_insights.py` (interactive)

**Documentation:** See `docs/HEALTH_INSIGHTS_*.md`

---

## 📚 Documentation

### Health Insights Agent Docs
- **Quick Start:** `docs/HEALTH_INSIGHTS_QUICK_START.md`
- **Full Guide:** `docs/HEALTH_INSIGHTS_README.md`
- **Architecture:** `docs/HEALTH_INSIGHTS_ARCHITECTURE.md`
- **Examples:** `docs/HEALTH_INSIGHTS_EXAMPLES.md`
- **Summary:** `docs/HEALTH_INSIGHTS_SUMMARY.md`
- **Index:** `docs/HEALTH_INSIGHTS_INDEX.md`

### Testing
- **Test Guide:** `docs/RUN_TESTS.md`
- **Test Results:** `docs/TESTING_COMPLETE.txt`

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run an Agent
```bash
# Stock Predictor
python agents/stock_predictor_agent.py

# Supply Chain Optimizer
python agents/supply_chain_optimizer_agent.py

# Operations Consultant
python agents/ops_consult_agent.py

# Health Insights (Demo)
python health_insights/simple_test.py
```

### 3. Test Health Insights
```bash
python health_insights/simple_test.py
```

---

## 📋 Agent Comparison

| Agent | Purpose | Use Case |
|-------|---------|----------|
| **Stock Predictor** | Analyze stock trends | Investment analysis |
| **Supply Chain Optimizer** | Optimize suppliers | Procurement decisions |
| **Operations Consultant** | Solve business problems | Process improvement |
| **Health Insights** | Analyze lab reports | Educational health info |

---

## ⚠️ Important Notes

### Health Insights Agent
- **Educational use only** - NOT a medical diagnosis tool
- Always includes medical disclaimer
- Recommends consulting healthcare professionals
- No treatment recommendations provided

### Other Agents
- Use simulated/demo data for examples
- Replace with real APIs for production use
- Requires Strands Agent framework

---

## 📦 Requirements

- Python 3.8+
- Strands Agent SDK (for agents)
- See `requirements.txt` for full list

---

## 🗂️ Legacy Files

Old tutorials, learning materials, and archived code are in the `legacy/` folder.

---

## 📝 License

Educational use only.

---

## 🤝 Contributing

To add a new agent:
1. Create agent file in `agents/` folder
2. Add documentation in `docs/` folder
3. Update this README

---

**Last Updated:** February 5, 2026
