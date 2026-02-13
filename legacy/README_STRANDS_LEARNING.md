# Strands Learning Path - Complete Documentation

Welcome! This folder contains comprehensive documentation to help you understand Strands and build AI agents.

## 📚 Documents Overview

### 1. **LEARNING_SUMMARY.md** ⭐ START HERE
A concise overview of:
- What Strands is
- The three core components (Agent, Tools, System Prompt)
- How the recipe bot works
- Key concepts and best practices
- Quick reference guide

**Read this first** to get a solid foundation.

---

### 2. **QUICK_START_GUIDE.md** 🚀 PRACTICAL
Hands-on guide with:
- 5-minute overview
- Minimal working example
- Step-by-step agent building
- Common tool patterns
- Real-world examples
- Debugging tips
- Installation and configuration

**Use this** when you want to build something quickly.

---

### 3. **STRANDS_GUIDE.md** 📖 COMPREHENSIVE
Deep dive into:
- What Strands is and why it matters
- Complete recipe bot explanation (line by line)
- How Strands works under the hood
- Step-by-step agent building
- Complete working examples
- Model providers (Bedrock, Anthropic, OpenAI, Gemini, Llama)
- Best practices and troubleshooting

**Read this** for a thorough understanding.

---

### 4. **RECIPE_BOT_BREAKDOWN.md** 🔍 DETAILED ANALYSIS
Line-by-line breakdown of recipe_bot.py:
- Complete code with annotations
- Step-by-step execution example
- Key concepts explained
- Comparison with your first agent
- What you learned

**Use this** to understand the recipe bot example in detail.

---

### 5. **STRANDS_ARCHITECTURE.md** 🏗️ VISUAL DIAGRAMS
Visual representations of:
- How Strands works (complete flow)
- Recipe bot architecture
- Tool definition and execution
- Conversation history (multi-turn)
- Comparisons and key takeaways

**Reference this** when you need visual understanding.

---

## 🎯 Learning Path

### For Beginners:
1. Read **LEARNING_SUMMARY.md** (10 min)
2. Run **my_first_agent.py** (5 min)
3. Run **recipe_bot_explained.py** (10 min)
4. Read **RECIPE_BOT_BREAKDOWN.md** (15 min)
5. Build your own simple agent (30 min)

**Total: ~70 minutes**

### For Intermediate:
1. Read **STRANDS_GUIDE.md** (30 min)
2. Study **STRANDS_ARCHITECTURE.md** (20 min)
3. Build a multi-tool agent (60 min)
4. Try different LLM providers (30 min)

**Total: ~140 minutes**

### For Advanced:
1. Read all documentation (60 min)
2. Build a production-ready agent (120 min)
3. Integrate with external APIs (60 min)
4. Deploy and monitor (60 min)

**Total: ~300 minutes**

---

## 🔑 Key Concepts at a Glance

### What is Strands?
A Python framework for building AI agents that can use tools and maintain conversations.

### The Three Core Components:

```
┌─────────────────────────────────────────┐
│  TOOLS                                  │
│  Functions your agent can call          │
│  Marked with @tool decorator            │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  SYSTEM PROMPT                          │
│  Instructions for the agent             │
│  Defines personality and behavior       │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  AGENT                                  │
│  Combines tools + system prompt         │
│  Handles everything else                │
└─────────────────────────────────────────┘
```

### The Flow:
```
User Input → Agent → LLM → Tool Decision → Tool Execution → Response
```

---

## 📝 Code Examples

### Minimal Example
```python
from strands import Agent, tool

@tool
def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"

agent = Agent(
    system_prompt="You are friendly",
    tools=[greet],
)

response = agent("Say hello to Alice")
```

### Recipe Bot Pattern
```python
from strands import Agent, tool
from ddgs import DDGS

@tool
def websearch(keywords: str) -> str:
    """Search the web."""
    return DDGS().text(keywords)

agent = Agent(
    system_prompt="You are RecipeBot",
    tools=[websearch],
)

while True:
    user_input = input("You > ")
    response = agent(user_input)
    print(f"RecipeBot > {response}")
```

---

## 🛠️ Tools You Have

### 1. my_first_agent.py
Your first working agent using pre-built tools.
```bash
.venv/bin/python my_first_agent.py
```

### 2. recipe_bot_explained.py
Enhanced recipe bot with detailed comments.
```bash
.venv/bin/python recipe_bot_explained.py
```

### 3. Original recipe_bot.py
The original example from the samples folder.
```bash
cd samples/01-tutorials/01-fundamentals/01-first-agent/02-simple-interactive-usecase/
python recipe_bot.py
```

---

## 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| LEARNING_SUMMARY.md | Quick overview | 10 min |
| QUICK_START_GUIDE.md | Practical guide | 15 min |
| STRANDS_GUIDE.md | Comprehensive guide | 30 min |
| RECIPE_BOT_BREAKDOWN.md | Detailed analysis | 20 min |
| STRANDS_ARCHITECTURE.md | Visual diagrams | 15 min |
| README_STRANDS_LEARNING.md | This file | 5 min |

---

## 🎓 What You'll Learn

