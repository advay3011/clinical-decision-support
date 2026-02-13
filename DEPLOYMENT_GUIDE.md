# Deployment Guide - Clinical Decision Support Chatbot

Deploy your clinical chatbot to Streamlit Cloud and GitHub.

## Step 1: Push to GitHub

### 1.1 Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Create a new repository named `clinical-decision-support` (or your preferred name)
3. **Do NOT** initialize with README (we already have one)
4. Click "Create repository"

### 1.2 Push Your Code

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: Clinical Decision Support Chatbot with Streamlit"

# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 1.3 Verify on GitHub

- Go to your repository URL: `https://github.com/YOUR_USERNAME/REPO_NAME`
- You should see all your files including `streamlit_app.py`

## Step 2: Deploy to Streamlit Cloud

### 2.1 Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up"
3. Sign in with GitHub (recommended)
4. Authorize Streamlit to access your GitHub account

### 2.2 Deploy Your App

1. Click "New app"
2. Select your repository:
   - **Repository**: `YOUR_USERNAME/REPO_NAME`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
3. Click "Deploy"

### 2.3 Add Secrets (API Key)

1. After deployment, click the three dots (⋯) in the top right
2. Select "Settings"
3. Go to "Secrets"
4. Add your API key:
   ```
   ANTHROPIC_API_KEY = "your-api-key-here"
   ```
5. Save

### 2.4 Your App is Live!

Your app will be available at:
```
https://YOUR_USERNAME-REPO_NAME.streamlit.app
```

## Step 3: Update Your GitHub Profile

### 3.1 Add to README

Edit your main `README.md` to include:

```markdown
## 🚀 Live Demo

Try the Clinical Decision Support Chatbot:
[**Launch App** →](https://YOUR_USERNAME-REPO_NAME.streamlit.app)

## Features

- 🏥 Friendly clinical assistant
- 💬 Natural conversation flow
- 📊 Vital sign assessment
- 💊 Medication interaction checking
- 📋 Session summaries
- ⚠️ Always recommends real doctor consultation
```

### 3.2 Add to GitHub Profile

1. Go to your GitHub profile
2. Edit your profile bio to mention this project
3. Pin this repository to your profile

## Step 4: Continuous Updates

### 4.1 Make Changes Locally

```bash
# Make your changes
# Edit files as needed

# Commit and push
git add .
git commit -m "Update: [describe your changes]"
git push origin main
```

### 4.2 Streamlit Cloud Auto-Deploys

- Streamlit Cloud automatically redeploys when you push to GitHub
- Check deployment status at [share.streamlit.io](https://share.streamlit.io)
- Your app updates within 1-2 minutes

## Troubleshooting

### App won't deploy

**Error: "ModuleNotFoundError: No module named 'strands'"**
- Make sure `requirements.txt` includes `strands-agents`
- Streamlit Cloud installs from `requirements.txt` automatically

**Error: "ANTHROPIC_API_KEY not found"**
- Add your API key to Streamlit Cloud Secrets (see Step 2.3)
- Don't commit `.env` file to GitHub (it's in `.gitignore`)

### App is slow

- First load takes 30-60 seconds (model initialization)
- Subsequent responses are faster
- Consider using a faster model if available

### Changes not showing up

- Wait 1-2 minutes for auto-deployment
- Check deployment logs at [share.streamlit.io](https://share.streamlit.io)
- Try hard refresh (Cmd+Shift+R or Ctrl+Shift+R)

## Advanced: Custom Domain

To use a custom domain (e.g., `clinical-assistant.com`):

1. Go to your app settings on Streamlit Cloud
2. Click "Settings" → "Custom domain"
3. Enter your domain
4. Update DNS records (instructions provided)

## Advanced: GitHub Actions (Optional)

Create `.github/workflows/deploy.yml` for automated testing:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ (if you add tests)
```

## File Structure for Deployment

```
your-repo/
├── streamlit_app.py          # Main entry point (required)
├── requirements.txt          # Dependencies (required)
├── .streamlit/
│   └── config.toml          # Streamlit config
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
├── DEPLOYMENT_GUIDE.md      # This file
├── agents/
│   ├── clinical_decision_support_agent.py
│   ├── clinical_decision_support_streamlit.py
│   └── test_clinical_agent.py
└── docs/
    ├── CLINICAL_DECISION_SUPPORT_README.md
    ├── CLINICAL_DECISION_SUPPORT_QUICKSTART.md
    └── CLINICAL_DECISION_SUPPORT_STREAMLIT.md
```

## Summary

1. ✅ Push to GitHub
2. ✅ Deploy to Streamlit Cloud
3. ✅ Add API key to Streamlit Secrets
4. ✅ Share your live app link
5. ✅ Update GitHub profile

Your app is now live and will auto-update whenever you push to GitHub!

## Support

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-cloud
- Strands Agents: https://github.com/strands-ai/strands-agents
- GitHub Help: https://docs.github.com

---

**Questions?** Check the troubleshooting section or refer to the official documentation links above.
