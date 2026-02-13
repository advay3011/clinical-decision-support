# Clinical Decision Support Chatbot - Quick Start

Get the clinical chatbot running in 2 minutes.

## 1. Install Dependencies

```bash
pip install strands-agents
```

## 2. Set API Key

```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
```

## 3. Run the Chatbot

```bash
python agents/clinical_decision_support_agent.py
```

## 4. Try a Sample Conversation

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
Agent: [Provides clean summary]

You: quit
Agent: Take care of yourself! Remember to follow up with your doctor if needed. Bye!
```

## 5. Test the Tools

```bash
python agents/test_clinical_agent.py
```

This runs:
- Individual tool tests
- Sample conversation flow
- Verification that everything works

## What the Agent Does

✅ Listens to patient concerns  
✅ Asks one thoughtful question at a time  
✅ Provides simple, actionable advice  
✅ Checks medication interactions  
✅ Assesses vital signs  
✅ Summarizes conversations  
✅ Always reminds patients to see a real doctor  

## Key Features

| Feature | Tool | Example |
|---------|------|---------|
| Vital Assessment | `assess_vitals()` | BP 160/90, HR 85 |
| Symptom Checking | `check_symptoms()` | Headache, fatigue |
| Drug Interactions | `check_drug_interaction()` | Metformin + Lisinopril |
| Treatment Guidelines | `get_treatment_guidelines()` | High blood pressure advice |
| Session Summary | `summarize_patient_session()` | Clean health report |
| Medical Knowledge | `search_medical_knowledge()` | What is lisinopril? |

## Conversation Tips

1. **Be natural** — Talk like you're texting a friend
2. **Share one thing at a time** — Don't dump all symptoms at once
3. **Ask follow-ups** — The agent will ask questions to understand better
4. **Mention medications** — Important for interaction checking
5. **Ask for summaries** — Get a clean report of what you discussed

## Common Commands

```
"my blood pressure is X over Y"     → Vital assessment
"i have a headache and fatigue"     → Symptom checking
"i take metformin and lisinopril"   → Drug interaction check
"what should i do about X?"         → Treatment guidelines
"summarize what we talked about"    → Session summary
"what is lisinopril?"               → Medical knowledge search
"quit" or "exit"                    → Exit chatbot
```

## Important Notes

⚠️ **This is a clinical assistant, not a doctor**  
⚠️ **For emergencies, call 911 or go to ER**  
⚠️ **Always see a real doctor for serious concerns**  
⚠️ **This tool provides general guidance only**  

## Troubleshooting

**Agent not responding?**
- Check API key: `echo $ANTHROPIC_API_KEY`
- Verify strands-agents installed: `pip list | grep strands`
- Check internet connection

**Want to customize?**
- Edit `agents/clinical_decision_support_agent.py`
- Add conditions to `get_treatment_guidelines()`
- Add medications to `search_medical_knowledge()`
- Adjust vital thresholds in `assess_vitals()`

## Next Steps

- Read full docs: `docs/CLINICAL_DECISION_SUPPORT_README.md`
- Customize for your needs
- Deploy as web service
- Integrate into your app

---

**Ready to chat?** Run: `python agents/clinical_decision_support_agent.py`