### Concepts:
- What Strands is and why it's useful
- How AI agents work
- Tool calling and execution
- Conversation history management
- System prompts and agent behavior
- Error handling and robustness

### Skills:
- Creating custom tools with `@tool` decorator
- Writing effective docstrings
- Building agents with system prompts
- Interactive agent loops
- Multi-turn conversations
- Debugging agent behavior
- Integrating external APIs
- Using different LLM providers

### Practical:
- Build your first agent
- Create custom tools
- Handle errors gracefully
- Test and iterate
- Deploy agents
- Monitor performance

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
.venv/bin/python -m pip install strands-agents strands-agents-tools duckduckgo-search
```

### 2. Run Your First Agent
```bash
.venv/bin/python my_first_agent.py
```

### 3. Run the Recipe Bot
```bash
.venv/bin/python recipe_bot_explained.py
```

### 4. Read the Documentation
Start with **LEARNING_SUMMARY.md**

### 5. Build Your Own Agent
Follow the pattern in **QUICK_START_GUIDE.md**

---

## 💡 Key Takeaways

1. **Strands = Tools + System Prompt + Agent**
2. **Docstrings are critical** - LLM reads them to understand tools
3. **Error handling matters** - Always handle exceptions
4. **System prompt guides behavior** - Be specific and clear
5. **Conversation history is automatic** - No extra work needed
6. **Tools are just functions** - Use `@tool` decorator
7. **Test early and often** - Iterate quickly

---

## 🔗 Resources

### Official Resources:
- Strands Documentation (in the power)
- Strands GitHub Repository
- AWS Bedrock Console

### In This Folder:
- STRANDS_GUIDE.md - Comprehensive guide
- QUICK_START_GUIDE.md - Practical examples
- RECIPE_BOT_BREAKDOWN.md - Detailed analysis
- STRANDS_ARCHITECTURE.md - Visual diagrams
- my_first_agent.py - Working example
- recipe_bot_explained.py - Enhanced example

### External Resources:
- DuckDuckGo Search API
- AWS Bedrock
- Anthropic Claude
- OpenAI GPT
- Google Gemini

---

## ❓ FAQ

### Q: Do I need to know Python?
**A:** Yes, basic Python knowledge is required. You should understand functions, decorators, and error handling.

### Q: Do I need an API key?
**A:** Yes, you need an LLM provider API key. Bedrock is the default (uses your AWS credentials).

### Q: Can I use different LLMs?
**A:** Yes! Strands supports Bedrock, Anthropic, OpenAI, Google Gemini, and Meta Llama.

### Q: How do I create custom tools?
**A:** Use the `@tool` decorator on any function. Write a clear docstring so the LLM understands it.

### Q: How does the agent remember conversations?
**A:** Strands automatically maintains conversation history. Each call to the agent includes previous messages.

### Q: What if my tool fails?
**A:** Always use try/except blocks to handle errors gracefully. Return error messages as strings.

### Q: Can I use Strands in production?
**A:** Yes! Strands is production-ready. Just ensure proper error handling and monitoring.

### Q: How do I debug my agent?
**A:** Enable logging with `logging.getLogger("strands").setLevel(logging.DEBUG)` to see what the agent is doing.

---

## 🎯 Next Steps

### Immediate (Today):
1. Read LEARNING_SUMMARY.md
2. Run my_first_agent.py
3. Run recipe_bot_explained.py

### Short Term (This Week):
1. Read STRANDS_GUIDE.md
2. Build your first custom agent
3. Experiment with different tools

### Medium Term (This Month):
1. Build a multi-tool agent
2. Try different LLM providers
3. Integrate with external APIs
4. Deploy an agent

### Long Term (This Quarter):
1. Build production-ready agents
2. Monitor and optimize performance
3. Contribute to Strands community
4. Build complex multi-agent systems

---

## 📞 Support

### If You Get Stuck:

1. **Check the documentation** - Most answers are in the guides
2. **Review the examples** - Look at my_first_agent.py and recipe_bot_explained.py
3. **Check error messages** - They usually tell you what's wrong
4. **Enable logging** - See what the agent is doing
5. **Test tools independently** - Ensure tools work before adding to agent

### Common Issues:

| Issue | Solution |
|-------|----------|
| Tool not used | Check docstring and system prompt |
| Wrong format | Ensure tool returns string |
| Incomplete response | Increase max_tokens |
| API key error | Check environment variables |
| Module not found | Install missing package |

---

## 🎉 You're Ready!

You now have everything you need to:
- Understand what Strands is
- Build your first AI agent
- Create custom tools
- Deploy production-ready agents

Start with **LEARNING_SUMMARY.md** and enjoy building!

---

## 📄 Document Structure

```
README_STRANDS_LEARNING.md (this file)
├── LEARNING_SUMMARY.md (start here)
├── QUICK_START_GUIDE.md (practical)
├── STRANDS_GUIDE.md (comprehensive)
├── RECIPE_BOT_BREAKDOWN.md (detailed)
├── STRANDS_ARCHITECTURE.md (visual)
├── my_first_agent.py (working example)
└── recipe_bot_explained.py (enhanced example)
```

---

## 🙏 Thank You

Thank you for learning Strands! We hope these guides help you build amazing AI agents.

Happy coding! 🚀
