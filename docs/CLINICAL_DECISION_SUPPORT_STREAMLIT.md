# Clinical Decision Support - Streamlit Web App

Run the clinical chatbot as a beautiful web interface with Streamlit.

## Quick Start

```bash
# Install streamlit if you haven't already
pip install streamlit

# Run the web app
streamlit run agents/clinical_decision_support_streamlit.py
```

The app will open in your browser at `http://localhost:8501`

## Features

✅ **Beautiful Chat Interface** - Clean, modern UI for conversations  
✅ **Message History** - All messages persist during the session  
✅ **Sidebar Help** - Quick commands and usage tips  
✅ **Real-time Responses** - Streaming responses as they're generated  
✅ **Mobile Friendly** - Works on phones and tablets  
✅ **Session Management** - Separate conversations for each user  

## How to Use

1. **Open the app** - Navigate to `http://localhost:8501`
2. **Share your concern** - Type your health question or symptom
3. **Answer follow-ups** - The agent will ask clarifying questions
4. **Get guidance** - Receive practical advice and next steps
5. **Request summary** - Ask for a summary of your conversation

## Example Interactions

### Blood Pressure Check
```
You: my blood pressure is 160 over 90
Agent: That's a little on the high side — are you feeling anything along with it, like headaches or chest tightness?

You: no dizziness or anything
Agent: Good, that's reassuring. Since your pressure is elevated but you're not feeling symptoms, the main things that help day to day are cutting back on salty foods, drinking more water, and try to get some light movement in even just a short walk. Have you checked your blood pressure before or is this a new reading for you?
```

### Symptom Assessment
```
You: i have a headache and fatigue
Agent: That combination can come from a few things. Let me ask - how long have you had these symptoms? Just today, or has it been going on for a few days?

You: just today
Agent: Okay, so it's recent. That's helpful. Are you feeling feverish at all, or is it just the headache and tiredness?
```

### Medication Check
```
You: i take metformin and just started lisinopril
Agent: Good — lisinopril is specifically for blood pressure. Metformin and lisinopril work well together with no major interactions. The key is staying consistent with them.
```

## Customization

### Change the Title
Edit the page config:
```python
st.set_page_config(
    page_title="Your Custom Title",
    page_icon="🏥",
)
```

### Add More Conditions
Edit the `get_treatment_guidelines()` tool:
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

### Customize Sidebar
Edit the sidebar section:
```python
with st.sidebar:
    st.markdown("### Your Custom Title")
    st.markdown("Your custom content here")
```

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repo and file
5. Deploy!

### Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run agents/clinical_decision_support_streamlit.py" > Procfile

# Create requirements.txt
pip freeze > requirements.txt

# Deploy
git push heroku main
```

### Deploy to AWS/Azure/GCP

Use their container deployment services with Docker:

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY agents/ agents/
CMD ["streamlit", "run", "agents/clinical_decision_support_streamlit.py"]
```

## Troubleshooting

### App not loading
- Check that streamlit is installed: `pip install streamlit`
- Verify the file path is correct
- Check for Python errors: `streamlit run agents/clinical_decision_support_streamlit.py --logger.level=debug`

### Agent not responding
- Check API key is set: `echo $ANTHROPIC_API_KEY`
- Verify strands-agents is installed: `pip list | grep strands`
- Check internet connection

### Slow responses
- This is normal for the first response (model loading)
- Subsequent responses should be faster
- Consider using a faster model if available

## Performance Tips

1. **Cache the agent** - Already done with `@st.cache_resource`
2. **Use session state** - Messages are stored in session state
3. **Limit history** - Consider clearing old messages for long sessions
4. **Optimize tools** - Simplify tool logic for faster responses

## Advanced Features

### Add User Authentication
```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(...)
name, authentication_status, username = authenticator.login()
```

### Add Analytics
```python
import streamlit_analytics

with streamlit_analytics.track():
    # Your app code here
```

### Add File Upload
```python
uploaded_file = st.file_uploader("Upload medical records")
if uploaded_file:
    # Process file
```

### Add Export to PDF
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Generate PDF from conversation
```

## Files

- `agents/clinical_decision_support_streamlit.py` - Main Streamlit app
- `docs/CLINICAL_DECISION_SUPPORT_STREAMLIT.md` - This file

## Next Steps

1. Run the app: `streamlit run agents/clinical_decision_support_streamlit.py`
2. Test with sample conversations
3. Customize for your needs
4. Deploy to production

---

**Ready to launch?** Run: `streamlit run agents/clinical_decision_support_streamlit.py`
