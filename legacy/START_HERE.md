# 🚀 START HERE - Strands Learning Guide

Welcome! You've just learned about Strands and the recipe bot. This file will guide you through all the resources we've created.

---

## ⚡ Quick Start (5 minutes)

### What is Strands?
A Python framework for building AI agents that can use tools and maintain conversations.

### The Three Core Components:
1. **Tools** - Functions your agent can call (marked with `@tool`)
2. **System Prompt** - Instructions that define the agent's personality
3. **Agent** - Combines tools + system prompt and handles everything

### Minimal Example:
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

---

## 📚 Choose Your Learning Path

### Path 1: I have 30 minutes
```
1. Read LEARNING_SUMMARY.md (10 min)
2. Run my_first_agent.py (5 min)
3. Read QUICK_START_GUIDE.md (10 min)
4. Understand the basics ✓
```

### Path 2: I have 90 minutes
```
1. Read LEARNING_SUMMARY.md (10 min)
2. Run my_first_agent.py (5 min)
3. Read STRANDS_GUIDE.md (30 min)
4. Read RECIPE_BOT_BREAKDOWN.md (20 min)
5. Run recipe_bot_explained.py (10 min)
6. Read STRANDS_ARCHITECTURE.md (10 min)
7. Deep understanding ✓
```

### Path 3: I have 120 minutes
```
1. Complete Path 2 (90 min)
2. Build your own agent (30 min)
3. Ready to build! ✓
```

---

## 📖 Documentation Files

| File | Purpose | Time | Start Here? |
|------|---------|------|-------------|
| **README_STRANDS_LEARNING.md** | Overview & index | 5 min | ✅ YES |
| **LEARNING_SUMMARY.md** | Quick overview | 10 min | ✅ YES |
| **QUICK_START_GUIDE.md** | Practical guide | 15 min | ✅ YES |
| **STRANDS_GUIDE.md** | Comprehensive | 30 min | 📖 |
| **RECIPE_BOT_BREAKDOWN.md** | Detailed analysis | 20 min | 📖 |
| **STRANDS_ARCHITECTURE.md** | Visual diagrams | 15 min | 📖 |
| **DOCUMENTATION_MAP.md** | Navigation guide | 5 min | 📖 |

---

## 💻 Code Examples

### 1. my_first_agent.py
Your first working agent with pre-built tools.
```bash
.venv/bin/python my_first_agent.py
```

### 2. recipe_bot_explained.py
Enhanced recipe bot with detailed comments.
```bash
.venv/bin/python recipe_bot_explained.py
```

### 3. Original recipe_bot.py
The original example from Strands samples.
```bash
cd samples/01-tutorials/01-fundamentals/01-first-agent/02-simple-interactive-usecase/
python recipe_bot.py
```

---

## 🎯 What You'll Learn

After going through these resources, you'll understand:

✓ What Strands is and why it's useful
✓ How AI agents work
✓ How to create custom tools
✓ Why docstrings matter for LLM understanding
✓ How to build interactive agents
✓ How conversation history works
✓ Error handling and best practices
✓ How to deploy agents

---

## 🔑 Key Concepts

### The Flow:
```
User Input → Agent → LLM → Tool Decision → Tool Execution → Response
```

### Why Docstrings Matter:
The LLM reads tool docstrings to understand:
- What the tool does
- What parameters it needs
- When to use it
- What to expect as output

### Conversation History:
```python
agent("My name is Alice")
response = agent("What's my name?")
# Agent remembers: "Alice"
```

---

## 🚀 Next Steps

### Immediate (Today):
1. Read **LEARNING_SUMMARY.md** (10 min)
2. Run **my_first_agent.py** (5 min)
3. Read **QUICK_START_GUIDE.md** (10 min)

### Short Term (This Week):
1. Read **STRANDS_GUIDE.md** (30 min)
2. Read **RECIPE_BOT_BREAKDOWN.md** (20 min)
3. Run **recipe_bot_explained.py** (10 min)
4. Build your first custom agent (60 min)

### Medium Term (This Month):
1. Build a multi-tool agent
2. Try different LLM providers
3. Integrate with external APIs
4. Deploy an agent

---

## ❓ FAQ

