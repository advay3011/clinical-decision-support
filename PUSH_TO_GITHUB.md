# Push Your Code to GitHub

Your code is committed locally and ready to push! Follow these steps:

## Step 1: Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Create a new repository:
   - **Repository name**: `clinical-decision-support` (or your preferred name)
   - **Description**: "🏥 Clinical Decision Support Chatbot - AI-powered health assistant using Strands Agents SDK"
   - **Visibility**: Public (so others can see it)
   - **Do NOT** initialize with README (we already have one)
3. Click "Create repository"

## Step 2: Add Remote and Push

Replace `YOUR_USERNAME` and `REPO_NAME` with your actual values:

```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

### Example:
If your GitHub username is `john-doe` and repo is `clinical-decision-support`:

```bash
git remote add origin https://github.com/john-doe/clinical-decision-support.git
git branch -M main
git push -u origin main
```

## Step 3: Verify on GitHub

1. Go to your repository: `https://github.com/YOUR_USERNAME/REPO_NAME`
2. You should see all your files including:
   - ✅ `streamlit_app.py`
   - ✅ `requirements.txt`
   - ✅ `.streamlit/config.toml`
   - ✅ `agents/` folder
   - ✅ `docs/` folder
   - ✅ All deployment guides

## Step 4: Deploy to Streamlit Cloud

Once your code is on GitHub:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - **Repository**: `YOUR_USERNAME/REPO_NAME`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
5. Click "Deploy"

## Step 5: Add API Key

After deployment:

1. Click ⋯ (top right)
2. Select "Settings"
3. Go to "Secrets"
4. Add:
   ```
   ANTHROPIC_API_KEY = "your-api-key-here"
   ```
5. Save

Your app will be live at: `https://YOUR_USERNAME-REPO_NAME.streamlit.app`

---

## Need Help?

- **GitHub Help**: https://docs.github.com
- **Streamlit Cloud**: https://docs.streamlit.io/streamlit-cloud
- **Full Deployment Guide**: See `DEPLOYMENT_GUIDE.md`

---

**Ready?** Replace YOUR_USERNAME and REPO_NAME above and run the commands!
