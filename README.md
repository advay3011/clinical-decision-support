# Clinical Decision Support Chatbot

A friendly, AI-powered clinical assistant built with the Strands Agents SDK. Provides health guidance, medication interaction checking, and symptom assessment using real medical data from NIH and FDA APIs.

## 🏥 Features

- **Patient Registration** - Register patients with name, DOB, and gender
- **Real Medical Data** - Integrated RxNorm (NIH) and OpenFDA APIs
- **9 Clinical Tools** - 6 local tools + 3 API-based tools
- **Streamlit Web App** - Beautiful, user-friendly interface
- **Streaming Responses** - Real-time word-by-word output
- **Amazon Nova 2 Lite** - Fast, lightweight LLM model

## 📁 Project Structure

```
.
├── agents/
│   ├── clinical_decision_support_agent.py          # CLI version
│   ├── clinical_decision_support_streamlit.py      # Streamlit module
│   ├── clinical_decision_support_enhanced.py       # With real medical APIs
│   ├── test_clinical_agent.py                      # CLI tests
│   └── test_real_medical_data.py                   # API tests
│
├── docs/
│   ├── CLINICAL_DECISION_SUPPORT_README.md         # Main guide
│   ├── CLINICAL_DECISION_SUPPORT_QUICKSTART.md     # Quick start
│   ├── CLINICAL_DECISION_SUPPORT_COMPLETE_GUIDE.md # Deep dive
│   ├── STRANDS_EXPLAINED_SIMPLE.md                 # Strands basics
│   ├── STRANDS_AND_TOOLS_SIMPLE.md                 # One-page overview
│   ├── HOW_ASSESS_VITALS_WORKS.md                  # Tool deep dive
│   ├── APIS_USED.md                                # API documentation
│   ├── MEDICAL_APIs_GUIDE.md                       # Medical API guide
│   └── REAL_MEDICAL_DATA_INTEGRATION.md            # Integration details
│
├── streamlit_app.py                                # Main web app
├── .env.example                                    # Environment template
├── requirements.txt                                # Dependencies
└── README.md                                       # This file
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Credentials

Copy `.env.example` to `.env` and add your AWS credentials:

```bash
cp .env.example .env
```

Edit `.env` with:
- `AWS_ACCESS_KEY_ID` - Your AWS access key
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
- `AWS_DEFAULT_REGION` - us-east-1 (or your region)

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

Visit `http://localhost:8501` in your browser.

## 🛠️ Tools

### Local Tools (6)
1. **assess_vitals** - Evaluate blood pressure and heart rate
2. **check_symptoms** - Cross-reference symptoms with conditions
3. **check_drug_interaction** - Check medication interactions
4. **get_treatment_guidelines** - Get plain English treatment advice
5. **summarize_patient_session** - Create health report summaries
6. **search_medical_knowledge** - Search medical knowledge base

### API-Based Tools (3)
1. **get_real_drug_info** - RxNorm API (NIH) - Real drug information
2. **check_real_drug_interactions** - RxNorm API - Real drug interactions
3. **get_drug_adverse_events** - OpenFDA API - Real adverse event data

## 📚 Documentation

- **Getting Started:** `docs/CLINICAL_DECISION_SUPPORT_QUICKSTART.md`
- **Complete Guide:** `docs/CLINICAL_DECISION_SUPPORT_COMPLETE_GUIDE.md`
- **Strands Basics:** `docs/STRANDS_EXPLAINED_SIMPLE.md`
- **One-Page Overview:** `docs/STRANDS_AND_TOOLS_SIMPLE.md`
- **Tool Deep Dive:** `docs/HOW_ASSESS_VITALS_WORKS.md`
- **APIs Used:** `docs/APIS_USED.md`

## 🤖 How It Works

### Strands Framework
Strands is an agent framework that:
1. Takes user input
2. Decides which tools to use
3. Calls the tools
4. Processes results
5. Generates a response

### The Agent Loop
```
User Input → Agent Thinks → Selects Tools → Calls Tools → Processes Results → Response
```

### Example Conversation
```
User: "My blood pressure is 160 over 90"
Agent: "That's a little on the high side. Are you feeling anything like headaches?"
User: "No, just stressed lately"
Agent: "Stress can definitely raise blood pressure. Here's what helps..."
```

## ⚠️ Important Disclaimer

**This is a clinical assistant tool, NOT a replacement for real medical care.**

- For emergencies, call 911
- Always consult a real doctor for serious concerns
- This tool provides general guidance only
- Not for diagnosis or treatment decisions

## 🔧 Configuration

### Model
Currently uses **Amazon Nova 2 Lite** (`us.amazon.nova-2-lite-v1:0`)

To change the model, edit `streamlit_app.py`:
```python
agent = Agent(
    model="your-model-name",  # Change here
    tools=[...],
    system_prompt=system_prompt
)
```

### Streamlit Config
Edit `.streamlit/config.toml` to customize the web app appearance.

## 📊 Testing

### Test CLI Version
```bash
python agents/test_clinical_agent.py
```

### Test Real Medical APIs
```bash
python agents/test_real_medical_data.py
```

## 🌐 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub repo
4. Deploy

### Environment Variables
Set these in Streamlit Cloud secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

## 📦 Requirements

- Python 3.8+
- Strands Agents SDK
- Streamlit
- AWS credentials (for Bedrock/Nova model)

See `requirements.txt` for full list.

## 🎯 Use Cases

- Patient health consultations
- Medication interaction checking
- Symptom assessment
- Treatment guideline lookup
- Health education
- Medical data analysis

## 🔐 Security

- `.env` file is excluded from git (see `.gitignore`)
- Never commit credentials
- Use environment variables for secrets
- AWS credentials are required for production

## 📝 License

Educational use only.

## 🤝 Contributing

To improve the agent:
1. Add new tools in the agent file
2. Update documentation
3. Test thoroughly
4. Commit and push

## 📞 Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review the test files
3. Check Strands documentation

---

**Built with:** Strands Agents SDK, Amazon Bedrock, Streamlit

**Last Updated:** February 15, 2026