**Q: Do I need to know Python?**
A: Yes, basic Python knowledge is required.

**Q: Do I need an API key?**
A: Yes, you need an LLM provider API key. Bedrock is the default.

**Q: Can I use different LLMs?**
A: Yes! Strands supports Bedrock, Anthropic, OpenAI, Gemini, and Llama.

**Q: How do I create custom tools?**
A: Use the `@tool` decorator on any function with a clear docstring.

**Q: How does the agent remember conversations?**
A: Strands automatically maintains conversation history.

**Q: What if my tool fails?**
A: Always use try/except blocks to handle errors gracefully.

---

## 💡 Key Takeaways

1. **Strands = Tools + System Prompt + Agent**
2. **Docstrings are critical** - LLM reads them
3. **Error handling matters** - Always handle exceptions
4. **System prompt guides behavior** - Be specific
5. **Conversation history is automatic** - No extra work
6. **Tools are just functions** - Use `@tool` decorator
7. **Test early and often** - Iterate quickly

---

## 📊 Learning Resources Summary

```
Total Documentation: ~83K
Total Code Examples: ~4K
Total Learning Material: ~87K

Estimated Reading Time: 95 minutes
Estimated Hands-On Time: 120 minutes
Total Learning Time: ~215 minutes (3.5 hours)
```

---

## ✅ Checklist

- [ ] Read LEARNING_SUMMARY.md
- [ ] Run my_first_agent.py
- [ ] Read QUICK_START_GUIDE.md
- [ ] Read STRANDS_GUIDE.md
- [ ] Read RECIPE_BOT_BREAKDOWN.md
- [ ] Run recipe_bot_explained.py
- [ ] Read STRANDS_ARCHITECTURE.md
- [ ] Build your first custom agent
- [ ] Deploy your agent

---

## 🎉 You're Ready!

You now have everything you need to:
- Understand what Strands is
- Build your first AI agent
- Create custom tools
- Deploy production-ready agents

**Start with LEARNING_SUMMARY.md and enjoy building!**

---

## 📞 Need Help?

### Check These First:
1. **README_STRANDS_LEARNING.md** - FAQ section
2. **QUICK_START_GUIDE.md** - Debugging tips
3. **STRANDS_GUIDE.md** - Troubleshooting section

### Common Questions:
- "How do I create a tool?" → QUICK_START_GUIDE.md
- "Why isn't my agent using the tool?" → QUICK_START_GUIDE.md (Debugging)
- "How does conversation history work?" → STRANDS_ARCHITECTURE.md
- "What's the recipe bot doing?" → RECIPE_BOT_BREAKDOWN.md

---

## 🗺️ File Navigation

```
START_HERE.md (you are here)
├─ LEARNING_SUMMARY.md (quick overview)
├─ QUICK_START_GUIDE.md (practical guide)
├─ STRANDS_GUIDE.md (comprehensive)
├─ RECIPE_BOT_BREAKDOWN.md (detailed analysis)
├─ STRANDS_ARCHITECTURE.md (visual diagrams)
├─ README_STRANDS_LEARNING.md (overview & index)
├─ DOCUMENTATION_MAP.md (navigation guide)
├─ my_first_agent.py (working example)
└─ recipe_bot_explained.py (enhanced example)
```

---

## 🚀 Ready to Start?

### Option 1: Quick Overview (10 minutes)
→ Read **LEARNING_SUMMARY.md**

### Option 2: Practical Guide (15 minutes)
→ Read **QUICK_START_GUIDE.md**

### Option 3: Complete Learning (90 minutes)
→ Read **README_STRANDS_LEARNING.md** for the full path

### Option 4: See Everything
→ Read **DOCUMENTATION_MAP.md** for navigation

---

## 🎓 What's Next?

1. **Choose your learning path** above
2. **Read the documentation** in order
3. **Run the code examples** to see it in action
4. **Build your own agent** following the patterns
5. **Deploy and iterate** based on results

---

## 🙏 Thank You

Thank you for learning Strands! We hope these resources help you build amazing AI agents.

**Happy coding! 🚀**

---

**Last Updated:** January 24, 2026
**Total Resources:** 7 documentation files + 2 code examples
**Total Learning Material:** ~87K
